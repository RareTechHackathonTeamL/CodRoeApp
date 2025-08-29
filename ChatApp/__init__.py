from flask import Flask
from flask_login import LoginManager
import os
import uuid
from util.assets import bundle_css_files

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
    app.config['ICON_FOLDER'] = 'static/img/user_icons/'
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

    login_manager.init_app(app)
    bundle_css_files(app)
    return app
