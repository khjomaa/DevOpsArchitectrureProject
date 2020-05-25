from flask import Flask
from flask_login import LoginManager
from app.config import Config

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)

    from app.users.routes import users
    from app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app

