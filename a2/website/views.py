from flask import Blueprint, render_template, request, redirect, url_for, flash

# All templates use 'main.*' endpoints
mainbp = Blueprint('main', __name__)

@mainbp.route('/', endpoint='index')
def index():
    return render_template('index.html', title="SportsZone | Home")

@mainbp.route('/create-event', methods=['GET', 'POST'], endpoint='create_event')
def create_event():
    if request.method == 'POST':
        # save form here (demo only)
        flash('Event saved (demo).')
        return redirect(url_for('main.index'))
    return render_template('create_event.html', title="Create Event")

@mainbp.route('/booking', endpoint='booking')
def booking():
    return render_template('booking.html', title="Booking History")

@mainbp.route('/event/<int:event_id>', endpoint='view_event')
def view_event(event_id):
    # you can fetch event by id here
    return render_template('event.html', event_id=event_id, title=f"Event #{event_id}")

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
