# website/views.py
import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import db
from .models import Event, Venue, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm

main_bp = Blueprint('main', __name__)

# ---------- Home (public) ----------
@main_bp.route('/', endpoint='index')
def index():
    # Toolbar filters
    cat = (request.args.get('category') or 'all').lower()
    st  = (request.args.get('status') or 'all').lower()
    q   = (request.args.get('q') or '').strip().lower()

    # Start query
    query = Event.query

    # Filter by category (sports type)
    if cat != 'all':
        query = query.filter(Event.sports_type.ilike(f"%{cat}%"))

    # Filter by status (case-insensitive)
    if st != 'all':
        if st == 'soldout':
            query = query.filter(Event.status.ilike('%sold out%'))
        else:
            query = query.filter(Event.status.ilike(f"%{st}%"))

    # Search by title, teams, or venue
    if q:
        query = query.join(Venue, isouter=True).filter(
            db.or_(
                Event.event_title.ilike(f"%{q}%"),
                Event.home_team_name.ilike(f"%{q}%"),
                Event.away_team_name.ilike(f"%{q}%"),
                Venue.venue_name.ilike(f"%{q}%")
            )
        )

    # Sort by start time
    events = query.order_by(Event.start_datetime.asc()).all()

    return render_template('index.html',
                           title="SportsZone | Home",
                           events=events)

# ---------- View a single event (public) ----------
@main_bp.route('/event/<int:event_id>', endpoint='view_event')
def view_event(event_id):
    e = Event.query.get_or_404(event_id)

    # Booking form
    booking_form = BookingForm()
    booking_form.event_id.data = e.id
    if getattr(booking_form, "quantity", None):
        booking_form.quantity.data = 1

    # Comment form
    comment_form = CommentForm()

    # Comments newest-first (model uses created_at)
    comments = (
        Comment.query
        .filter_by(event_id=e.id)
        .order_by(Comment.created_at.desc())
        .all()
    )

    page_title = e.event_title
    return render_template(
        "event.html",
        title=page_title,
        event=e,
        booking_form=booking_form,
        comment_form=comment_form,
        comments=comments,
    )

