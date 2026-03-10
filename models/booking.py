from datetime import datetime
from models import db


class Booking(db.Model):
    __tablename__ = 'bookings'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'),
                             nullable=False, index=True)
    train_id     = db.Column(db.Integer, db.ForeignKey('trains.id', ondelete='CASCADE'),
                             nullable=False, index=True)
    seat_count   = db.Column(db.Integer, nullable=False)
    total_fare   = db.Column(db.Numeric(10, 2), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Booking #{self.id} user={self.user_id} train={self.train_id}>'
