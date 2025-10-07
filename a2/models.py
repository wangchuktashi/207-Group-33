from . import db
from datetime import datetime
from flask_login import UserMixin

# user related data
class User(db.Model, UserMixin):
    pass

# sports event related data 
class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    # user id (FK)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    sports_type = db.Column(db.String(64), unique=True, index=True)
    event_title = db.Column(db.String(256))
    home_team_name = db.Column(db.String(64))
    away_team_name = db.Column(db.String(64))
    event_image = db.Column(db.String(64))
    start_datetime = db.Column(db.DateTime, default=datetime.now())
    end_datetime = db.Column(db.DateTime, default=datetime.now())

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

# event status data
class EventStatus(db.Model):
    __tablename__ = "eventStatus"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event_status = db.Column(db.String(32), index=True)
    event_status_date = db.Column(db.DateTime, default=datetime.now())

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

# venue related data
class Venue(db.Model):
    __tablename__ = "venue"
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(128))
    venue_address = db.Column(db.String(256), nullable=True)
    capacity = db.Column(db.Integer)

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"
    
# user comment data
class Comment(db.Model):
    pass

# booking & ticket data
class Booking(db.Model):
    pass