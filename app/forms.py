# forms.py (create this file)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_wtf.file import FileAllowed, FileRequired, FileField, MultipleFileField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')


class EditImageForm(FlaskForm):

    file = MultipleFileField(
    "Upload Files",
    validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ]
)

    format_conversion = SelectField("Format Conversion", choices=[
        ("", "Choose format conversion"),
        ("cpng", "Convert to PNG"),
        ("cjpg", "Convert to JPG"),
        ("cjpeg", "Convert to JPEG"),
        ("cwebp", "Convert to WEBP")
    ], validators=[Optional()])

    image_processing = SelectField("Image Processing", choices=[
        ("", "Choose image processing option"),
        ("cgray", "Convert to Grayscale"),
        ("histeq", "B&W - Contrast + Grain"),
        ("blur", "Blur Image"),
        ("canny", "Edge Image"),
        ("rotate", "Rotate Clockwise"),
        ("sharpen", "Sharpen Image")
    ], validators=[Optional()])

    submit = SubmitField("Submit")
