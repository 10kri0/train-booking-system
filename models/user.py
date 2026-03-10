from datetime import datetime
from flask_login import UserMixin
from models import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    full_name     = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False, index=True)
    phone         = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to bookings
    bookings = db.relationship('Booking', backref='user', lazy=True,
                               cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'
