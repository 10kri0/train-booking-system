-- ============================================================
-- Online Train Booking System — Database Schema
-- Database: train_booking_db
-- ============================================================
CREATE DATABASE IF NOT EXISTS train_booking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE train_booking_db;
-- ------------------------------------------------------------
-- Table: users
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- ------------------------------------------------------------
-- Table: admins
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_admins_email (email)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- ------------------------------------------------------------
-- Table: stations (optional master list)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- ------------------------------------------------------------
-- Table: trains
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS trains (
    id INT AUTO_INCREMENT PRIMARY KEY,
    train_name VARCHAR(150) NOT NULL,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    departure_time VARCHAR(10) NOT NULL,
    arrival_time VARCHAR(10) NOT NULL,
    total_seats INT NOT NULL CHECK (total_seats > 0),
    available_seats INT NOT NULL CHECK (available_seats >= 0),
    fare DECIMAL(10, 2) NOT NULL CHECK (fare > 0),
    status ENUM('active', 'cancelled') NOT NULL DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_trains_route (source, destination),
    INDEX idx_trains_status (status)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- ------------------------------------------------------------
-- Table: bookings
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    train_id INT NOT NULL,
    seat_count INT NOT NULL CHECK (seat_count >= 1),
    total_fare DECIMAL(10, 2) NOT NULL,
    booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bookings_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_bookings_train FOREIGN KEY (train_id) REFERENCES trains(id) ON DELETE CASCADE,
    INDEX idx_bookings_user (user_id),
    INDEX idx_bookings_train (train_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- ============================================================
-- Seed Data
-- ============================================================
-- Seed Stations
INSERT IGNORE INTO stations (name, city, state)
VALUES ('Delhi', 'New Delhi', 'Delhi'),
    ('Mumbai', 'Mumbai', 'Maharashtra'),
    ('Chennai', 'Chennai', 'Tamil Nadu'),
    ('Bangalore', 'Bengaluru', 'Karnataka'),
    ('Kolkata', 'Kolkata', 'West Bengal'),
    ('Hyderabad', 'Hyderabad', 'Telangana'),
    ('Pune', 'Pune', 'Maharashtra'),
    ('Jaipur', 'Jaipur', 'Rajasthan'),
    ('Varanasi', 'Varanasi', 'Uttar Pradesh'),
    ('Ahmedabad', 'Ahmedabad', 'Gujarat');
-- Seed Sample Trains
INSERT IGNORE INTO trains (
        train_name,
        source,
        destination,
        departure_time,
        arrival_time,
        total_seats,
        available_seats,
        fare,
        status
    )
VALUES (
        'Rajdhani Express',
        'Delhi',
        'Mumbai',
        '06:00',
        '22:00',
        200,
        200,
        1500.00,
        'active'
    ),
    (
        'Shatabdi Express',
        'Mumbai',
        'Pune',
        '07:30',
        '10:00',
        150,
        150,
        300.00,
        'active'
    ),
    (
        'Duronto Express',
        'Chennai',
        'Bangalore',
        '08:00',
        '12:30',
        180,
        180,
        500.00,
        'active'
    ),
    (
        'Garib Rath',
        'Kolkata',
        'Delhi',
        '14:00',
        '06:00',
        300,
        300,
        800.00,
        'active'
    ),
    (
        'Vande Bharat',
        'Delhi',
        'Varanasi',
        '06:00',
        '14:00',
        100,
        100,
        1200.00,
        'active'
    ),
    (
        'Deccan Queen',
        'Mumbai',
        'Pune',
        '17:00',
        '19:30',
        120,
        120,
        250.00,
        'active'
    ),
    (
        'Chennai Express',
        'Mumbai',
        'Chennai',
        '21:00',
        '19:30',
        250,
        250,
        1100.00,
        'active'
    ),
    (
        'Howrah Mail',
        'Delhi',
        'Kolkata',
        '22:00',
        '20:00',
        260,
        260,
        950.00,
        'active'
    ),
    (
        'Karnataka Express',
        'Delhi',
        'Bangalore',
        '20:00',
        '21:30',
        220,
        220,
        1350.00,
        'active'
    ),
    (
        'Tejas Express',
        'Ahmedabad',
        'Mumbai',
        '06:40',
        '12:25',
        130,
        130,
        700.00,
        'active'
    );
-- NOTE: The default admin account is seeded by the Flask app on first startup.
-- To manually insert (replace hash with generated Werkzeug hash):
-- INSERT IGNORE INTO admins (full_name, email, password_hash) VALUES
--     ('System Admin', 'admin@trainbooking.com', '<werkzeug-hash>');