from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, IntegerField,HiddenField,  SubmitField, StringField, PasswordField, SelectField, DateTimeLocalField
from wtforms.validators import InputRequired, Length, Email, EqualTo, AnyOf, NumberRange, Optional
from flask_wtf.file import FileRequired, FileField, FileAllowed
from datetime import datetime

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
        validators=[InputRequired(), Length(min=8, max=15, message="Enter 8–15 characters")]
    )

    street_address = StringField("Street address", validators=[InputRequired(), Length(max=255)])

    password = PasswordField("Password", validators=[
        InputRequired(),
        Length(min=6),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm  = PasswordField("Confirm Password")

    submit = SubmitField("Register")
# event form
class EventForm(FlaskForm):
    event_title = StringField('Event Title', validators=[InputRequired(), Length(max=256)])
    sport_type = SelectField(
        'Sport Type',
        choices=[
            ('football', 'Football'),
            ('basketball', 'Basketball'),
            ('rugby', 'Rugby'),
            ('cricket', 'Cricket'),
            ('tennis', 'Tennis'),
            ('hockey', 'Hockey'),
        ],
        validators=[
            InputRequired(message='Please choose a sport'),
            AnyOf(values=['football','basketball','rugby','cricket','tennis','hockey'],
                  message='Invalid sport selected')
        ]
    )
    home_team = StringField('Home Team', validators=[InputRequired(),  Length(max=64)])
    away_team = StringField('Away Team', validators=[InputRequired(),  Length(max=64)])
    start_datetime = DateTimeLocalField('Event Date', format='%Y-%m-%dT%H:%M', 
                               validators=[InputRequired(message='Please choose a start date and time')])
    end_datetime = DateTimeLocalField('Event Date', format='%Y-%m-%dT%H:%M',
                           validators=[InputRequired(message='Please choose an end date time.')])
    venue = StringField('Venue', validators=[InputRequired(), Length(max=128)])
    total_tickets = IntegerField(
        'Total Tickets',
        validators=[InputRequired(), NumberRange(min=1, max=50000)],
        render_kw={'min': 1, 'max': 50000, 'step': 1}
    )
    image = FileField('Event Image', validators=[
        FileRequired(message = 'Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    description = TextAreaField('Event description', validators=[Optional(), Length(max=5000)])
    submit = SubmitField("Create Event")
    reset = SubmitField("Reset")

class BookingForm(FlaskForm):
    event_id = HiddenField(validators=[InputRequired()])
    ticket_type = SelectField(
        "Ticket type",
        choices=[("General", "General"), ("Student", "Student"), ("VIP", "VIP")],
        validators=[InputRequired()]
    )
    quantity = IntegerField(
        "Quantity",
        validators=[InputRequired(), NumberRange(min=1, max=10, message="1–10 only")]
    )
    submit = SubmitField("Book Now")

# user comment form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Post Comment')
    
