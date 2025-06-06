from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..forms import EditImageForm

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@login_required
def home():
    form = EditImageForm()
    return render_template("index.html", form=form)

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/usage")
def usage():
    return render_template("usage.html")
