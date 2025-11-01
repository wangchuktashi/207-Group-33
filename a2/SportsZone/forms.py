# website/forms.py
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField,
    DateTimeLocalField, IntegerField, HiddenField, TextAreaField, FloatField
)
from wtforms.validators import (
    InputRequired, Length, Email, EqualTo, AnyOf, NumberRange, Optional, ValidationError
)

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# -------- Auth --------
class LoginForm(FlaskForm):
    email_id = StringField("Email", validators=[InputRequired(), Email(), Length(max=100)])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    first_name = StringField("First name", validators=[InputRequired(), Length(max=100)])
    surname = StringField("Surname", validators=[InputRequired(), Length(max=100)])
    email_id = StringField("Email", validators=[InputRequired(), Email(), Length(max=100)])
    mobile_number = StringField("Contact number", validators=[InputRequired(), Length(min=8, max=15)])
    street_address = StringField("Street address", validators=[InputRequired(), Length(max=255)])
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6), EqualTo('confirm', message="Passwords should match")]
    )
    confirm  = PasswordField("Confirm Password")
    submit = SubmitField("Register")

# -------- Events --------
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

    home_team = StringField('Home Team', validators=[InputRequired(), Length(max=64)])
    away_team = StringField('Away Team', validators=[InputRequired(), Length(max=64)])

    start_datetime = DateTimeLocalField(
        'Start',
        format='%Y-%m-%dT%H:%M',
        validators=[InputRequired(message='Choose a start date & time')]
    )
    end_datetime = DateTimeLocalField(
        'End',
        format='%Y-%m-%dT%H:%M',
        validators=[InputRequired(message='Choose an end date & time')]
    )

    venue = StringField('Venue', validators=[InputRequired(), Length(max=128)])

    # Prevent negatives and silly values
    total_tickets = IntegerField(
        'Total Tickets',
        validators=[InputRequired(), NumberRange(min=1, max=50000, message="1–50,000 only")]
    )
    ticket_price  = FloatField(
        'Ticket Price (AUD)',
        validators=[InputRequired(), NumberRange(min=0, max=10000, message="Must be ≥ 0")]
    )

    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png/jpg/jpeg')
    ])
    description = TextAreaField('Event description', validators=[Optional(), Length(max=5000)])

    submit = SubmitField("Create Event")
    reset = SubmitField("Reset")

    # ---- Custom validators ----
    def validate_start_datetime(self, field):
        # Require start to be in the future (allow small grace period)
        now = datetime.now()
        if field.data is None:
            return
        if field.data <= now + timedelta(minutes=1):
            raise ValidationError("Start time must be in the future.")

    def validate_end_datetime(self, field):
        # Require end after start
        if field.data is None or self.start_datetime.data is None:
            return
        if field.data <= self.start_datetime.data:
            raise ValidationError("End time must be after the start time.")

# -------- Bookings --------
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

# -------- Comments --------
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired(), Length(max=400)])
    submit = SubmitField('Post Comment')
