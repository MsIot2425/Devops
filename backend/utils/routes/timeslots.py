from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils.logger import logger
from psycopg2.extras import RealDictCursor
import datetime

timeslots = Blueprint('timeslots', __name__)

@timeslots.route('/timeslots', methods=['GET'])
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
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des créneaux horaires : {e}")
        return jsonify({"message": "Erreur lors de la récupération des créneaux horaires"}), 500

@timeslots.route('/timeslots', methods=['POST'])
def create_timeslot():
    """Créer un nouveau créneau horaire."""
    data = request.json
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    # Validation des champs requis
    if not start_time or not end_time:
        logger.warning("Tentative de création de créneau avec des champs manquants.")
        return jsonify({"message": "Heures de début et de fin requises"}), 400

    try:
        # Validation des formats de date/heure
        start_time = datetime.datetime.fromisoformat(start_time)
        end_time = datetime.datetime.fromisoformat(end_time)

        if end_time <= start_time:
            logger.warning("L'heure de fin doit être postérieure à l'heure de début.")
            return jsonify({"message": "L'heure de fin doit être après l'heure de début"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Vérifier si un créneau similaire existe déjà
        cursor.execute(
            "SELECT * FROM timeslots WHERE start_time = %s AND end_time = %s",
            (start_time, end_time)
        )
        existing_slot = cursor.fetchone()
        if existing_slot:
            logger.warning(f"Créneau de {start_time} à {end_time} déjà existant.")
            return jsonify({"message": "Ce créneau horaire existe déjà"}), 409
        
        # Insertion du nouveau créneau
        cursor.execute(
            "INSERT INTO timeslots (start_time, end_time, is_available) VALUES (%s, %s, TRUE)",
            (start_time, end_time)
        )
        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Créneau de {start_time} à {end_time} créé avec succès.")
        return jsonify({"message": f"Créneau de {start_time} à {end_time} créé avec succès"}), 201
    
    except ValueError as ve:
        logger.error(f"Format de date invalide : {ve}")
        return jsonify({"message": "Format de date/heure invalide. Utilisez ISO 8601 (YYYY-MM-DDTHH:MM:SS)"}), 400

    except Exception as e:
        logger.error(f"Erreur lors de la création du créneau : {e}")
        return jsonify({"message": "Erreur lors de la création du créneau"}), 500
