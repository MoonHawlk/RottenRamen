from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)


app.config['SECRET_KEY'] = 'bae137565d7b103cafc4ccfed0d32e63'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rottenramen.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor faça login para usar essa funcionalidade.'
login_manager.login_message_category = 'alert-info'


from rottenramen import routes
