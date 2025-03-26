
-- Script adapté pour le backend ReserKine (avec téléphone utilisateur)

DROP TABLE IF EXISTS reservations CASCADE;
DROP TABLE IF EXISTS timeslots CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Table des utilisateurs
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    telephone TEXT NOT NULL
);

-- Table des créneaux horaires
CREATE TABLE timeslots (
    id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    is_available BOOLEAN DEFAULT TRUE
);

-- Table des réservations
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    time_slot TIMESTAMP NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
