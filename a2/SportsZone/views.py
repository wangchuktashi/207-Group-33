from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
#Login + password 
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Event, EventStatus, Venue, Comment, Booking, User  


mainbp = Blueprint('main', __name__)

@mainbp.route('/', endpoint='index')
def index():
    cat = (request.args.get('category') or 'all').lower()
    st  = (request.args.get('status') or 'all').lower()
    q   = (request.args.get('q') or '').strip().lower()

    query = Event.query
    if cat != 'all':
        query = query.filter(Event.sports_type.ilike(cat))

    events = query.order_by(Event.start_datetime.asc()).all()

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

@mainbp.route('/event/<int:event_id>', endpoint='view_event')
def view_event(event_id):
    e = Event.query.get_or_404(event_id)
    return render_template('event.html', title=e.title, event=e)

@mainbp.route('/create-event', methods=['GET', 'POST'], endpoint='create_event')
def create_event():
    if request.method == 'POST':
        f = request.form

        # upsert venue quickly
        vname = (f.get('venue') or '').strip()
        venue = Venue.query.filter_by(venue_name=vname).first()
        if not venue:
            venue = Venue(venue_name=vname, capacity=int(f.get('tickets') or 0))
            db.session.add(venue)
            db.session.flush()

        def parse_dt(val):
            try:    return datetime.strptime(val, "%Y-%m-%dT%H:%M")
            except: return None

        e = Event(
            venue_id=venue.id if venue else None,
            sports_type=f.get('sport'),
            event_title=f.get('title'),
            home_team_name=f.get('home'),
            away_team_name=f.get('away'),
            event_image=f.get('image') or "",
            start_datetime=parse_dt(f.get('start')),
            end_datetime=parse_dt(f.get('end')),
        )
        db.session.add(e)
        db.session.flush()
        db.session.add(EventStatus(event_id=e.id, event_status="Open"))
        db.session.commit()

        flash('Event saved.', 'success')
        return redirect(url_for('main.view_event', event_id=e.id))

    return render_template('create_event.html', title="Create Event")


@mainbp.route('/event/<int:event_id>', endpoint='event_detail')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event.html', event=event, title=event.event_title or event.home_team_name)

# ----------------------------------------------------------
# BOOKING HISTORY (Temporarily no login required for testing)
# ----------------------------------------------------------
@mainbp.route('/booking', methods=['GET'], endpoint='booking')
# @login_required  # Disabled login requirement to test booking history without logging in
def booking():
    rows = (db.session.query(Booking, Event, Venue)
            # Commented filter below if you want to see ALL bookings
            # .filter(Booking.user_id == current_user.id)
            .join(Event, Booking.event_id == Event.id, isouter=True)
            .join(Venue, Event.venue_id == Venue.id, isouter=True)
            .order_by(Booking.booking_date.desc())
            .all())
    bookings = []
    for b, e, v in rows:
        bookings.append({
            "id": b.id,
            "date": b.booking_date.strftime("%d %b %Y, %I:%M %p") if b.booking_date else "",
            "qty": b.booking_quantity or 1,
            "event": {
                "id": e.id if e else None,
                "title": (e.event_title or f"{e.home_team_name} vs {e.away_team_name}") if e else "Unknown Event",
                "start_text": e.start_text if e else "",
                "end_text": e.end_text if e else "",
                "venue_text": e.venue_text if e else (v.venue_name if v else ""),
                "image": e.event_image if e else None
            }
        })
    return render_template('booking.html', title="Booking History", bookings=bookings)


# ---------------------------------
# LOGIN / LOGOUT (kept unchanged)
# ---------------------------------
@mainbp.route('/login', methods=['GET','POST'], endpoint='login')
def login():
    from .forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.user_name.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            next_url = request.args.get('next') or url_for('main.index')
            return redirect(next_url)
        flash("Invalid username or password.", "danger")
    return render_template('login.html', form=form, title="Login")

@mainbp.route('/register', endpoint='register')
def register():
    return "<h1>Register - coming soon</h1>"

@mainbp.route('/logout', endpoint='logout')
@login_required 
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.index'))


# --------------------------------------------------
#  no login for testing
# --------------------------------------------------
@mainbp.route('/book', methods=['POST'], endpoint='create_booking')
# @login_required  # Disabled login for testing
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
    qty = max(1, min(qty, 50000)) 
    booking = Booking(event_id=event.id, booking_quantity=qty)
    db.session.add(booking)
    db.session.commit()
    flash("Your booking was created!", "success")
    return redirect(url_for('main.booking'))
# --------------------------------------------------
# no login for testing
# --------------------------------------------------
@mainbp.route('/delete-booking/<int:booking_id>', methods=['POST'], endpoint='delete_booking')
# @login_required  #  Disabled login requirement for testing
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash(f"Booking ID BK-{booking_id} deleted successfully.", "info")
    return redirect(url_for('main.booking'))

