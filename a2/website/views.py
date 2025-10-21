# website/views.py
import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from . import db
from .models import Event, EventStatus, Venue, Comment  # (Comment is here if you add posting later)
from .forms import EventForm, CommentForm                # EventForm is used below

mainbp = Blueprint('main', __name__)

# ---------- Home (public) ----------
@mainbp.route('/', endpoint='index')
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
@mainbp.route('/event/<int:event_id>', endpoint='view_event')
def view_event(event_id):
    e = Event.query.get_or_404(event_id)
    return render_template('event.html', title=e.title, event=e)

# ---------- Create event via WTForms + upload (login required) ----------
@mainbp.route('/create-event', methods=['GET', 'POST'], endpoint='create_event')
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
@mainbp.route('/booking', endpoint='booking')
@login_required
def booking():
    return render_template('booking.html', title="Booking History")

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
