from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment  # plain Python classes (no DB)

# All templates use 'main.*' endpoints
mainbp = Blueprint('main', __name__)

# ---------- sample data (in-memory) ----------
def _sample_events():
    e1 = Event(
        id=1,
        title="England vs Spain",
        sport="Football",
        venue="Wembley Stadium, London",
        start_text="Sat, Oct 18 • 7:30 PM",
        end_text="9:30 PM",
        image="ft1.jpg",
        hero_image="engvsspain.jpg",
        description="UEFA Euro 2025 Qualifier — witness England take on Spain under the lights.",
        status="Open",
    )
    e1.add_comment(Comment("Jake", "Is there on-site parking at Wembley?", "12 Oct, 07:50"))
    e1.add_comment(Comment("Tom", "Is Foden playing?", "10 Oct, 18:05"))

    e2 = Event(
        id=2,
        title="Miami Heats vs Brooklyn Nets",
        sport="Basketball",
        venue="Kaseya Center, Miami",
        start_text="Sun, Oct 20 • 6:00 PM",
        end_text="8:00 PM",
        image="basketball1.jpg",
        hero_image="basketball1.jpg",
        description="NBA preseason face-off with fast breaks and big plays.",
        status="Sold Out",
    )

    e3 = Event(
        id=3,
        title="Australia vs India",
        sport="Cricket",
        venue="MCG, Melbourne",
        start_text="Sun, Nov 9 • 7:00 PM",
        end_text="10:00 PM",
        image="cricket1.jpg",
        hero_image="cricket1.jpg",
        description="ICC Finals — Australia battles India for ultimate cricket glory.",
        status="Open",
    )

    return [e1, e2, e3]

def list_events():
    return _sample_events()

def get_event(event_id: int):
    return next((e for e in _sample_events() if e.id == event_id), None)

# ---------- routes ----------
@mainbp.route('/', endpoint='index')
def index():
    events = list_events()
    return render_template('index.html', title="SportsZone | Home", events=events)

@mainbp.route('/event/<int:event_id>', endpoint='view_event')
def view_event(event_id):
    event = get_event(event_id)
    if not event:
        abort(404)
    return render_template('event.html', title=event.title, event=event)

@mainbp.route('/create-event', methods=['GET', 'POST'], endpoint='create_event')
def create_event():
    if request.method == 'POST':
        flash('Event saved (demo).')
        return redirect(url_for('main.index'))
    return render_template('create_event.html', title="Create Event")

@mainbp.route('/booking', endpoint='booking')
def booking():
    # optional: pass dummy orders later if you want
    return render_template('booking.html', title="Booking History")

# (optional) placeholders so navbar items don’t 404 if you keep auth links later
@mainbp.route('/login', endpoint='login')
def login():
    return "<h1>Login - coming soon</h1>"

@mainbp.route('/register', endpoint='register')
def register():
    return "<h1>Register - coming soon</h1>"

@mainbp.route('/logout', endpoint='logout')
def logout():
    return redirect(url_for('main.index'))