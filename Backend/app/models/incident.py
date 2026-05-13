from app.extensions import db
from datetime import datetime


class Incident(db.Model):
    __tablename__ = 'incidents'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shift       = db.Column(db.String(20),  nullable=False)   # DAYSHIFT / NIGHTSHIFT
    date        = db.Column(db.String(20),  nullable=False)   # DD/MM/YYYY
    time        = db.Column(db.String(60),  nullable=False)   # free text e.g. "1620HRS"
    terminal    = db.Column(db.String(100), nullable=False)   # location / terminal name
    description = db.Column(db.Text,        nullable=False)   # full incident narrative
    created_at  = db.Column(db.String(30),  nullable=False)   # ISO timestamp (for report filtering)

    def to_dict(self):
        return {
            'id':          self.id,
            'shift':       self.shift,
            'date':        self.date,
            'time':        self.time,
            'terminal':    self.terminal,
            'description': self.description,
            'created_at':  self.created_at
        }

    def __repr__(self):
        return f'<Incident {self.id} | {self.shift} | {self.terminal} | {self.date}>'
