from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required
from ..forms import EditImageForm
from ..utils import allowed_file, processImage
from PIL import Image
import os, base64
from io import BytesIO
from werkzeug.utils import secure_filename

image_bp = Blueprint('image', __name__)

@image_bp.route("/edit", methods=["GET", "POST"])
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
                    abra = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","uploads")

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