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
def client(app):
    return app.test_client()

def test_signup_success(client):
    response = client.post('/signup', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful' in response.data

def test_signup_duplicate_username(client):
    # First create a user
    client.post('/signup', data={
        'username': 'dupuser',
        'email': 'dupuser1@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    # Try signing up with same username again
    response = client.post('/signup', data={
        'username': 'dupuser',
        'email': 'dupuser2@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    assert b'Username already exists' in response.data

def test_signup_duplicate_email(client):
    # First create a user
    client.post('/signup', data={
        'username': 'uniqueuser',
        'email': 'dupemail@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    # Try signing up with same email again
    response = client.post('/signup', data={
        'username': 'anotheruser',
        'email': 'dupemail@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    assert b'Email already registered' in response.data

def test_login_success(client):
    # First signup user
    client.post('/signup', data={
        'username': 'loginuser',
        'email': 'loginuser@example.com',
        'password': 'loginpass',
        'confirm_password': 'loginpass'
    }, follow_redirects=True)

    # Then login
    response = client.post('/login', data={
        'username': 'loginuser',
        'password': 'loginpass',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' in response.data or b'Welcome' in response.data

def test_login_invalid_password(client):
    # Signup user
    client.post('/signup', data={
        'username': 'wrongpassuser',
        'email': 'wrongpass@example.com',
        'password': 'correctpass',
        'confirm_password': 'correctpass'
    }, follow_redirects=True)

    # Login with wrong password
    response = client.post('/login', data={
        'username': 'wrongpassuser',
        'password': 'wrongpass',
    }, follow_redirects=True)
    assert b'Invalid username or password' in response.data

def test_logout(client):
    # Signup and login first
    client.post('/signup', data={
        'username': 'logoutuser',
        'email': 'logoutuser@example.com',
        'password': 'logoutpass',
        'confirm_password': 'logoutpass'
    }, follow_redirects=True)
    client.post('/login', data={
        'username': 'logoutuser',
        'password': 'logoutpass',
    }, follow_redirects=True)

    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert b'Login' in response.data or b'Sign In' in response.data


def test_password_hashing():
    user = User(username='testuser')
    user.set_password('mysecurepassword')

    # Check that the password is hashed and starts with a known scheme
    assert user.password_hash != 'mysecurepassword'
    assert user.password_hash.startswith(('pbkdf2:', 'scrypt:'))  # accepts both

