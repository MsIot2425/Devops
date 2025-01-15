from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
from cryptography.fernet import Fernet
import logging
import os

# Initialiser l'application Flask
app = Flask(__name__)

# Clés et configurations
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'fallback_jwt_key')  # Clé par défaut en cas d'absence
fernet_key = os.environ.get('FERNET_KEY', Fernet.generate_key())  # Générer une clé par défaut si non fournie
cipher = Fernet(fernet_key)

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ReserKine")

# Initialiser JWT
jwt = JWTManager(app)

# Connexion PostgreSQL
def get_db_connection():
    try:
        return psycopg2.connect(
            host="localhost",
            database="reserverkine",
            user="votre_utilisateur",
            password="votre_mot_de_passe"
        )
    except psycopg2.Error as e:
        logger.error(f"Erreur de connexion à la base de données : {e}")
        raise

# Gestion des erreurs globales
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Erreur non gérée : {e}")
    return jsonify({"error": str(e)}), 500

# Enregistrement d'un utilisateur
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        logger.warning("Champs manquants lors de l'enregistrement.")
        return jsonify({"message": "Tous les champs sont requis"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Utilisateur {username} enregistré avec succès.")
        return jsonify({"message": "Utilisateur créé avec succès"}), 201
    except psycopg2.Error as e:
        logger.error(f"Erreur d'enregistrement de l'utilisateur : {e}")
        return jsonify({"message": "Erreur lors de l'enregistrement de l'utilisateur"}), 500

# Authentification
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logger.warning("Tentative de connexion avec des champs manquants.")
        return jsonify({"message": "Nom d'utilisateur et mot de passe requis"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        # Chiffrer l'ID utilisateur
        encrypted_id = cipher.encrypt(str(user['id']).encode('utf-8'))
        access_token = create_access_token(identity=encrypted_id.decode('utf-8'))
        logger.info(f"Utilisateur {username} connecté avec succès.")
        return jsonify({"access_token": access_token}), 200

    logger.warning(f"Tentative de connexion échouée pour {username}.")
    return jsonify({"message": "Identifiants incorrects"}), 401

# Route protégée : créer une réservation
@app.route('/reservations', methods=['POST'])
@jwt_required()
def create_reservation():
    data = request.json
    patient = data.get('patient')
    time_slot = data.get('time_slot')

    if not patient or not time_slot:
        logger.warning("Tentative de création de réservation avec des champs manquants.")
        return jsonify({"message": "Patient et créneau horaire requis"}), 400

    # Décoder et déchiffrer l'ID utilisateur
    encrypted_id = get_jwt_identity()
    user_id = int(cipher.decrypt(encrypted_id.encode('utf-8')).decode('utf-8'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reservations (patient_name, time_slot, user_id) VALUES (%s, %s, %s)",
            (patient, time_slot, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Réservation confirmée pour {patient} à {time_slot} par l'utilisateur {user_id}.")
        return jsonify({"message": f"Réservation confirmée pour {patient} à {time_slot}"}), 201
    except psycopg2.Error as e:
        logger.error(f"Erreur lors de la création de la réservation : {e}")
        return jsonify({"message": "Erreur lors de la création de la réservation"}), 500

# Route protégée : obtenir les réservations de l'utilisateur
@app.route('/reservations', methods=['GET'])
@jwt_required()
def get_reservations():
    encrypted_id = get_jwt_identity()
    user_id = int(cipher.decrypt(encrypted_id.encode('utf-8')).decode('utf-8'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM reservations WHERE user_id = %s", (user_id,))
        reservations = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info(f"Réservations récupérées pour l'utilisateur {user_id}.")
        return jsonify(reservations), 200
    except psycopg2.Error as e:
        logger.error(f"Erreur lors de la récupération des réservations : {e}")
        return jsonify({"message": "Erreur lors de la récupération des réservations"}), 500

# Liste des créneaux disponibles
@app.route('/timeslots', methods=['GET'])
def get_timeslots():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM timeslots WHERE is_available = TRUE")
        timeslots = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info("Créneaux horaires disponibles récupérés avec succès.")
        return jsonify(timeslots), 200
    except psycopg2.Error as e:
        logger.error(f"Erreur lors de la récupération des créneaux horaires : {e}")
        return jsonify({"message": "Erreur lors de la récupération des créneaux horaires"}), 500

if __name__ == '__main__':
    app.run(debug=True)
