from datetime import datetime
from models import db


class Admin(db.Model):
    __tablename__ = 'admins'

    id            = db.Column(db.Integer, primary_key=True)
    full_name     = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Admin {self.email}>'
