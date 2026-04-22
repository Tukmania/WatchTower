from flask import Blueprint, request, jsonify
from app.services.event_service import log_event, undo_last_event, get_recent_events

events_bp = Blueprint('events', __name__)


@events_bp.route('/api/log', methods=['POST'])
def log_event_route():
    data = request.json
    result = log_event(
        event_type=data['event_type'],
        subtype=data.get('subtype', ''),
        location=data['location'],
        location_category=data['location_category']
    )
    return jsonify(result)


@events_bp.route('/api/undo', methods=['POST'])
def undo_last_route():
    result = undo_last_event()
    return jsonify(result)


@events_bp.route('/api/events/recent', methods=['GET'])
def recent_events_route():
    events = get_recent_events(limit=20)
    return jsonify(events)