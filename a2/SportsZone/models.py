from datetime import datetime
from flask_login import UserMixin
from . import db

# -------------------- Users --------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    # allow formats like "0423 456 132" -> make longer than 10
    mobile_number = db.Column(db.String(20), unique=True, nullable=False)
    email_id = db.Column(db.String(100), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"

# -------------------- Venues --------------------
class Venue(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(128))
    venue_address = db.Column(db.String(256), nullable=True)
    capacity = db.Column(db.Integer)

    def __repr__(self):
        return f"<Venue {self.venue_name}>"

# -------------------- Events --------------------
class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    sports_type = db.Column(db.String(64), index=True)
    event_title = db.Column(db.String(256))
    home_team_name = db.Column(db.String(64))
    away_team_name = db.Column(db.String(64))
    event_image = db.Column(db.String(256))
    start_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    end_datetime = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='event', lazy=True)
    venue = db.relationship('Venue', backref='events')

    # ---------- properties used by your templates ----------
    @property
    def title(self):        # event.title
        return self.event_title or ""

    @property
    def sport(self):        # event.sport
        return self.sports_type or ""

    @property
    def image(self):        # event.image
        return self.event_image or ""

    @property
    def hero_image(self):   # event.hero_image
        return self.event_image or ""

    @property
    def start_text(self):   # event.start_text
        return self.start_datetime.strftime("%a, %b %d • %I:%M %p") if self.start_datetime else ""

    @property
    def end_text(self):     # event.end_text
        return self.end_datetime.strftime("%I:%M %p") if self.end_datetime else ""

    @property
    def status(self):       # event.status (latest from EventStatus)
        s = (EventStatus.query
             .filter_by(event_id=self.id)
             .order_by(EventStatus.event_status_date.desc())
             .first())
        return s.event_status if s else "Open"

    @property
    def badge(self):        # event.badge (Bootstrap color)
        return {"Open": "primary", "Sold Out": "danger",
                "Cancelled": "secondary", "Inactive": "warning"}.get(self.status, "secondary")

    @property
    def venue_text(self):   # "Name, Address"
        if not self.venue:
            return ""
        if self.venue.venue_address:
            return f"{self.venue.venue_name}, {self.venue.venue_address}"
        return self.venue.venue_name

    def __repr__(self):
        return f"<Event {self.event_title}>"

# -------------------- Statuses --------------------
class EventStatus(db.Model):
    __tablename__ = "eventStatus"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event_status = db.Column(db.String(32), index=True)
    event_status_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EventStatus {self.event_status}>"

# -------------------- Comments --------------------
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    text = db.Column(db.String(400))
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)

    # event.html uses "created_at"
    @property
    def created_at(self):
        return self.posted_date.strftime("%d %b, %H:%M")

    def __repr__(self):
        return f"<Comment {self.id}>"

# -------------------- Bookings / Tickets --------------------
class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    booking_quantity = db.Column(db.Integer)

    def __repr__(self):
        return f"<Booking {self.id}>"

class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    ticket_price = db.Column(db.Float, nullable=False)
    tickets_available = db.Column(db.Integer)

    def __repr__(self):
        return f"<Ticket {self.id}>"
