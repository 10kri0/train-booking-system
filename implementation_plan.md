# Implementation Plan: Online Train Booking System (Full-Stack)

Complete Flask + SQLAlchemy + MySQL + Bootstrap web application built from scratch inside `c:\python projects\Train Booking Systrem copy\`.

---

## User Review Required

> [!IMPORTANT]
> This plan creates **~35+ new files** from scratch. The project directory currently only contains a `Docs/` folder — no source code exists yet.

> [!IMPORTANT]
> **MySQL credentials**: The generated `config.py` will use default values (`root` / no password / `train_booking_db`). You will need to update the `.env` file with your actual MySQL password before running the app.

> [!NOTE]
> **ORM choice**: SQLAlchemy is used for models and migrations. A `schema.sql` raw SQL file is also generated for reference and manual DB setup.

---

## Proposed Changes

### Component 1 — Project Root

#### [NEW] [app.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/app.py)
Flask application factory (`create_app()`). Registers all blueprints, initializes SQLAlchemy, Flask-Login, and creates DB tables on startup.

#### [NEW] [config.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/config.py)
`Config` class loading from `.env`: `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `DEBUG`.

#### [NEW] [.env.example](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/.env.example)
Template for environment variables.

#### [NEW] [requirements.txt](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/requirements.txt)
```
Flask
Flask-SQLAlchemy
Flask-Login
PyMySQL
cryptography
python-dotenv
Werkzeug
```

#### [NEW] [schema.sql](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/schema.sql)
Raw SQL CREATE TABLE statements for `users`, `admins`, `trains`, `bookings`, `stations`. Includes PKs, FKs, indexes, CHECK constraints, seed data.

---

### Component 2 — Database Models

#### [NEW] [models/__init__.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/models/__init__.py)
SQLAlchemy `db` instance creation.

#### [NEW] [models/user.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/models/user.py)
`User` model: `id`, `full_name`, `email` (unique), `phone`, `password_hash`, `created_at`. Implements `UserMixin` for Flask-Login.

#### [NEW] [models/admin.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/models/admin.py)
`Admin` model: `id`, `full_name`, `email` (unique), `password_hash`, `created_at`. Implements `UserMixin`.

#### [NEW] [models/train.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/models/train.py)
`Train` model: `id`, `train_name`, `source`, `destination`, `departure_time`, `arrival_time`, `total_seats`, `available_seats`, `fare`, `status` (active/cancelled), `created_at`.

#### [NEW] [models/booking.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/models/booking.py)
`Booking` model: `id`, `user_id` (FK→users), `train_id` (FK→trains), `seat_count`, `total_fare`, `booking_date`. Relationships to User and Train.

#### [NEW] [models/station.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/models/station.py)
`Station` model: `id`, `name` (unique), `city`, `state`. Used for station dropdowns.

---

### Component 3 — Flask Routes (Blueprints)

#### [NEW] [routes/__init__.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/routes/__init__.py)

#### [NEW] [routes/auth.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/routes/auth.py)
Blueprint `auth`. Routes:
- `GET/POST /register` — User registration with bcrypt hashing
- `GET/POST /login` — User login, session creation
- `GET /logout` — Clear user session
- `GET /` — Landing redirect

#### [NEW] [routes/user.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/routes/user.py)
Blueprint `user`, prefix `/user`. All routes protected by `@login_required`.
- `GET /dashboard` — Dashboard with search form
- `GET /search` — Train search results (query params: source, destination)
- `GET /check-fare` — Fare check form + results
- `GET/POST /book/<train_id>` — Booking form + booking submission
- `GET /booking-confirm/<booking_id>` — Booking confirmation page
- `GET /booking-history` — User's booking history
- `GET /profile` — View profile
- `GET/POST /edit-profile` — Edit name + phone
- `GET/POST /change-password` — Change password with old-password verification

#### [NEW] [routes/admin.py](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/routes/admin.py)
Blueprint `admin_bp`, prefix `/admin`. All routes protected by admin session check.
- `GET/POST /login` — Admin login
- `GET /logout` — Admin logout
- `GET /dashboard` — Stats overview
- `GET /trains` — All trains table
- `GET/POST /add-train` — Add train form
- `GET/POST /edit-train/<id>` — Edit train (pre-filled)
- `POST /cancel-train/<id>` — Soft-cancel train
- `POST /delete-train/<id>` — Hard delete train
- `GET /profile` — Admin profile view
- `GET/POST /edit-profile` — Admin edit profile

