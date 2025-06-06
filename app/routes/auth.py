from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from ..forms import LoginForm, SignupForm
from ..models import User
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        flash("Invalid username or password")
    return render_template("login.html", form=form)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists")
            return redirect(url_for("auth.signup"))
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered")
            return redirect(url_for("auth.signup"))

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for("auth.login"))

    return render_template("signup.html", form=form)

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
