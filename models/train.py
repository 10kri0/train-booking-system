from datetime import datetime
from models import db


class Train(db.Model):
    __tablename__ = 'trains'

    id              = db.Column(db.Integer, primary_key=True)
    train_name      = db.Column(db.String(150), nullable=False)
    source          = db.Column(db.String(100), nullable=False, index=True)
    destination     = db.Column(db.String(100), nullable=False, index=True)
    departure_time  = db.Column(db.String(10), nullable=False)   # stored as "HH:MM"
    arrival_time    = db.Column(db.String(10), nullable=False)
    total_seats     = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    fare            = db.Column(db.Numeric(10, 2), nullable=False)
    status          = db.Column(db.Enum('active', 'cancelled'), default='active', nullable=False)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow,
                                onupdate=datetime.utcnow)

    # Relationship to bookings
    bookings = db.relationship('Booking', backref='train', lazy=True)

    def __repr__(self):
        return f'<Train {self.train_name} {self.source}→{self.destination}>'
