from flask import Blueprint, request, send_file, jsonify
from datetime import datetime, timedelta
from app.models.event    import Event
from app.models.incident import Incident
from app.services.report_service import generate_excel_report

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/api/report', methods=['GET'])
def download_report():
    start_str = request.args.get('start')  # "2026-04-26T18:00"
    end_str   = request.args.get('end')    # "2026-04-27T07:00"

    if not start_str or not end_str:
        return jsonify({'error': 'start and end parameters are required'}), 400

    try:
        start_dt = datetime.strptime(start_str, '%Y-%m-%dT%H:%M')
        end_dt   = datetime.strptime(end_str,   '%Y-%m-%dT%H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid datetime format. Use YYYY-MM-DDTHH:MM'}), 400

    if end_dt <= start_dt:
        return jsonify({'error': 'End time must be after start time'}), 400

    # Include all events within [start, end) — end minute is exclusive so we add 1 min
    end_dt_exclusive = end_dt + timedelta(minutes=1)

    start_ts = start_dt.strftime('%Y-%m-%d %H:%M:%S')
    end_ts   = end_dt_exclusive.strftime('%Y-%m-%d %H:%M:%S')

    events = Event.query.filter(
        Event.timestamp >= start_ts,
        Event.timestamp <  end_ts
    ).order_by(Event.timestamp).all()

    events_list = [e.to_dict() for e in events]

    # Incidents logged (by created_at) within the same window
    incidents = Incident.query.filter(
        Incident.created_at >= start_dt.isoformat(),
        Incident.created_at <  end_dt_exclusive.isoformat()
    ).order_by(Incident.id.asc()).all()

    incidents_list = [i.to_dict() for i in incidents]

    # Human-readable label for the Excel header
    label = (
        f"{start_dt.strftime('%d/%m/%Y %H:%M')} – "
        f"{end_dt.strftime('%d/%m/%Y %H:%M')}"
    )

    # Safe filename suffix
    filename_base = (
        f"{start_dt.strftime('%Y%m%d_%H%M')}"
        f"_to_{end_dt.strftime('%Y%m%d_%H%M')}"
    )

    filepath = generate_excel_report(events_list, label, filename_base, incidents_list)

    return send_file(
        filepath,
        as_attachment=True,
        download_name=f'CCTV_Report_{filename_base}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )