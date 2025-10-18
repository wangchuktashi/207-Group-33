# website/forms.py
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

# Login form
class LoginForm(FlaskForm):
    email_id = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

# Registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First name", validators=[InputRequired(), Length(max=100)])
    surname = StringField("Surname", validators=[InputRequired(), Length(max=100)])
    email_id = StringField("Email", validators=[InputRequired(), Email(), Length(max=100)])
    mobile_number  = StringField(
        "Contact number",
        validators=[InputRequired(), Regexp(r'^\+?\d[\d\s-]{6,}$', message="Enter a valid phone number")]
    )
    street_address = StringField("Street address", validators=[InputRequired(), Length(max=256)])

    password = PasswordField("Password", validators=[
        InputRequired(),
        Length(min=6),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm  = PasswordField("Confirm Password")
    street_address = StringField("Street address", validators=[InputRequired(), Length(max=255)])

    submit = SubmitField("Register")