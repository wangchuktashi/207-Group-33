# website/models.py
from datetime import datetime
from flask_login import UserMixin
from . import db

# -------------------- Users --------------------
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id             = db.Column(db.Integer, primary_key=True)
    first_name     = db.Column(db.String(100), nullable=False)
    surname        = db.Column(db.String(100), nullable=False)
    email_id       = db.Column(db.String(100), unique=True, index=True, nullable=False)
    password_hash  = db.Column(db.String(255), nullable=False)
    mobile_number  = db.Column(db.String(15), unique=True, nullable=False)
    street_address = db.Column(db.String(255), nullable=False)

    comments = db.relationship("Comment", backref="user", lazy=True)
    bookings = db.relationship("Booking", backref="user", lazy=True)
    # If you want “event owner/creator”
    events_created = db.relationship(
        "Event",
        backref="creator",
        lazy=True,
        foreign_keys="Event.user_id",
    )

    def __repr__(self):
        return f"<User {self.first_name} {self.surname}>"

# -------------------- Venues --------------------
class Venue(db.Model):
    __tablename__ = "venues"

    id            = db.Column(db.Integer, primary_key=True)
    venue_name    = db.Column(db.String(128), nullable=False)
    venue_address = db.Column(db.String(256))
    capacity      = db.Column(db.Integer)

    events = db.relationship("Event", backref="venue", lazy=True)

    def __repr__(self):
        return f"<Venue {self.venue_name}>"

# -------------------- Events --------------------
class Event(db.Model):
    __tablename__ = "events"
<<<<<<< HEAD
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
=======
>>>>>>> 5bb00b266d03f599965e62d7995c6314eb4aedc0

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey("users.id"))      # creator/owner (optional)
    venue_id        = db.Column(db.Integer, db.ForeignKey("venues.id"))

    # Core info
    sports_type     = db.Column(db.String(64), index=True)                  # Football, Basketball, etc.
    event_title     = db.Column(db.String(256), nullable=False)
    home_team_name  = db.Column(db.String(64))
    away_team_name  = db.Column(db.String(64))
    event_image     = db.Column(db.String(256))                             # filename in /static/img
    description     = db.Column(db.Text)

    # Timing
    start_datetime  = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_datetime    = db.Column(db.DateTime)

    # Booking controls
    status          = db.Column(db.String(32), index=True, default="Open", nullable=False)
    total_tickets   = db.Column(db.Integer, default=120, nullable=False)
    tickets_sold    = db.Column(db.Integer, default=0,  nullable=False)
    ticket_price    = db.Column(db.Float,   default=0.0, nullable=False)

    comments = db.relationship("Comment", backref="event", lazy=True, cascade="all, delete-orphan")
    bookings = db.relationship("Booking", backref="event", lazy=True, cascade="all, delete-orphan")

    # ---- Helpers ----
    def remaining_tickets(self) -> int:
        return max(0, (self.total_tickets or 0) - (self.tickets_sold or 0))

    def can_book(self, qty: int) -> bool:
        if self.status != "Open":
            return False
        if qty is None or qty <= 0:
            return False
        return self.remaining_tickets() >= qty

    def apply_booking(self, qty: int) -> None:
        """Adjust counters and status. Call before commit, after can_book()."""
        self.tickets_sold = (self.tickets_sold or 0) + qty
        if self.remaining_tickets() <= 0:
            self.status = "Sold Out"

    @property
    def venue_text(self) -> str:
        if self.venue:
            parts = [self.venue.venue_name, self.venue.venue_address]
            return " - ".join([p for p in parts if p])
        return ""

    def __repr__(self):
        return f"<Event {self.event_title}>"

# -------------------- Comments --------------------
class Comment(db.Model):
    __tablename__ = "comments"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id   = db.Column(db.Integer, db.ForeignKey("events.id"))
    text       = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Comment {self.id}>"

# -------------------- Bookings --------------------
class Booking(db.Model):
    __tablename__ = "bookings"

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id         = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    booking_date     = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    booking_quantity = db.Column(db.Integer, nullable=False)
    order_code       = db.Column(db.String(32), index=True)  # e.g. "BK-123" after insert

    def __repr__(self):
        return f"<Booking {self.id} x{self.booking_quantity}>"
