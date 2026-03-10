from functools import wraps
from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, session)
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from models.admin import Admin
from models.train import Train
from models.booking import Booking
from models.station import Station
from models.user import User

admin_bp = Blueprint('admin_bp', __name__)


# ── Admin-required decorator ──────────────────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in as admin to access this page.', 'warning')
            return redirect(url_for('admin_bp.admin_login'))
        return f(*args, **kwargs)
    return decorated


def get_current_admin():
    return Admin.query.get(session.get('admin_id'))


# ── Admin Login ────────────────────────────────────────────────────────────────
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_id' in session:
        return redirect(url_for('admin_bp.dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please enter email and password.', 'danger')
            return render_template('admin/login.html')

        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id']   = admin.id
            session['admin_name'] = admin.full_name
            flash(f'Welcome, {admin.full_name}!', 'success')
            return redirect(url_for('admin_bp.dashboard'))

        flash('Invalid admin credentials.', 'danger')

    return render_template('admin/login.html')


# ── Admin Logout ───────────────────────────────────────────────────────────────
@admin_bp.route('/logout')
@admin_required
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin_bp.admin_login'))


# ── Admin Dashboard ────────────────────────────────────────────────────────────
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_trains     = Train.query.count()
    active_trains    = Train.query.filter_by(status='active').count()
    cancelled_trains = Train.query.filter_by(status='cancelled').count()
    total_bookings   = Booking.query.count()
    total_users      = User.query.count()
    recent_bookings  = (Booking.query
                        .order_by(Booking.booking_date.desc())
                        .limit(5).all())
    admin = get_current_admin()
    return render_template('admin/dashboard.html',
                           total_trains=total_trains,
                           active_trains=active_trains,
                           cancelled_trains=cancelled_trains,
                           total_bookings=total_bookings,
                           total_users=total_users,
                           recent_bookings=recent_bookings,
                           admin=admin)


# ── View All Trains ────────────────────────────────────────────────────────────
@admin_bp.route('/trains')
@admin_required
def view_trains():
    status_filter = request.args.get('status', 'all')
    query         = Train.query
    if status_filter == 'active':
        query = query.filter_by(status='active')
    elif status_filter == 'cancelled':
        query = query.filter_by(status='cancelled')
    trains = query.order_by(Train.id.desc()).all()
    admin  = get_current_admin()
    return render_template('admin/trains.html',
                           trains=trains,
                           status_filter=status_filter,
                           admin=admin)


# ── View All Bookings ──────────────────────────────────────────────────────────
@admin_bp.route('/bookings')
@admin_required
def view_bookings():
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    admin    = get_current_admin()
    return render_template('admin/bookings.html',
                           bookings=bookings,
                           admin=admin)


# ── View All Users ─────────────────────────────────────────────────────────────
@admin_bp.route('/users')
@admin_required
def view_users():
    users = User.query.order_by(User.created_at.desc()).all()
    admin_emails = [a.email for a in Admin.query.all()]
    admin = get_current_admin()
    return render_template('admin/users.html',
                           users=users,
                           admin_emails=admin_emails,
                           admin=admin)


# ── Promote User to Admin ──────────────────────────────────────────────────────
@admin_bp.route('/promote-user/<int:user_id>', methods=['POST'])
@admin_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    # Check if already admin
    existing_admin = Admin.query.filter_by(email=user.email).first()
    if existing_admin:
        flash(f'{user.full_name} is already an admin.', 'warning')
    else:
        new_admin = Admin(
            full_name=user.full_name,
            email=user.email,
            password_hash=user.password_hash  # Copy the password hash
        )
        db.session.add(new_admin)
        db.session.commit()
        flash(f'{user.full_name} has been promoted to admin.', 'success')
    return redirect(url_for('admin_bp.view_users'))


# ── Delete Booking ─────────────────────────────────────────────────────────────
@admin_bp.route('/delete-booking/<int:booking_id>', methods=['POST'])
@admin_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    train   = booking.train
    train.available_seats += booking.seat_count
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted successfully.', 'success')
    return redirect(url_for('admin_bp.view_bookings'))


# ── Add Train ──────────────────────────────────────────────────────────────────
@admin_bp.route('/add-train', methods=['GET', 'POST'])
@admin_required
def add_train():
    stations = Station.query.order_by(Station.name).all()
    admin    = get_current_admin()

    if request.method == 'POST':
        train_name     = request.form.get('train_name', '').strip()
        source         = request.form.get('source', '').strip()
        destination    = request.form.get('destination', '').strip()
        departure_time = request.form.get('departure_time', '').strip()
        arrival_time   = request.form.get('arrival_time', '').strip()

        try:
            total_seats = int(request.form.get('total_seats', 0))
            fare        = float(request.form.get('fare', 0))
        except ValueError:
            flash('Seats and fare must be valid numbers.', 'danger')
            return render_template('admin/add_train.html',
                                   stations=stations, admin=admin)

        if not all([train_name, source, destination, departure_time, arrival_time]):
            flash('All fields are required.', 'danger')
            return render_template('admin/add_train.html',
                                   stations=stations, admin=admin)

        if source.lower() == destination.lower():
            flash('Source and destination cannot be the same.', 'danger')
            return render_template('admin/add_train.html',
                                   stations=stations, admin=admin)

        if total_seats <= 0:
            flash('Total seats must be a positive number.', 'danger')
            return render_template('admin/add_train.html',
                                   stations=stations, admin=admin)

        if fare <= 0:
            flash('Fare must be a positive number.', 'danger')
            return render_template('admin/add_train.html',
                                   stations=stations, admin=admin)

        train = Train(
            train_name=train_name, source=source, destination=destination,
            departure_time=departure_time, arrival_time=arrival_time,
            total_seats=total_seats, available_seats=total_seats, fare=fare
        )
        db.session.add(train)
        db.session.commit()
        flash(f'Train "{train_name}" added successfully!', 'success')
        return redirect(url_for('admin_bp.view_trains'))

    return render_template('admin/add_train.html', stations=stations, admin=admin)


# ── Edit Train ─────────────────────────────────────────────────────────────────
@admin_bp.route('/edit-train/<int:train_id>', methods=['GET', 'POST'])
@admin_required
def edit_train(train_id):
    train    = Train.query.get_or_404(train_id)
    stations = Station.query.order_by(Station.name).all()
    admin    = get_current_admin()

    if request.method == 'POST':
        train_name     = request.form.get('train_name', '').strip()
        source         = request.form.get('source', '').strip()
        destination    = request.form.get('destination', '').strip()
        departure_time = request.form.get('departure_time', '').strip()
        arrival_time   = request.form.get('arrival_time', '').strip()

        try:
            total_seats = int(request.form.get('total_seats', 0))
            fare        = float(request.form.get('fare', 0))
        except ValueError:
            flash('Seats and fare must be valid numbers.', 'danger')
            return render_template('admin/edit_train.html',
                                   train=train, stations=stations, admin=admin)

        if not all([train_name, source, destination, departure_time, arrival_time]):
            flash('All fields are required.', 'danger')
            return render_template('admin/edit_train.html',
                                   train=train, stations=stations, admin=admin)

        if total_seats <= 0 or fare <= 0:
            flash('Seats and fare must be positive numbers.', 'danger')
            return render_template('admin/edit_train.html',
                                   train=train, stations=stations, admin=admin)

        # Adjust available seats proportionally
        seat_diff            = total_seats - train.total_seats
        train.available_seats = max(0, train.available_seats + seat_diff)

        train.train_name     = train_name
        train.source         = source
        train.destination    = destination
        train.departure_time = departure_time
        train.arrival_time   = arrival_time
        train.total_seats    = total_seats
        train.fare           = fare

        db.session.commit()
        flash(f'Train "{train_name}" updated successfully!', 'success')
        return redirect(url_for('admin_bp.view_trains'))

    return render_template('admin/edit_train.html',
                           train=train, stations=stations, admin=admin)


# ── Cancel Train (soft delete) ─────────────────────────────────────────────────
@admin_bp.route('/cancel-train/<int:train_id>', methods=['POST'])
@admin_required
def cancel_train(train_id):
    train = Train.query.get_or_404(train_id)
    train.status = 'cancelled'
    db.session.commit()
    flash(f'Train "{train.train_name}" has been cancelled.', 'warning')
    return redirect(url_for('admin_bp.view_trains'))


# ── Restore Train ──────────────────────────────────────────────────────────────
@admin_bp.route('/restore-train/<int:train_id>', methods=['POST'])
@admin_required
def restore_train(train_id):
    train = Train.query.get_or_404(train_id)
    train.status = 'active'
    db.session.commit()
    flash(f'Train "{train.train_name}" has been restored to active.', 'success')
    return redirect(url_for('admin_bp.view_trains'))


# ── Delete Train (hard delete) ─────────────────────────────────────────────────
@admin_bp.route('/delete-train/<int:train_id>', methods=['POST'])
@admin_required
def delete_train(train_id):
    train = Train.query.get_or_404(train_id)
    name  = train.train_name
    db.session.delete(train)
    db.session.commit()
    flash(f'Train "{name}" permanently deleted.', 'danger')
    return redirect(url_for('admin_bp.view_trains'))


# ── Admin Profile ──────────────────────────────────────────────────────────────
@admin_bp.route('/profile')
@admin_required
def admin_profile():
    admin = get_current_admin()
    return render_template('admin/profile.html', admin=admin)


# ── Admin Edit Profile ─────────────────────────────────────────────────────────
@admin_bp.route('/edit-profile', methods=['GET', 'POST'])
@admin_required
def admin_edit_profile():
    admin = get_current_admin()

    if request.method == 'POST':
        full_name        = request.form.get('full_name', '').strip()
        old_password     = request.form.get('old_password', '')
        new_password     = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name:
            flash('Name is required.', 'danger')
            return render_template('admin/edit_profile.html', admin=admin)

        admin.full_name = full_name
        session['admin_name'] = full_name

        # Change password if requested
        if old_password or new_password or confirm_password:
            if not check_password_hash(admin.password_hash, old_password):
                flash('Current password is incorrect.', 'danger')
                return render_template('admin/edit_profile.html', admin=admin)
            if len(new_password) < 6:
                flash('New password must be at least 6 characters.', 'danger')
                return render_template('admin/edit_profile.html', admin=admin)
            if new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
                return render_template('admin/edit_profile.html', admin=admin)
            admin.password_hash = generate_password_hash(new_password)

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin_bp.admin_profile'))

    return render_template('admin/edit_profile.html', admin=admin)
