from app import db
from flask_login import UserMixin

# creat a User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique = True)
    username = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(80), unique = True)
    total_expense_amount = db.Column(db.Float, default=0.00)
    expenses = db.relationship('Expense', backref='user')


# create a model for all the expenses by all users
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), default='-')
    amount = db.Column(db.Float, nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense_type.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# create a model for all the expense types
class ExpenseType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique = True)
    color = db.Column(db.String(50), unique = True)
    expenses = db.relationship('Expense', backref='expense_type')
