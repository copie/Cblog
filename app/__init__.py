from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config
from flask_login import LoginManager
from flask_pagedown import PageDown


mail = Mail()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = '在访问此页面之前请先登陆'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .manage import manage as manage_blueprint
    app.register_blueprint(manage_blueprint)

    return app
