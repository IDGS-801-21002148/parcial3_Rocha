from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime  # Agrega este import

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_plain = db.Column(db.String(255), nullable=True)  
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_plain = password  
        self.password_hash = generate_password_hash(password)  

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Cliente(db.Model):
    __tablename = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombreCompleto = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(100))
    fechaPedido = db.Column(db.Date, default=datetime.datetime.utcnow)
    total = db.Column(db.Float)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

class Pizzas(db.Model):
    __tablename = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    tamaño = db.Column(db.String(100))
    ingredientes = db.Column(db.String(255))
    cantidadPizzas = db.Column(db.String(100))
    subTotal = db.Column(db.Float)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)