# website/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp

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

    submit = SubmitField("Register")
