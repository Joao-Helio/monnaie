from flask import Flask, render_template
from flask_migrate import Migrate
from models import db, HouseHold, Account, Category, Transaction, CreditCard, FutureExpense
from sqlalchemy import func
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monnaiedb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def dashboard():
    accounts = Account.query.all()
    total_balance = sum(account.balance for account in accounts)
    
    # Calculate total bills and expenses for the current month
    current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = current_month + timedelta(days=32)
    next_month = next_month.replace(day=1)
    
    total_expenses = db.session.query(func.sum(Transaction.amount)).\
        filter(Transaction.is_expense == True, 
               Transaction.date >= current_month,
               Transaction.date < next_month).scalar() or 0
    
    return render_template('dashboard.html', accounts=accounts, total_balance=total_balance, total_expenses=total_expenses)

@app.route('/accounts')
def accounts():
    accounts = Account.query.all()
    return render_template('accounts.html', accounts=accounts)

@app.route('/expenses')
def expenses():
    categories = Category.query.all()
    expenses = Transaction.query.filter_by(is_expense=True).order_by(Transaction.date.desc()).all()
    return render_template('expenses.html', categories=categories, expenses=expenses)

@app.route('/credit_cards')
def credit_cards():
    credit_cards = CreditCard.query.all()
    return render_template('credit_cards.html', credit_cards=credit_cards)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
