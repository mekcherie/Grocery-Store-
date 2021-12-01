from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os

from grocery_app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)

from grocery_app.routes import auth, main
app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()