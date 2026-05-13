from flask import Blueprint, request, jsonify
from app.services.incident_service import log_incident, get_incidents, delete_incident

incidents_bp = Blueprint('incidents', __name__)


@incidents_bp.route('/api/incidents', methods=['POST'])
def log_incident_route():
    data = request.json
    required = ('shift', 'date', 'time', 'terminal', 'description')
    if not data or not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    result = log_incident(
        shift=data['shift'],
        date=data['date'],
        time=data['time'],
        terminal=data['terminal'],
        description=data['description']
    )
    return jsonify(result), 201


@incidents_bp.route('/api/incidents', methods=['GET'])
def get_incidents_route():
    start = request.args.get('start')
    end   = request.args.get('end')
    return jsonify(get_incidents(start, end))


@incidents_bp.route('/api/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident_route(incident_id):
    result = delete_incident(incident_id)
    status = 200 if result['success'] else 404
    return jsonify(result), status
