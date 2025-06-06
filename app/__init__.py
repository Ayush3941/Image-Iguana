from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from .routes import register_routes
    register_routes(app)

    return app

