from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from routes.auth import auth
from routes.reservations import reservations
from routes.timeslots import timeslots
from utils.logger import logger
from werkzeug.exceptions import NotFound

# Initialiser Flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY

# Initialiser JWT
jwt = JWTManager(app)

# Activer CORS 
CORS(app)

# Enregistrer les Blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(reservations, url_prefix='/reservations')
app.register_blueprint(timeslots, url_prefix='/timeslots')

# Route pour la page d'accueil
@app.route('/')
def index():
    """Page d'accueil de l'API"""
    return jsonify({"message": "Bienvenue sur l'API ReserKine"}), 200


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, NotFound):  # Conserver le 404
        logger.error(f"Erreur 404 : {e}")
        return jsonify({"error": "La ressource demandée est introuvable."}), 404
    logger.error(f"Erreur non gérée : {e}")
    return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    logger.info("Démarrage de l'application Flask ReserKine...")
#    app.run(debug=True) 
    app.run(host="0.0.0.0", port=5000)
