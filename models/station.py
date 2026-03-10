from models import db


class Station(db.Model):
    __tablename__ = 'stations'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Station {self.name}, {self.city}>'
