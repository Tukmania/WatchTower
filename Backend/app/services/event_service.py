from datetime import datetime
from app.extensions import db
from app.models.event import Event
from app.utils.time_helpers import get_time_block


def log_event(event_type, subtype, location, location_category):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    time_block = get_time_block(now)
    shift_date = now.strftime('%Y-%m-%d')

    event = Event(
        event_type=event_type,
        subtype=subtype or '',
        location=location,
        location_category=location_category,
        timestamp=timestamp,
        time_block=time_block,
        shift_date=shift_date
    )

    db.session.add(event)
    db.session.commit()

    return event.to_dict()


def undo_last_event():
    event = Event.query.order_by(Event.id.desc()).first()
    if event:
        event_dict = event.to_dict()
        db.session.delete(event)
        db.session.commit()
        return {'success': True, 'undone': event_dict}
    return {'success': False, 'message': 'No events to undo'}


def get_recent_events(limit=20):
    events = Event.query.order_by(Event.id.desc()).limit(limit).all()
    return [e.to_dict() for e in events]