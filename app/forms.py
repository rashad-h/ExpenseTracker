from typing import Text
from werkzeug.utils import validate_arguments
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import PasswordField, BooleanField, DecimalField, SelectField
from wtforms import DateField
from wtforms.validators import DataRequired, InputRequired, Email, Length, NumberRange
import datetime


# a form class for user Registeration
class RegisterationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),
                         Email(message="Invalid Email!"), Length(max=50)], 
                        render_kw={"class": "form-control", "placeholder": "Email"})
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=30)], 
                            render_kw={"class": "form-control", "placeholder": "username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)],
                            render_kw={"class": "form-control", "placeholder": "password"})


# a form class for user Login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=30)],
                             render_kw={"class": "form-control", "placeholder": "username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(max=80)], 
                            render_kw={"class": "form-control", "placeholder": "password"})
    remember = BooleanField('Remember Me')


# a form for the adding expenses
class ExpenseForm(FlaskForm):
    amount = DecimalField('Amount', places=2, rounding=None, validators=[InputRequired(),
                            NumberRange(min=0, message='Must enter a number greater than 0')], 
                            render_kw={"class": "form-control", "id": "amountID",
                            "type": "number", "min": "0.01", "step": "0.01"})
    date = DateField('Date', format='%Y-%m-%d', default = datetime.date.today(),
    validators=[InputRequired()], 
                    render_kw={"class": "form-control", "id": "dateID",
                                "type": "date"})
    expenseType = SelectField('Choose a type',
                             choices=['Rent/Utilities', 'Food & Groceries', 'Transportation',
                                        'Savings', 'Entertainment', 'Healthcare', 'Others'],
                               option_widget=None, validators=[InputRequired()],
                               render_kw={"class": "form-control", "id": "typeID"})
    description = StringField('Description', 
                                render_kw={"class": "form-control", "id": "descriptionID"},
                                validators=[Length(max=50)]);