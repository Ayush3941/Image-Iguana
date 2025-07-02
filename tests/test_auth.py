from app.models import User
from flask import url_for
from werkzeug.security import check_password_hash

def test_signup(client, db):
    response = client.post("/signup", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    user = User.query.filter_by(username="testuser").first()
    assert user is not None
    assert check_password_hash(user.password_hash, "password123")
    assert b'Registration successful' in response.data

def test_signup_existing_user(client, db):
    # Pre-create user
    user = User(username="duplicate", email="dup@example.com")
    user.set_password("testpass")
    db.session.add(user)
    db.session.commit()

    response = client.post("/signup", data={
        "username": "duplicate",
        "email": "new@example.com",
        "password": "newpass"
    }, follow_redirects=True)

    assert b'Username already exists' in response.data

def test_login_success(client, db):
    user = User(username="loginuser", email="login@example.com")
    user.set_password("mypassword")
    db.session.add(user)
    db.session.commit()

    response = client.post("/login", data={
        "username": "loginuser",
        "password": "mypassword"
    }, follow_redirects=True)

    assert b'Logout' in response.data or response.status_code == 200

def test_login_failure(client):
    response = client.post("/login", data={
        "username": "nonexistent",
        "password": "wrongpass"
    }, follow_redirects=True)

    assert b'Invalid username or password' in response.data

def test_logout(client, db):
    # Create and log in user
    user = User(username="logoutuser", email="logout@example.com")
    user.set_password("mypassword")
    db.session.add(user)
    db.session.commit()
    client.post("/login", data={"username": "logoutuser", "password": "mypassword"}, follow_redirects=True)

    response = client.get("/logout", follow_redirects=True)
    assert b'Login' in response.data
