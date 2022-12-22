from expense import db,jwt
from datetime import date
import uuid
from werkzeug.security import generate_password_hash, check_password_hash



class UsersModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(128), unique=True)
    created = db.Column(db.Date, default=date.today)
    updated = db.Column(db.Date, default=date.today)
    password_hash = db.Column(db.String(128))
    expenses = db.relationship('Expense', backref='user', lazy=True)

    def __init__(self, email, name ,password):
        self.public_id = str(uuid.uuid4())
        self.email = email
        self.name = name
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Expense(db.Model):
    __tablename__  = "expense"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(128),nullable=False)
    incurred_on = db.Column(db.Date, default=date.today, nullable=False)
    notes = db.Column(db.String(128), nullable=False)
    updated_at = db.Column(db.Date, default=date.today,nullable=False)

    def __init__(self, userId: int, title:str, amount:float, category:str, incurred_on:date, notes:str)->None:
        self.userId = userId
        self.title = title
        self.amount = amount
        self.category = category
        self.incurred_on = incurred_on
        self.notes = notes


