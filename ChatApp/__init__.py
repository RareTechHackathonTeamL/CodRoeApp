from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import uuid
from util.assets import bundle_css_files

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
        'user': DB_USER,
        'password':DB_PASSWORD,
        'host':DB_HOST,
        'db_name':DB_DATABASE,
        })
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ICON_FOLDER'] = 'static/img/user_icons/'
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024


    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bundle_css_files(app)
    return app
