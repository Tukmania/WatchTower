from flask import Blueprint, request, send_file
from datetime import datetime
from app.models.event import Event
from app.services.report_service import generate_excel_report

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/api/report', methods=['GET'])
def download_report():
    shift_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    events = Event.query.filter_by(
        shift_date=shift_date
    ).order_by(Event.timestamp).all()

    events_list = [e.to_dict() for e in events]
    filepath = generate_excel_report(events_list, shift_date)

    return send_file(
        filepath,
        as_attachment=True,
        download_name=f'CCTV_Report_{shift_date}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )