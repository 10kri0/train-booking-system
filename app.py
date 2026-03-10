from flask import Flask
from flask_login import LoginManager

from config import Config
from models import db
from models.user import User
from models.admin import Admin
from models.train import Train
from models.booking import Booking
from models.station import Station

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # Register blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Create tables and seed data
    with app.app_context():
        db.create_all()
        _seed_data()

    # Custom error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        from flask import render_template
        return render_template('errors/500.html'), 500

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def _seed_data():
    """Seed default admin and sample trains on first run."""
    from werkzeug.security import generate_password_hash

    # Seed default admin
    if not Admin.query.filter_by(email='admin@trainbooking.com').first():
        admin = Admin(
            full_name='System Admin',
            email='admin@trainbooking.com',
            password_hash=generate_password_hash('Admin@123')
        )
        db.session.add(admin)

    # Seed stations
    stations_data = [
        ('Delhi', 'New Delhi', 'Delhi'),
        ('Mumbai', 'Mumbai', 'Maharashtra'),
        ('Chennai', 'Chennai', 'Tamil Nadu'),
        ('Bangalore', 'Bengaluru', 'Karnataka'),
        ('Kolkata', 'Kolkata', 'West Bengal'),
        ('Hyderabad', 'Hyderabad', 'Telangana'),
        ('Pune', 'Pune', 'Maharashtra'),
        ('Jaipur', 'Jaipur', 'Rajasthan'),
        ('Varanasi', 'Varanasi', 'Uttar Pradesh'),
        ('Ahmedabad', 'Ahmedabad', 'Gujarat'),
    ]
    for name, city, state in stations_data:
        if not Station.query.filter_by(name=name).first():
            db.session.add(Station(name=name, city=city, state=state))

    # Seed sample trains
    if Train.query.count() == 0:
        trains_data = [
            ('Rajdhani Express',  'Delhi',     'Mumbai',    '06:00', '22:00', 200, 1500.00),
            ('Shatabdi Express',  'Mumbai',    'Pune',      '07:30', '10:00', 150,  300.00),
            ('Duronto Express',   'Chennai',   'Bangalore', '08:00', '12:30', 180,  500.00),
            ('Garib Rath',        'Kolkata',   'Delhi',     '14:00', '06:00', 300,  800.00),
            ('Vande Bharat',      'Delhi',     'Varanasi',  '06:00', '14:00', 100, 1200.00),
            ('Deccan Queen',      'Mumbai',    'Pune',      '17:00', '19:30', 120,  250.00),
            ('Chennai Express',   'Mumbai',    'Chennai',   '21:00', '19:30', 250, 1100.00),
            ('Howrah Mail',       'Delhi',     'Kolkata',   '22:00', '20:00', 260,  950.00),
            ('Karnataka Express', 'Delhi',     'Bangalore', '20:00', '21:30', 220, 1350.00),
            ('Tejas Express',     'Ahmedabad', 'Mumbai',    '06:40', '12:25', 130,  700.00),
        ]
        for name, src, dst, dep, arr, seats, fare in trains_data:
            db.session.add(Train(
                train_name=name, source=src, destination=dst,
                departure_time=dep, arrival_time=arr,
                total_seats=seats, available_seats=seats, fare=fare
            ))

    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
