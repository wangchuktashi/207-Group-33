# website/forms.py
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, AnyOf, NumberRange
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

    # No regex: just require presence + sensible length range
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
    event_title = StringField('Event Title', validators=[InputRequired()])
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
    home_team = StringField('Home Team', validators=[InputRequired()])
    away_team = StringField('Away Team', validators=[InputRequired()])
    start_datetime = DateField('Event Date', format='%Y-%m-%d', 
                               validators=[InputRequired(message='Please choose a start date and time')])
    end_datetime = DateField('Event Date', format='%Y-%m-%d',
                           validators=[InputRequired(message='Please choose an end date time.')])
    venue = StringField('Venue', validators=[InputRequired()])
    total_tickets = SelectField(
        'Total Tickets',
        coerce=int,
        choices=[(i, str(i)) for i in range(1, 50001)],
        validators=[
            InputRequired(message='Please select number of tickets'),
            NumberRange(min=1, max=50000, message='Select between 1 and 50000 tickets')
        ]
    )
    image = FileField('Event Image', validators=[
        FileRequired(message = 'Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    description = TextAreaField('Description', validators=[InputRequired(message='Short description for attendees...')])
    submit = SubmitField("Create Event")
    reset = SubmitField("Reset")

# user comment form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Create')
    
