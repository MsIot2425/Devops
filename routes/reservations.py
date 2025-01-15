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
    patient = data.get('patient')
    time_slot = data.get('time_slot')

    if not patient or not time_slot:
        logger.warning("Tentative de création de réservation avec des champs manquants.")
        return jsonify({"message": "Patient et créneau horaire requis"}), 400

    encrypted_id = get_jwt_identity()
    user_id = decrypt_id(encrypted_id)

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
    except Exception as e:
        logger.error(f"Erreur lors de la création de la réservation : {e}")
        return jsonify({"message": "Erreur lors de la création de la réservation"}), 500
