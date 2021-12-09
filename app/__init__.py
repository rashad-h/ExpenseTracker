from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
import logging

logging.basicConfig(filename='expense_tracker.log', format='%(asctime)s %(message)s', level=logging.DEBUG)


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


migrate = Migrate(app, db)

# to tell the flask_admin which application it is attached to and to use bootstrap
admin = Admin(app,template_mode='bootstrap3')
login = LoginManager()
login.init_app(app)


from app import views, models
