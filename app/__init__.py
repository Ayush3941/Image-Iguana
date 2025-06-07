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
    print("Using database:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Set this to your actual login route

    with app.app_context():
        from .models import User  # Import here to avoid circular import

        @login_manager.user_loader
        def load_user(user_id):
            return db.session.get(User, int(user_id))

        from .routes.auth import auth_bp
        app.register_blueprint(auth_bp) 
        from .routes.main import main_bp
        app.register_blueprint(main_bp) 
        from .routes.image_processing import image_bp
        app.register_blueprint(image_bp) 

        db.create_all()  # optional: create tables if not already created

    return app
