from . import db
from datetime import datetime
from flask_login import UserMixin

# user related data
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    # assume mobile numbers with format such as 0423 456 132
    mobile_number = db.Column(db.String(10), unique=True, nullable=False)
    email_id = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')               # relation to call user.comments and comment.created_by
    
    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

# sports event related data 
class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))          # relationship to event
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))        # relationship to venue
    sports_type = db.Column(db.String(64), unique=True, index=True)
    event_title = db.Column(db.String(256))
    home_team_name = db.Column(db.String(64))
    away_team_name = db.Column(db.String(64))
    event_image = db.Column(db.String(64))
    start_datetime = db.Column(db.DateTime, default=datetime.now())
    end_datetime = db.Column(db.DateTime, default=datetime.now())
    comments = db.relationship('Comment', backref='event')              # relation to call event.comments and comment.event

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

# event status data
class EventStatus(db.Model):
    __tablename__ = "eventStatus"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))        # relationship to event
    event_status = db.Column(db.String(32), index=True)
    event_status_date = db.Column(db.DateTime, default=datetime.now())

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

# venue related data
class Venue(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(128))
    venue_address = db.Column(db.String(256), nullable=True)
    capacity = db.Column(db.Integer)

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"
    
# user comment data
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))          # relationship to user
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    text = db.Column(db.String(400))
    posted_date = db.Column(db.DateTime, default=datetime.now()) 

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"

# booking data
class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))          # relationship to user
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    booking_date = db.Column(db.DateTime, default=datetime.now())
    booking_quantity = db.Column(db.Integer)

    # string print method
    def __repr__(self):
        return f"Booking: {self.integer}"

# ticket data
class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))    # relationship to booking
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))        # relationship to event
    ticket_price = db.Column(db.Float, nullable=False)  
    tickets_available = db.Column(db.Integer)

    # string print method
    def __repr__(self):
        return f"Ticket: {self.integer}"