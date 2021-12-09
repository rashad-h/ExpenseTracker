import os


WTF_CSRF_ENABLED = True
SECRET_KEY = 'my-key'



# create the path to the database
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_tRICK_MODIFICATIONS = True

