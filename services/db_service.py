from flask_sqlalchemy import SQLAlchemy
import boto3
import json
from http.client import HTTPException
from botocore.exceptions import ClientError
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

log = logging.getLogger(__name__)

# Inicializar SQLAlchemy
db = SQLAlchemy()

# Obtener credenciales desde AWS Secrets Manager
def get_secret_manager_db():
    secret_name = "rds!cluster-9b4b7cd8-22ee-48ff-bbc4-d1f43ddf3bc8"
    region_name = "us-east-1"

    try:
        client = boto3.client("secretsmanager", region_name=region_name)
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])
        
        # Proporcionar valores predeterminados para host y dbname si no están en el secreto
        secret["host"] = secret.get("host", "cluster-gamer-vault.cluster-c6r6ws4k4vwo.us-east-1.rds.amazonaws.com:3306")
        secret["dbname"] = secret.get("dbname", "gamervaultlts")
        
        return secret
    except ClientError as e:
        log.error(f"Error al obtener el secreto: {e}")
        raise Exception("No se pudieron obtener las credenciales de la base de datos.") from e

# Configuración de la base de datos
def init_app(app):
    try:
        db_credentials = get_secret_manager_db()
        DB_HOST = db_credentials["host"]
        DB_NAME = db_credentials["dbname"]
        DB_USER = db_credentials["username"]
        DB_PASS = db_credentials["password"]

        app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(app)
        log.info("Base de datos configurada correctamente")

        # Verificar conexión a la base de datos
        with app.app_context():
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))  # Consulta simple para verificar la conexión
                log.info("Conexión exitosa a la base de datos")
    except Exception as e:
        log.critical("Error crítico al configurar la base de datos: %s", str(e))
        raise Exception("Error crítico: No se pudo configurar la base de datos.") from e