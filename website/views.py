from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from .forms import BookingForm, EventForm
from . import db
from .models import Event, Booking

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = Event.query.all()  
    return render_template('Index.html', events=events)

@main_bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    form = BookingForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You must log in to book tickets.", "warning")
            return redirect(url_for('login'))

        qty = form.quantity.data
        if qty > event.tickets:
            flash("Not enough tickets available.", "danger")
        else:
            event.tickets -= qty
            booking = Booking(quantity=qty, user_id=current_user.id, event_id=event.id)
            db.session.add(booking)
            db.session.commit()
            flash("Booking successful!", "success")
            return redirect(url_for('booking_history'))

    return render_template('event.html', event=event, form=form)


@main_bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            category=form.category.data,
            description=form.description.data,
            venue=form.venue.data,
            date=form.date.data,
            tickets=form.tickets.data,
            image=form.image.data,
            creator_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for('index'))
    return render_template('create_event.html', form=form)


@main_bp.route('/booking-history')
@login_required
def booking_history():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('booking.html', bookings=bookings)
