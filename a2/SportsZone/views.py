# website/views.py
import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import db
from .models import Event, EventStatus, Venue, Comment, Booking # (Comment is here if you add posting later)
from .forms import EventForm, CommentForm , BookingForm               # EventForm is used below

main_bp = Blueprint('main', __name__)

# ---------- Home (public) ----------
@main_bp.route('/', endpoint='index')
def index():
    # optional filters used by your toolbar
    cat = (request.args.get('category') or 'all').lower()
    st  = (request.args.get('status') or 'all').lower()
    q   = (request.args.get('q') or '').strip().lower()

    query = Event.query
    if cat != 'all':
        query = query.filter(Event.sports_type.ilike(cat))

    events = query.order_by(Event.start_datetime.asc()).all()

    # Apply status + search filters using the properties
    def ok(e: Event) -> bool:
        if st != 'all' and e.status.lower() != st:
            return False
        if q:
            hay = f"{e.title} {e.sport} {e.venue_text}".lower()
            if q not in hay:
                return False
        return True

    events = [e for e in events if ok(e)]
    return render_template('index.html', title="SportsZone | Home", events=events)

# ---------- View a single event (public) ----------
@main_bp.route('/event/<int:event_id>', endpoint='view_event')
def view_event(event_id):
    e = Event.query.get_or_404(event_id)

    form = BookingForm()
    form.event_id.data = e.id  # pre-fill hidden field
    form.quantity.data = 1     # default

    return render_template('event.html', title=e.title, event=e, form=form)
# ---------- Create event via WTForms + upload (login required) ----------
@main_bp.route('/create-event', methods=['GET', 'POST'], endpoint='create_event')
@login_required
def create_event():
    form = EventForm()

    # If user clicked reset, just reload the form
    if form.reset.data:
        return redirect(url_for('main.create_event'))

    if form.validate_on_submit() and form.submit.data:
        # save upload (returns filename or None)
        filename = _save_upload(form)

        # ensure venue exists (model stores venue_id)
        venue_name = (form.venue.data or "").strip()
        venue = None
        if venue_name:
            venue = Venue.query.filter_by(venue_name=venue_name).first()
            if not venue:
                venue = Venue(venue_name=venue_name)
                db.session.add(venue)
                db.session.flush()  # get id

        # map form fields to Event model columns
        event = Event(
            sports_type      = form.sport_type.data,
            event_title      = form.event_title.data,
            home_team_name   = form.home_team.data,
            away_team_name   = form.away_team.data,
            start_datetime   = form.start_datetime.data,
            end_datetime     = form.end_datetime.data,
            event_image      = filename or ""
        )
        if venue:
            event.venue = venue  # sets venue_id via relationship

        db.session.add(event)
        db.session.flush()
        db.session.add(EventStatus(event_id=event.id, event_status="Open"))
        db.session.commit()

        # After a successful create, you can redirect back to the form or to the new event
        return redirect(url_for('main.view_event', event_id=event.id))

    return render_template('create_event.html', form=form, title="Create Event")

# ---------- Booking page (leave as-is) ----------
@main_bp.route('/booking', methods=['GET'], endpoint='booking')
@login_required
def booking():
    # join Bookings -> Event -> Venue so we can display some details
    rows = (
        db.session.query(Booking, Event, Venue)
        .filter(Booking.user_id == current_user.id)
        .join(Event, Booking.event_id == Event.id, isouter=True)
        .join(Venue, Event.venue_id == Venue.id, isouter=True)
        .order_by(Booking.booking_date.desc())
        .all()
    )

    bookings = []
    for b, e, v in rows:
        bookings.append({
            "id": b.id,
            "date": (
                b.booking_date.strftime("%d %b %Y, %I:%M %p")
                if b.booking_date else ""
            ),
            "qty": b.booking_quantity or 1,
            "event": {
                "id": e.id if e else None,
                "title": (
                    e.event_title
                    or f"{e.home_team_name} vs {e.away_team_name}"
                ) if e else "Unknown Event",
                "start_text": getattr(e, "start_text", ""),   # safe fallback
                "end_text": getattr(e, "end_text", ""),
                "venue_text": getattr(e, "venue_text", v.venue_name if v else ""),
                "image": e.event_image if e else None
            }
        })

    return render_template(
        'booking.html',
        title="Booking History",
        bookings=bookings
    )


# =========================
# CREATE A BOOKING (requires login)
# called via POST (e.g. "Book Now" button on event page)
# =========================
@main_bp.route('/book', methods=['POST'], endpoint='create_booking')
@login_required
def create_booking():
    form = BookingForm()
    if not form.validate_on_submit():
        flash("Invalid booking submission.", "danger")
        return redirect(url_for('main.index'))

    event_id = int(form.event_id.data)
    qty = int(form.quantity.data)

    event = Event.query.get(event_id)
    if not event:
        flash("Event not found.", "warning")
        return redirect(url_for('main.index'))

    booking = Booking(
        user_id=current_user.id,
        event_id=event.id,
        booking_quantity=qty
    )
    db.session.add(booking)
    db.session.commit()

    flash("Your booking was created!", "success")
    return redirect(url_for('main.booking'))

# ---------- helper: save upload to static/img and return filename ----------
def _save_upload(form):
    file_field = getattr(form, 'image', None)
    if not file_field or not file_field.data:
        return None

    fp = file_field.data
    filename = secure_filename(getattr(fp, 'filename', '') or '')
    if not filename:
        return None

    # Save into your app's static/img directory
    from flask import current_app
    upload_dir = os.path.join(current_app.root_path, 'static', 'img')
    os.makedirs(upload_dir, exist_ok=True)

    try:
        fp.save(os.path.join(upload_dir, filename))
    except Exception:
        # Keep it simple per your request: on error, just skip storing a file
        return None

    # store only the filename in DB
    return filename
