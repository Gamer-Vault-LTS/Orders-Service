from flask import Blueprint, request, jsonify
from models.order_model import Order
from models.user_model import User
from models.wallet_model import Wallet
from services.db_service import db
from decimal import Decimal, InvalidOperation
from models.challenge_levels_model import ChallengeLevels

order_bp = Blueprint("orders", __name__)

def set_challenge_level(user_id):
    try:
        
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 401
        
        progress = user.challenge_progress
        progress += 1
        
        levels = ChallengeLevels.query.all()
        
        for level in levels:
            if progress >= level.min_transactions:
                user_lvl = level.level_id
                
        user.challenge_level_id = user_lvl
        user.challenge_progress = progress
        
        db.session.commit()
        return jsonify({"message": "Challenge level updated"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@order_bp.route("", methods=["POST"])
def create_order():
    
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        # Verificar si el usuario existe
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Verificar si el usuario tiene wallet
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if not wallet:
            return jsonify({"error": "Wallet not found"}), 404

        # Validar y convertir los montos a Decimal
        try:
            total = Decimal(str(data.get("total", "0")))
            savings = Decimal(str(data.get("savings", "0")))
        except (InvalidOperation, TypeError, ValueError):
            return jsonify({"error": "Invalid total or savings format"}), 400

        # Asegurar que wallet.balance es Decimal
        if not isinstance(wallet.balance, Decimal):
            wallet.balance = Decimal(str(wallet.balance))

        # Crear la orden
        new_order = Order(
            user_id=user_id,
            total=total,
            savings=savings,
            status=data.get("status", "pending"),
            description=data.get("description"),
            payment_method=data.get("payment_method"),
        )

        db.session.add(new_order)

        # Sumar savings al balance de la wallet
        wallet.balance += savings
        
        set_challenge_level(user_id)
        
        db.session.commit()
        
        return jsonify({
            "message": "Order created and savings added to wallet successfully",
            "order_id": new_order.order_id,
            "new_balance": float(wallet.balance)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@order_bp.route("/<user_id>", methods=["GET"])
def get_user_orders(user_id):
    # Verificar si el usuario existe
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Obtener las órdenes del usuario
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.asc()).all()

    # Formatear la respuesta
    return jsonify([{
        "order_id": o.order_id,
        "total": float(o.total),
        "savings": float(o.savings),
        "status": o.status,
        "description": o.description,
        "created_at": o.created_at.isoformat(),
        "payment_method": o.payment_method
    } for o in orders])
    
@order_bp.route("detail/<order_id>", methods=["GET"])
def get_order(order_id):
    
    try:
        order_id = str(order_id)
        
        order = Order.query.filter_by(order_id=order_id).first()
        
        if not order:
            return jsonify({"error": "Order not found"}), 404
        
        return jsonify(
            { 
                "created_at": order.created_at,
                "order_id": order.order_id,
                "total": float(order.total),
                "savings": float(order.savings),
                "status": order.status,
                "description": order.description,  
                "payment_method": order.payment_method
            } 
        ), 200
    except ValueError as e:
        return jsonify({"OrderError": e}), 400
    