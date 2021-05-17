from flask import Flask
from config import Config, TestingConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# initialise app as a Flask object
app = Flask(__name__)
# run the config function to establish environment variables
app.config.from_object(Config)
# for testing, we uncomment this line to use the test database or memory
#app.config.from_object(TestingConfig)
# handle database management using SQLAlchemy and Flask-migrate (for portable databases)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
# handle user authentification for logins
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, helper