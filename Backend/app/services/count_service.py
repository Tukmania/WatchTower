from datetime import datetime
from app.extensions import db
from app.models.event import Event
from app.utils.time_helpers import get_time_block
from sqlalchemy import func, case


TERMINALS = [
    'TERMINAL 1A',
    'TERMINAL 1B',
    'TERMINAL 1C',
    'TERMINAL 1D',
    'MARINA'
]

SHOPS = [
    'LAOMAI JKIA',
    'LAOMAI MOMBASA',
    'CRAYSON PHARMACY JKIA',
    'CRAYSON PHARMACY KIAMBU ROAD',
    'CRAYSON PHARMACY MOMBASA'
]


def get_terminal_counts(shift_date):
    terminal_counts = {}
    for terminal in TERMINALS:
        rows = db.session.query(
            Event.subtype,
            func.count(Event.id).label('cnt')
        ).filter(
            Event.location == terminal,
            Event.shift_date == shift_date,
            Event.location_category == 'terminal'
        ).group_by(Event.subtype).all()

        terminal_counts[terminal] = {row.subtype: row.cnt for row in rows}

    return terminal_counts


def get_shop_counts(shift_date):
    shop_counts = {}
    for shop in SHOPS:
        rows = db.session.query(
            Event.event_type,
            func.count(Event.id).label('cnt')
        ).filter(
            Event.location == shop,
            Event.shift_date == shift_date,
            Event.location_category == 'shop'
        ).group_by(Event.event_type).all()

        shop_counts[shop] = {row.event_type: row.cnt for row in rows}

    return shop_counts


def get_summary(shift_date):
    result = db.session.query(
        func.sum(case((Event.subtype == 'bag_wrap', 1), else_=0)).label('bag_wraps'),
        func.sum(case((Event.subtype == 'box_wrap', 1), else_=0)).label('box_wraps'),
        func.sum(case((Event.subtype == 'foot_traffic', 1), else_=0)).label('foot_traffic'),
        func.sum(case((Event.event_type == 'interaction', 1), else_=0)).label('interactions'),
        func.sum(case((Event.event_type == 'walkin', 1), else_=0)).label('walkins'),
        func.sum(case((Event.event_type == 'receipt', 1), else_=0)).label('receipts')
    ).filter(Event.shift_date == shift_date).one()

    return {
        'bag_wraps':    result.bag_wraps or 0,
        'box_wraps':    result.box_wraps or 0,
        'foot_traffic': result.foot_traffic or 0,
        'interactions': result.interactions or 0,
        'walkins':      result.walkins or 0,
        'receipts':     result.receipts or 0
    }


def get_block_summary(shift_date, time_block):
    result = db.session.query(
        func.sum(case((Event.subtype == 'bag_wrap', 1), else_=0)).label('bag_wraps'),
        func.sum(case((Event.subtype == 'box_wrap', 1), else_=0)).label('box_wraps'),
        func.sum(case((Event.subtype == 'foot_traffic', 1), else_=0)).label('foot_traffic'),
        func.sum(case((Event.event_type == 'interaction', 1), else_=0)).label('interactions'),
        func.sum(case((Event.event_type == 'walkin', 1), else_=0)).label('walkins'),
        func.sum(case((Event.event_type == 'receipt', 1), else_=0)).label('receipts')
    ).filter(
        Event.shift_date == shift_date,
        Event.time_block == time_block
    ).one()

    return {
        'bag_wraps':    result.bag_wraps or 0,
        'box_wraps':    result.box_wraps or 0,
        'foot_traffic': result.foot_traffic or 0,
        'interactions': result.interactions or 0,
        'walkins':      result.walkins or 0,
        'receipts':     result.receipts or 0
    }


def get_trend(shift_date):
    rows = db.session.query(
        Event.time_block,
        func.sum(case((Event.subtype == 'bag_wrap', 1), else_=0)).label('bag_wraps'),
        func.sum(case((Event.subtype == 'box_wrap', 1), else_=0)).label('box_wraps'),
        func.sum(case((Event.subtype == 'foot_traffic', 1), else_=0)).label('foot_traffic')
    ).filter(
        Event.shift_date == shift_date
    ).group_by(Event.time_block).order_by(Event.time_block).all()

    return [
        {
            'time_block':   row.time_block,
            'bag_wraps':    row.bag_wraps or 0,
            'box_wraps':    row.box_wraps or 0,
            'foot_traffic': row.foot_traffic or 0
        }
        for row in rows
    ]