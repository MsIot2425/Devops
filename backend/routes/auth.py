from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from db import get_db_connection
from utils.logger import logger
from utils.security import encrypt_id
import bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
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
    except Exception as e:
        logger.error(f"Erreur d'enregistrement de l'utilisateur : {e}")
        return jsonify({"message": "Erreur lors de l'enregistrement de l'utilisateur"}), 500

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Nom d'utilisateur et mot de passe requis"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        encrypted_id = encrypt_id(user['id'])
        access_token = create_access_token(identity=encrypted_id)
        logger.info(f"Utilisateur {username} connecté avec succès.")
        return jsonify({"access_token": access_token}), 200

    logger.warning(f"Tentative de connexion échouée pour {username}.")
    return jsonify({"message": "Identifiants incorrects"}), 401
