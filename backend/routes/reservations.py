from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection
from utils.logger import logger
from utils.security import decrypt_id

reservations = Blueprint('reservations', __name__)

@reservations.route('/reservations', methods=['POST'])
@jwt_required()
def create_reservation():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    date = data.get('date')
    department = data.get('department')
    doctor = data.get('doctor')
    message = data.get('message')

    encrypted_id = get_jwt_identity()
    user_id = decrypt_id(encrypted_id)

    if not name or not date or not doctor:
        logger.warning("Champs requis manquants.")
        return jsonify({"message": "Nom, date, et kiné sont obligatoires."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservations (patient_name, email, phone, date_rdv, department, doctor, message, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, email, phone, date, department, doctor, message, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Réservation créée pour {name} le {date} avec {doctor}")
        return jsonify({"message": f"Rendez-vous confirmé pour {name} le {date}."}), 201
    except Exception as e:
        logger.error(f"Erreur en BDD : {e}")
        return jsonify({"message": "Erreur serveur."}), 500