# ---------- Create event via WTForms + upload (login required) ----------
@main_bp.route('/create-event', methods=['GET', 'POST'])
@main_bp.route('/create-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def create_event(event_id=None):
    """Create a new event, or edit an existing one if event_id is given."""
    event = None
    if event_id:
        event = Event.query.get_or_404(event_id)
        if event.user_id != current_user.id:
            flash("You can only edit events you created.", "danger")
            return redirect(url_for('main.my_events'))

    # Prefill form if editing
    form = EventForm(obj=event) if event else EventForm()

    # Make venue text show the current venue name when editing
    if event and request.method == 'GET':
        form.venue.data = event.venue.venue_name if event.venue else ""
        form.home_team.data = event.home_team_name or ""
        form.away_team.data = event.away_team_name or ""
    if form.validate_on_submit():
        # Optional: save new image if uploaded
        filename = _save_upload(form)

        if not event:
            # ---------- CREATE ----------
            event = Event(
                user_id         = current_user.id,
                event_title     = form.event_title.data,
                sports_type     = form.sport_type.data,
                home_team_name  = form.home_team.data,
                away_team_name  = form.away_team.data,
                start_datetime  = form.start_datetime.data,
                end_datetime    = form.end_datetime.data,
                description     = form.description.data,
                total_tickets   = form.total_tickets.data,
                ticket_price    = form.ticket_price.data,
            )
            if filename:
                event.event_image = filename
            db.session.add(event)
        else:
            # ---------- UPDATE (like your teacher's example) ----------
            event.event_title     = form.event_title.data
            event.sports_type     = form.sport_type.data
            event.home_team_name  = form.home_team.data
            event.away_team_name  = form.away_team.data
            event.start_datetime  = form.start_datetime.data
            event.end_datetime    = form.end_datetime.data
            event.description     = form.description.data
            event.total_tickets   = form.total_tickets.data
            event.ticket_price    = form.ticket_price.data
            if filename:  # only replace if a new file was uploaded
                event.event_image = filename

        # Venue: find existing or create new
        venue_name = (form.venue.data or "").strip()
        if venue_name:
            v = Venue.query.filter_by(venue_name=venue_name).first()
            if not v:
                v = Venue(venue_name=venue_name)
                db.session.add(v)
                db.session.flush()
            event.venue_id = v.id

        db.session.commit()
        flash("Event updated successfully!" if event_id else "Event created successfully!", "success")
        return redirect(url_for('main.view_event', event_id=event.id))

    # Reuse the same template for both create and edit
    return render_template("create_event.html", form=form, event=event, title=("Edit Event" if event else "Create Event"))

#my events
@main_bp.route('/my-events', methods=['GET'], endpoint='my_events')
@login_required
def my_events():
    events = (
        Event.query
        .filter(Event.user_id == current_user.id)
        .order_by(Event.start_datetime.desc())
        .all()
    )
    return render_template('my_events.html', title="My Events", events=events)
# ---------- Booking history ----------
@main_bp.route('/booking', methods=['GET'], endpoint='booking')
@login_required
def booking():
    rows = (
        db.session.query(Booking, Event, Venue)
        .filter(Booking.user_id == current_user.id)
        .join(Event, Booking.event_id == Event.id, isouter=True)
        .join(Venue, Event.venue_id == Venue.id, isouter=True)
        .order_by(Booking.booking_date.desc())
        .all()
    )

    orders = []
    for b, e, v in rows:
        orders.append({
            "order_code": f"BK-{b.id}",
            "booked_at": b.booking_date.strftime("%d %b %Y, %I:%M %p") if b.booking_date else "",
            "quantity": b.booking_quantity or 1,
            "event_id": e.id if e else None,
            "event_title": (e.event_title or f"{e.home_team_name} vs {e.away_team_name}") if e else "Unknown Event",
            "image": e.event_image if e else None,
            "sport": e.sports_type if e else "",
        })

    return render_template('booking.html', title="Booking History", orders=orders)

# ---------- Create a booking ----------
@main_bp.route('/book', methods=['POST'], endpoint='create_booking')
@login_required
def create_booking():
    event_id = request.form.get('event_id', type=int)
    qty = request.form.get('quantity', default=1, type=int)

    if not event_id:
        flash("Missing event.", "danger")
        return redirect(url_for('main.index'))

    event = Event.query.get(event_id)
    if not event:
        flash("Event not found.", "warning")
        return redirect(url_for('main.index'))

    qty = max(1, min(qty, 10))  # align with form validator

    if not event.can_book(qty):
        flash("Not enough tickets or event closed.", "warning")
        return redirect(url_for('main.view_event', event_id=event.id))

    # create booking and apply counters
    booking = Booking(
        user_id=current_user.id,
        event_id=event.id,
        booking_quantity=qty
    )
    event.apply_booking(qty)

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

    from flask import current_app
    upload_dir = os.path.join(current_app.root_path, 'static', 'img')
    os.makedirs(upload_dir, exist_ok=True)

    try:
        fp.save(os.path.join(upload_dir, filename))
    except Exception:
        return None

    return filename

# ---------- Add a comment ----------
@main_bp.route('/event/<int:event_id>/comment', methods=["POST"])
@login_required
def add_comment(event_id):
    e = Event.query.get_or_404(event_id)
    form = CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(text=form.text.data, user_id=current_user.id, event_id=e.id))
        db.session.commit()
        flash("Comment added!", "success")
    else:
        flash("Error submitting comment.", "danger")
    return redirect(url_for("main.view_event", event_id=event_id))

@main_bp.route('/event/<int:event_id>/cancel', methods=['POST'], endpoint='cancel_event')
@login_required
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        flash("You can only cancel events you created.", "danger")
        return redirect(url_for('main.my_events'))
    event.status = "Cancelled"
    db.session.commit()
    flash("Event cancelled.", "info")
    return redirect(url_for('main.create_event', event_id=event.id))
