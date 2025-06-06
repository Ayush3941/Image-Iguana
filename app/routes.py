# app/routes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, send_file
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from .models import User
from .utils import allowed_file, processImage
from .forms import LoginForm, SignupForm, EditImageForm
from . import db, login_manager
import os, base64, tempfile, zipfile, shutil
from PIL import Image
from io import BytesIO



main = Blueprint('main', __name__)

@main.route("/")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    form = EditImageForm()
    return render_template("index.html", form=form)


@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html', form=form)

@main.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('main.signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('main.signup'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('main.login'))

    return render_template('signup.html', form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route("/about")
@login_required
def about():
    return render_template("about.html", title="About")




@main.route("/", methods=["GET", "POST"])
@login_required
def edit():
    form = EditImageForm()

    if form.validate_on_submit():
        # Handle annotation
        if 'annotated_image' in request.form and request.form['annotated_image']:
            data_url = request.form['annotated_image']
            original_filename = request.form['original_filename']
            edited_filename = request.form['edited_filename']

            header, encoded = data_url.split(",", 1)
            data = base64.b64decode(encoded)
            img = Image.open(BytesIO(data))
            annotated_path = os.path.join("static", "uploads", "annotated_" + os.path.basename(edited_filename))
            img.save(annotated_path)

            return render_template(
                "preview.html",
                original_filename=original_filename,
                edited_filename=os.path.relpath(annotated_path, "static").replace("\\", "/")
            )

        format_conversion = form.format_conversion.data
        image_processing = form.image_processing.data
        files = form.file.data  # This should be `MultipleFileField` in the form

        if not files or (len(files) == 1 and files[0].filename == ''):
            flash('No files selected for upload')
            return redirect(url_for('main.home'))

        processed_files = []
        error_files = []

        for file in files:
            try:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    abra = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","uploads")

                    file_path = os.path.join(abra, filename)
                    file.save(file_path)

                    processed_file = processImage(filename, format_conversion, image_processing)
                    if processed_file:
                        processed_files.append(processed_file)
                    else:
                        error_files.append(f"{filename} (processing failed)")
                else:
                    error_files.append(f"{file.filename} (invalid type)")
            except Exception as e:
                error_files.append(f"{file.filename} (error: {str(e)})")

        if error_files:
            flash(f"Errors with {len(error_files)} file(s): {', '.join(error_files[:3])}{'...' if len(error_files) > 3 else ''}")

        if not processed_files:
            flash('No files were processed successfully')
            return redirect(url_for('main.home'))
        print("dguqgwdviquwbdliqhwbdxiouqwgd    oiwydvweidv wiqh",processed_files)
        if len(processed_files) == 1:
            download_filename = os.path.basename(processed_files[0])
            return send_file(
                processed_files[0],
                as_attachment=True,
                download_name=download_filename,
                mimetype='image/png'
            )

        # Zip for multiple
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, 'processed_images.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in processed_files:
                zipf.write(file_path, os.path.basename(file_path))

        def cleanup():
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Cleanup error: {e}")

        response = send_file(
            zip_path,
            as_attachment=True,
            download_name='processed_images.zip',
            mimetype='application/zip'
        )
        response.call_on_close(cleanup)
        return response

    return render_template("index.html", form=form)


@main.route("/usage")
@login_required
def usage():
    return render_template("usage.html", title="Usage")

@main.route("/download/<path:filename>")
@login_required
def download(filename):
    file_path = os.path.join("static", filename)
    return send_file(file_path, as_attachment=True)