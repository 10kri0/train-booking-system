from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        full_name        = request.form.get('full_name', '').strip()
        email            = request.form.get('email', '').strip().lower()
        phone            = request.form.get('phone', '').strip()
        password         = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        if not all([full_name, email, phone, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        if len(full_name) > 100:
            flash('Full name must be less than 100 characters.', 'danger')
            return render_template('auth/register.html')

        if not '@' in email or len(email) > 150:
            flash('Invalid email address.', 'danger')
            return render_template('auth/register.html')

        if len(phone) > 15 or not phone.isdigit():
            flash('Phone number must be 10-15 digits.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'danger')
            return render_template('auth/register.html')

        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f'Account created successfully! Welcome, {user.full_name}!', 'success')
        return redirect(url_for('user.dashboard'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        if not email or not password:
            flash('Please enter your email and password.', 'danger')
            return render_template('auth/login.html')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(next_page or url_for('user.dashboard'))

        flash('Invalid email or password. Please try again.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
