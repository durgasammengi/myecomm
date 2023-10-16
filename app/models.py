from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=False)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(10), index=True, unique=False)
    cart = db.relationship('Cart', backref='user', lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
@login.user_loader
def load_user(id):
    # Retrieve a user object from the database based on the provided user ID.
    return User.query.get(int(id))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    product_type = db.Column(db.String(20), nullable=True)  # Added product_type field

    def __init__(self, name, description, price, image_path, product_type):
        self.name = name
        self.description = description
        self.price = price
        self.image_path = image_path
        self.product_type = product_type

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define Cart model fields (e.g., product_id, quantity, etc.)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1) 