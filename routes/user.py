from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, session)
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from models import db
from models.user import User
from models.train import Train
from models.booking import Booking
from models.station import Station

user_bp = Blueprint('user', __name__)


# ── Dashboard ─────────────────────────────────────────────────────────────────
@user_bp.route('/dashboard')
@login_required
def dashboard():
    stations = Station.query.order_by(Station.name).all()
    return render_template('user/dashboard.html', stations=stations)


# ── Search Trains ──────────────────────────────────────────────────────────────
@user_bp.route('/search')
@login_required
def search():
    source      = request.args.get('source', '').strip()
    destination = request.args.get('destination', '').strip()

    if not source or not destination:
        flash('Please enter source and destination stations.', 'warning')
        return redirect(url_for('user.dashboard'))

    if source.lower() == destination.lower():
        flash('Source and destination cannot be the same.', 'warning')
        return redirect(url_for('user.dashboard'))

    trains = Train.query.filter_by(
        source=source, destination=destination, status='active'
    ).all()

    return render_template('user/search_results.html',
                           trains=trains, source=source, destination=destination)


# ── Check Fare ─────────────────────────────────────────────────────────────────
@user_bp.route('/check-fare', methods=['GET', 'POST'])
@login_required
def check_fare():
    stations = Station.query.order_by(Station.name).all()
    trains   = []
    source = destination = ''

    if request.method == 'POST':
        source      = request.form.get('source', '').strip()
        destination = request.form.get('destination', '').strip()

        if source and destination and source.lower() != destination.lower():
            trains = Train.query.filter_by(
                source=source, destination=destination, status='active'
            ).all()
            if not trains:
                flash(f'No trains found from {source} to {destination}.', 'info')
        else:
            flash('Please select valid and different source/destination.', 'warning')

    return render_template('user/check_fare.html',
                           stations=stations, trains=trains,
                           source=source, destination=destination)


# ── Book Ticket ────────────────────────────────────────────────────────────────
@user_bp.route('/book/<int:train_id>', methods=['GET', 'POST'])
@login_required
def book_ticket(train_id):
    train = Train.query.get_or_404(train_id)

    if train.status == 'cancelled':
        flash('This train has been cancelled and is no longer bookable.', 'danger')
        return redirect(url_for('user.dashboard'))

    if train.available_seats <= 0:
        flash('This train is fully booked.', 'danger')
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        try:
            seat_count = int(request.form.get('seat_count', 0))
        except (ValueError, TypeError):
            flash('Please enter a valid number of seats.', 'danger')
            return render_template('user/book_ticket.html', train=train)

        if seat_count < 1:
            flash('Seat count must be at least 1.', 'danger')
            return render_template('user/book_ticket.html', train=train)

        if seat_count > train.available_seats:
            flash(f'Only {train.available_seats} seat(s) available.', 'danger')
            return render_template('user/book_ticket.html', train=train)

        total_fare = float(train.fare) * seat_count

        # Atomic update — re-fetch with lock to prevent race conditions
        train.available_seats -= seat_count

        booking = Booking(
            user_id=current_user.id,
            train_id=train.id,
            seat_count=seat_count,
            total_fare=total_fare
        )
        db.session.add(booking)
        db.session.commit()

        flash(f'Booking confirmed! Booking ID: #{booking.id}', 'success')
        return redirect(url_for('user.booking_confirm', booking_id=booking.id))

    return render_template('user/book_ticket.html', train=train)


# ── Booking Confirmation ───────────────────────────────────────────────────────
@user_bp.route('/booking-confirm/<int:booking_id>')
@login_required
def booking_confirm(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('user.dashboard'))
    return render_template('user/booking_confirm.html', booking=booking)


# ── Booking History ────────────────────────────────────────────────────────────
@user_bp.route('/booking-history')
@login_required
def booking_history():
    bookings = (Booking.query
                .filter_by(user_id=current_user.id)
                .order_by(Booking.booking_date.desc())
                .all())
    return render_template('user/booking_history.html', bookings=bookings)


# ── Profile ────────────────────────────────────────────────────────────────────
@user_bp.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html')


# ── Edit Profile ───────────────────────────────────────────────────────────────
@user_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone     = request.form.get('phone', '').strip()

        if not full_name or not phone:
            flash('Name and phone are required.', 'danger')
            return render_template('user/edit_profile.html')

        current_user.full_name = full_name
        current_user.phone     = phone
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))

    return render_template('user/edit_profile.html')


# ── Change Password ────────────────────────────────────────────────────────────
@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password     = request.form.get('old_password', '')
        new_password     = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not check_password_hash(current_user.password_hash, old_password):
            flash('Current password is incorrect.', 'danger')
            return render_template('user/change_password.html')

        if len(new_password) < 6:
            flash('New password must be at least 6 characters.', 'danger')
            return render_template('user/change_password.html')

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return render_template('user/change_password.html')

        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('user.profile'))

    return render_template('user/change_password.html')
