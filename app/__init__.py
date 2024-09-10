import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app(config_type):
    app = Flask(__name__, static_folder='static')

    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')

    app.config.from_pyfile(configuration)

    db.init_app(app)
    bootstrap.init_app(app)
    bootstrap.load_css = True
    login_manager = LoginManager(app)
    bcrypt = Bcrypt(app)

    from app.catalog import main
    app.register_blueprint(main)

    from app.auth import authentication
    app.register_blueprint(authentication)

    return app