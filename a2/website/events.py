from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, Comment, Venue
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename

event_bp = Blueprint('event', __name__, url_prefix='/create-event')

# @event_bp.route('/create-event', methods=['GET', 'POST'])
@event_bp.route('/<int:event_id>', endpoint='view_event')
def view_event(event_id):
    e = Event.query.get_or_404(event_id)

    return render_template('event.html', title=e.title, event=e)

@event_bp.route('/', methods=['GET', 'POST'], endpoint='create_event')
def create_event():
    print('Method type: ', request.method)
    form = EventForm()

    # if user clicked reset
    if form.reset.data:
        return redirect(url_for('event.create_event'))
    
    if form.validate_on_submit() and form.submit.data:
        # save upload and get DB path
        db_file_path = check_upload_file(form)

        # ensure venue exists (model stores venue_id)
        venue_name = (form.venue.data or "").strip()
        venue = None
        if venue_name:
            venue = Venue.query.filter_by(venue_name=venue_name).first()
            if not venue:
                venue = Venue(venue_name=venue_name)
                db.session.add(venue)
                db.session.flush()   # assign id without committing

        # map form fields to Event model columns (use actual column names)
        event = Event(
            sports_type = form.sport_type.data,
            event_title = form.event_title.data,
            home_team_name = form.home_team.data,
            away_team_name = form.away_team.data,
            start_datetime = form.start_datetime.data,
            end_datetime = form.end_datetime.data,
            event_image = db_file_path
        )
        if venue:
            event.venue = venue   # sets venue_id via relationship

        # add the object to the db session
        db.session.add(event)
        db.session.commit()
        print('Successfully created new event', 'success')
        # Always end with redirect when form is valid
        return redirect(url_for('event.create_event'))
    
    return render_template('create_event.html', form=form)

def check_upload_file(form):
    file_field = getattr(form, 'image', None)
    if not file_field:
        return None
    fp = file_field.data
    if not fp:
        return None
    filename = secure_filename(getattr(fp, 'filename', '') or '')
    if not filename:
        return None

    base_dir = os.path.dirname(__file__)
    upload_dir = os.path.join(base_dir, 'static', 'img')
    os.makedirs(upload_dir, exist_ok=True)

    upload_path = os.path.join(upload_dir, filename)
    try:
        fp.save(upload_path)
    except Exception as e:
        print("Error saving upload:", e)
        return None

    # return only the filename for storage
    return filename

