from app.extensions import db
from datetime import datetime


class Event(db.Model):
    __tablename__ = 'events'

    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_type        = db.Column(db.String(50), nullable=False)
    subtype           = db.Column(db.String(50), nullable=True)
    location          = db.Column(db.String(100), nullable=False)
    location_category = db.Column(db.String(20), nullable=False)  # 'terminal' or 'shop'
    timestamp         = db.Column(db.String(30), nullable=False)
    time_block        = db.Column(db.String(20), nullable=False)
    shift_date        = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id':                self.id,
            'event_type':        self.event_type,
            'subtype':           self.subtype,
            'location':          self.location,
            'location_category': self.location_category,
            'timestamp':         self.timestamp,
            'time_block':        self.time_block,
            'shift_date':        self.shift_date
        }

    def __repr__(self):
        return f'<Event {self.id} | {self.event_type} | {self.location} | {self.timestamp}>'