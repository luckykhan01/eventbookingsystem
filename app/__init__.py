from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB max size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


from app import routes, models