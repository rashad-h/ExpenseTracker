from flask.helpers import url_for
from app import app
from app import db
from app import admin
from app import login
from app import models
from flask import render_template, flash, request , redirect
from flask_admin.contrib.sqla import ModelView 
from flask_login import login_user, login_required, logout_user, current_user

from sqlalchemy import desc

from werkzeug.security import generate_password_hash, check_password_hash

import logging
import datetime
from .forms import LoginForm, RegisterationForm, ExpenseForm


# adding the expense models if not existed
# models_exist = models.ExpenseType.query.get(1)
# if models_exist:
#     pass
# else:
#     expense_type = models.ExpenseType(name="Rent/Utilities", color="#FAFFC7")
#     db.session.add(expense_type)
#     db.session.commit()

# personal model view to restrict admin view
class myModelView(ModelView):
    def is_accessible(self):
        return True


# overwriting the user_loader function
@login.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


#adding the path if user is not logged in
login.login_view = "login"


# adding the models to the Flask Adminstration
admin.add_view(myModelView(models.User, db.session))
admin.add_view(myModelView(models.Expense, db.session))
admin.add_view(myModelView(models.ExpenseType, db.session))


# code to run when on home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="Home")


# view for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        if form.validate_on_submit():
            user = models.User.query.filter_by(username=form.username.data).first()
            # check if the user exists
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    logging.info(f'User with username {user.username} was logged in')
                    return redirect(url_for('dashboard'))

            flash("Incorrect username or password")
            return render_template('login.html', title="Login", form=form)
        return render_template('login.html', title="Login", form=form)

# view for the sign up page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegisterationForm()

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            
            check_user = models.User.query.filter_by(username=form.username.data).first()
            if check_user:
                flash("The username is taken")
            else:
                check_user = models.User.query.filter_by(email=form.email.data).first()
                if check_user:
                    flash("Email already Exists!")
                else:
                    new_user = models.User(email = form.email.data, username = form.username.data, password = hashed_password)
                    db.session.add(new_user)
                    db.session.commit()
                    logging.info(f'User with username {new_user.username} was added')

                    login_user(new_user)
                    logging.info(f'User with username {new_user.username} was logged in')
                    return redirect(url_for('dashboard'))
        for field, errors in form.errors.items():
                for error in errors:
                    flash("{}: {}".format(
                        getattr(form, field).label.text,
                        error
                    ))
        return render_template('registeration.html', title='Sign Up', form=form)


# adding view for dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    expenses = models.Expense.query.filter_by(user_id=user.id).order_by(desc(models.Expense.date)).all()
    return render_template('dashboard.html', title='Dashboard', user=user, expenses=expenses)


# adding expenses to your account
@app.route('/addExpenses', methods=['GET', 'POST'])
@login_required
def addExpenses():
    user = current_user
    form = ExpenseForm()

    expenses = models.Expense.query.filter_by(user_id=user.id).order_by(desc(models.Expense.date)).all()

    if form.validate_on_submit():
        if form.description.data:
            description = form.description.data
        else:
            description = '-'
        expenseType = models.ExpenseType.query.filter_by(name=form.expenseType.data).first()
        new_expense = models.Expense(amount=form.amount.data,
                                    expense_id=expenseType.id,
                                    user_id=user.id,
                                    description=description, 
                                    date=form.date.data)
        db.session.add(new_expense)
        user.total_expense_amount = user.total_expense_amount + float(new_expense.amount)

        db.session.commit()
        flash("Expense was added successfully!")
        logging.info(f'User with username {user.username} added expense with amount {new_expense.amount} type {new_expense.expense_type.name}')
        
        return redirect('/addExpenses')
    
    for field, errors in form.errors.items():
        for error in errors:
            flash("{}: {}".format(
                getattr(form, field).label.text,
                error
            ))
    return render_template('add_expenses.html', title='Add Expenses', user=user, form=form, expenses=expenses)


# adding a view for statistics
@app.route('/statistics')
@login_required
def statistics():
    recent_expenses = models.Expense.query.filter_by(user_id=current_user.id).order_by(desc(models.Expense.date)).limit(10).all()
    labels = []
    values = []
    type_numbers = []
    for expense in recent_expenses:
        labels.append(expense.date.strftime("%m/%d/%Y"))
        values.append(expense.amount)

    for type in models.ExpenseType.query.all():
        type_amount = 0
        for expense in type.expenses:
            if expense.user_id == current_user.id:
                type_amount = type_amount + expense.amount
        type_numbers.append(type_amount)

    labels.reverse()
    values.reverse()

    return render_template('statistics.html', title='Statistics', user=current_user,
                         recent_values=values, recent_labels=labels,
                        type_numbers=type_numbers)


# if users choose to logout
@app.route('/logout')
@login_required
def logout():
    logging.info(f'User with username {current_user.username} was logged out')
    logout_user()
    return redirect(url_for('index'))
