from flask import Blueprint, request, jsonify
from datetime import datetime
from app.services.count_service import (
    get_terminal_counts,
    get_shop_counts,
    get_summary,
    get_block_summary,
    get_trend,
    get_hourly_summary
)
from app.utils.time_helpers import get_time_block

counts_bp = Blueprint('counts', __name__)


@counts_bp.route('/api/counts', methods=['GET'])
def get_counts_route():
    shift_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    now = datetime.now()
    current_block = get_time_block(now)

    return jsonify({
        'terminals':     get_terminal_counts(shift_date),
        'shops':         get_shop_counts(shift_date),
        'summary':       get_summary(shift_date),
        'block_summary': get_block_summary(shift_date, current_block),
        'current_block': current_block
    })


@counts_bp.route('/api/counts/hourly', methods=['GET'])
def get_hourly_counts_route():
    shift_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    return jsonify(get_hourly_summary(shift_date))


@counts_bp.route('/api/events/trend', methods=['GET'])
def get_trend_route():
    shift_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    return jsonify(get_trend(shift_date))