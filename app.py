from flask import Flask, jsonify
from controllers.order_controller import order_bp
from services.db_service import init_app, db 
from sqlalchemy import text  

app = Flask(__name__)

init_app(app)


app.register_blueprint(order_bp, url_prefix="/orders")

@app.route("/")
def root():
    return jsonify({"status": "healthy"}), 200

@app.route('/health')
def health_check():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return "OK - Database Connected", 200
    except Exception as e:
        return f"Database Connection Failed: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
