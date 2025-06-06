from .auth import auth_bp
from .main import main_bp
from .image_processing import image_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp, url_prefix="/")
    app.register_blueprint(image_bp, url_prefix="/image")
