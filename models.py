from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    name = db.Column(db.String(80), nullable=False)  # Nome do usuário
    email = db.Column(db.String(120), unique=True, nullable=False)  # E-mail único
    password_hash = db.Column(db.String, nullable=True)
    id_house_hold = db.Column(db.Integer, db.ForeignKey('house_hold.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

class HouseHold(db.Model):
    __tablename__ = 'house_hold'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    accounts = db.relationship('Account', backref='house_hold', lazy=True)
    credit_cards = db.relationship('CreditCard', backref='house_hold', lazy=True)
    users = db.relationship('User', backref='house_hold', lazy=True)
    categories = db.relationship('Category', backref='house_hold', lazy=True)
    future_expenses = db.relationship('FutureExpense', backref='house_hold', lazy=True)


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    balance = db.Column(db.Numeric, nullable=True)
    id_house_hold = db.Column(db.Integer, db.ForeignKey('house_hold.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    transactions = db.relationship('Transaction', backref='account', lazy=True)


class CreditCard(db.Model):
    __tablename__ = 'credit_cards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1), nullable=True)
    limit = db.Column(db.BigInteger, nullable=True)
    closing_date = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    current_balance = db.Column(db.Numeric, nullable=True)
    id_house_hold = db.Column(db.Integer, db.ForeignKey('house_hold.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    transactions = db.relationship('Transaction', backref='credit_card', lazy=True)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric, nullable=True)
    date = db.Column(db.Date, nullable=True)
    description = db.Column(db.String, nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)
    credit_card_id = db.Column(db.Integer, db.ForeignKey('credit_cards.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    is_expense = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

class FutureExpense(db.Model):
    __tablename__ = 'future_expenses'
    id = db.Column(db.Integer, primary_key=True)
    id_house_hold = db.Column(db.Integer, db.ForeignKey('house_hold.id'), nullable=True)
    description = db.Column(db.String(1), nullable=True)
    amount = db.Column(db.Numeric, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    id_categories = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1), nullable=True)
    id_house_hold = db.Column(db.Integer, db.ForeignKey('house_hold.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    transactions = db.relationship('Transaction', backref='category', lazy=True)
    future_expenses = db.relationship('FutureExpense', backref='category', lazy=True)
