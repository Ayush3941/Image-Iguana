import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app, db
from app.models import User
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()

@pytest.fixture
def session(app):
    return db.session

def test_user_creation(session):
    user = User(username='testuser', email='test@example.com')
    user.set_password('securepass')
    session.add(user)
    session.commit()

    retrieved = User.query.filter_by(username='testuser').first()
    assert retrieved is not None
    assert retrieved.email == 'test@example.com'
    assert retrieved.username == 'testuser'

def test_password_hashing_and_check(session):
    user = User(username='secureuser', email='secure@example.com')
    user.set_password('supersecret')
    session.add(user)
    session.commit()

    assert user.password_hash != 'supersecret'
    assert user.password_hash.startswith(('pbkdf2:', 'scrypt:'))  # Accept both
    assert user.check_password('supersecret') is True
    assert user.check_password('wrongpassword') is False
