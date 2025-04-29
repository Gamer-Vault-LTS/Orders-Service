from flask import Flask
from controllers.order_controller import order_bp
from services.db_service import init_app, db 
from sqlalchemy import text  

app = Flask(__name__)

# Inicializar la base de datos
init_app(app)

# Registrar blueprints
app.register_blueprint(order_bp, url_prefix="/orders")

# Ruta para comprobar la salud de la aplicación
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
