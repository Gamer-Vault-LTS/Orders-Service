from services.db_service import db

class User(db.Model):
    __tablename__ = "users"
    
    # Definición de columnas
    user_id = db.Column(db.String(36), primary_key=True)  # UUID como clave primaria
    first_name = db.Column(db.String(50))  # Primer nombre
    last_name = db.Column(db.String(50))  # Apellido
    username = db.Column(db.String(50), unique=True)  # Nombre de usuario único
    email = db.Column(db.String(100), unique=True)  # Correo electrónico único
    password_hash = db.Column(db.String(255))  # Hash de la contraseña
    phone = db.Column(db.String(20))  # Teléfono
    birth_date = db.Column(db.Date)  # Fecha de nacimiento
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Marca de tiempo de creación
    avatar = db.Column(db.String(255)) # URL o nombre del archivo del avatar
    challenge_level_id = db.Column(db.Integer)
    challenge_progress = db.Column(db.Integer)
    
    
    def __init__(self, first_name, last_name, username, email, password_hash, challenge_level_id, challenge_progress, phone=None, birth_date=None, avatar=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.phone = phone
        self.birth_date = birth_date
        self.avatar = avatar
        self.challenge_level_id = challenge_level_id
        self.challenge_progress = challenge_progress

    def __repr__(self):
        return f"<User {self.username}>"
