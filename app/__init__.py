from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_migrate import Migrate

from flask import Flask
from flask_session import Session
import redis

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
migrate = Migrate(app, db)
mail = Mail(app)

app.config['SESSION_TYPE'] = 'redis'  # Use Redis as the session store
app.config['SESSION_PERMANENT'] = False  # Sessions are not permanent
app.config['SESSION_USE_SIGNER'] = True  # Sign session cookie for added security

# Configure Redis server for Flask-Session
app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=0)

# Set the session timeout (10 minutes)
app.config['PERMANENT_SESSION_LIFETIME'] = 600  # 600 seconds = 10 minutes

# Initialize Flask-Session
Session(app)

from app import routes, models