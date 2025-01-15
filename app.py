from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth import auth
from routes.reservations import reservations
from utils.logger import logger

# Initialiser Flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY

# Initialiser JWT
jwt = JWTManager(app)

# Enregistrer les Blueprints
app.register_blueprint(auth)
app.register_blueprint(reservations)

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Erreur non gérée : {e}")
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)