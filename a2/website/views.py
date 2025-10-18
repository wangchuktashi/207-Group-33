from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Event, EventStatus, Venue, Comment

mainbp = Blueprint('main', __name__)

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


@mainbp.route('/booking', endpoint='booking')
def booking():
    return render_template('booking.html', title="Booking History")

#@mainbp.route('/login', endpoint='login')
#def login():
   # return "<h1>Login - coming soon</h1>"

#@mainbp.route('/register', endpoint='register')
#def register():
  #  return "<h1>Register - coming soon</h1>"

#@mainbp.route('/logout', endpoint='logout')
#def logout():
 #   return redirect(url_for('main.index'))
