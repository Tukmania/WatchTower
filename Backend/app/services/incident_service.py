from datetime import datetime
from app.extensions import db
from app.models.incident import Incident


def log_incident(shift, date, time, terminal, description):
    incident = Incident(
        shift=shift,
        date=date,
        time=time,
        terminal=terminal,
        description=description,
        created_at=datetime.now().isoformat()
    )
    db.session.add(incident)
    db.session.commit()
    return incident.to_dict()


def get_incidents(start=None, end=None):
    query = Incident.query.order_by(Incident.id.asc())
    if start and end:
        query = query.filter(
            Incident.created_at >= start,
            Incident.created_at <= end
        )
    return [i.to_dict() for i in query.all()]


def delete_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if incident:
        db.session.delete(incident)
        db.session.commit()
        return {'success': True}
    return {'success': False, 'message': 'Incident not found'}
