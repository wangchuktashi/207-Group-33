# website/forms.py
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Login form
class LoginForm(FlaskForm):
    email_id = StringField("Email", validators=[InputRequired(), Email(), Length(max=100)])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

# Registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First name", validators=[InputRequired(), Length(max=100)])
    surname = StringField("Surname", validators=[InputRequired(), Length(max=100)])
    email_id = StringField("Email", validators=[InputRequired(), Email(), Length(max=100)])
    mobile_number = StringField(
        "Contact number",
        validators=[
            InputRequired(),
            Regexp(r'^\+?\d[\d\s-]{6,}$', message="Enter a valid phone number")
        ]
    )
    street_address = StringField("Street address", validators=[InputRequired(), Length(max=255)])

    password = PasswordField("Password", validators=[
        InputRequired(),
        Length(min=6),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

# event form
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Destination Image', validators=[
        FileRequired(message = 'Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    currency = StringField('Currency', validators=[InputRequired()])
    submit = SubmitField("Create")
    # more to add...


# user comment form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Create')
    
