import pytest
from app import create_app, db as _db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test_secret"
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    return _db
