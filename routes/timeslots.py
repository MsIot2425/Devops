from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils.logger import logger

timeslots = Blueprint('timeslots', __name__)

@timeslots.route('/timeslots', methods=['GET'])
def get_timeslots():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM timeslots WHERE is_available = TRUE")
        timeslots = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info("Créneaux horaires disponibles récupérés avec succès.")
        return jsonify(timeslots), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des créneaux horaires : {e}")
        return jsonify({"message": "Erreur lors de la récupération des créneaux horaires"}), 500

@timeslots.route('/timeslots', methods=['POST'])
def create_timeslot():
    data = request.json
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not start_time or not end_time:
        logger.warning("Tentative de création de créneau avec des champs manquants.")
        return jsonify({"message": "Heures de début et de fin requises"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO timeslots (start_time, end_time, is_available) VALUES (%s, %s, TRUE)",
            (start_time, end_time)
        )
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Créneau de {start_time} à {end_time} créé avec succès.")
        return jsonify({"message": f"Créneau de {start_time} à {end_time} créé avec succès"}), 201
    except Exception as e:
        logger.error(f"Erreur lors de la création du créneau : {e}")
        return jsonify({"message": "Erreur lors de la création du créneau"}), 500