---

### Component 4 — HTML Templates (Jinja2 + Bootstrap 5)

All templates extend `base.html` which provides:
- Bootstrap 5 CDN
- Navbar (conditional: user/admin/guest links)
- Flash message alert banners
- Footer

| Template | Purpose |
|---|---|
| `base.html` | Master layout |
| `index.html` | Landing page |
| `auth/login.html` | User login |
| `auth/register.html` | User registration |
| `user/dashboard.html` | Search form + welcome |
| `user/search_results.html` | Train table + Book button |
| `user/check_fare.html` | Fare check results |
| `user/book_ticket.html` | Booking form with JS fare preview |
| `user/booking_confirm.html` | Booking confirmation |
| `user/booking_history.html` | History table |
| `user/profile.html` | Profile view |
| `user/edit_profile.html` | Edit profile form |
| `user/change_password.html` | Change password form |
| `admin/login.html` | Admin login |
| `admin/dashboard.html` | Stats cards + quick links |
| `admin/trains.html` | Full trains CRUD table |
| `admin/add_train.html` | Add train form |
| `admin/edit_train.html` | Edit train form (pre-filled) |
| `admin/profile.html` | Admin profile |
| `admin/edit_profile.html` | Admin edit profile |
| `errors/404.html` | 404 page |
| `errors/500.html` | 500 page |

---

### Component 5 — Static Assets

#### [NEW] [static/css/style.css](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/static/css/style.css)
Custom styles layered on Bootstrap: color theme (`#1a237e` navy + `#ff6f00` amber), card shadows, hero section, table hover styles, availability badges.

#### [NEW] [static/js/main.js](file:///c:/python%20projects/Train%20Booking%20Systrem%20copy/static/js/main.js)
- Dynamic total fare calculation on booking page (seat count × fare)
- Flash message auto-dismiss (3 seconds)
- Cancel train confirmation dialog
- Form validation helpers

---

## Verification Plan

### Setup Steps (Required Before Testing)
1. Install dependencies: `pip install -r requirements.txt`
2. Set MySQL credentials in `.env` (copy from `.env.example`)
3. Create database in MySQL: `CREATE DATABASE train_booking_db CHARACTER SET utf8mb4;`
4. Run: `python app.py` — SQLAlchemy auto-creates all tables on first run
5. Open browser: `http://localhost:5000`

### Manual Verification Tests

#### Test 1 — User Registration & Login
1. Navigate to `http://localhost:5000/register`
2. Fill in: Name, Email, Phone, Password (≥6 chars), Confirm Password → Submit
3. **Expected:** Redirected to `/login` with success flash "Account created successfully!"
4. Login with same credentials → **Expected:** Redirected to `/user/dashboard`

#### Test 2 — Train Search & Booking
1. On user dashboard, enter Source: "Delhi", Destination: "Mumbai" → Search
2. **Expected:** Train results table shown with fare, seats, and "Book" button
3. Click "Book" on any train, enter seat count = 2 → Confirm
4. **Expected:** Booking confirmation page with Booking ID + total fare
5. Navigate to "My Bookings" → **Expected:** New booking appears in history table

#### Test 3 — Admin Login & Train Management
1. Navigate to `http://localhost:5000/admin/login`
2. Login with seeded admin credentials (admin@trainbooking.com / Admin@123)
3. **Expected:** Redirected to `/admin/dashboard` showing stats
4. Click "Add Train" → Fill form → Submit → **Expected:** Train appears in train list
5. Click "Edit" on a train → Change fare → Save → **Expected:** Updated fare shown
6. Click "Cancel" on a train → **Expected:** Train marked cancelled, disappears from user search

#### Test 4 — Session Protection
1. Without logging in, navigate to `http://localhost:5000/user/dashboard`
2. **Expected:** Redirected to `/login`
3. Without admin session, navigate to `http://localhost:5000/admin/dashboard`
4. **Expected:** Redirected to `/admin/login`

#### Test 5 — Profile Management
1. Login as user → Navigate to Profile → Click "Edit Profile"
2. Change phone number → Save → **Expected:** Updated phone shown on profile
3. Click "Change Password" → Enter wrong old password → **Expected:** Error flash
4. Enter correct old password + new password → **Expected:** Success flash; login with new password works
