from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint de test
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenue sur RéserKine!"})

# Authentification
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    # Simulation de validation des identifiants
    if username == "admin" and password == "1234":
        return jsonify({"message": "Connexion réussie"}), 200
    return jsonify({"message": "Identifiants incorrects"}), 401

# Gestion des réservations
@app.route("/reservations", methods=["POST"])
def create_reservation():
    data = request.json
    patient = data.get("patient")
    time_slot = data.get("time_slot")
    # Ajoutez ici une logique pour sauvegarder la réservation
    return jsonify({"message": f"Réservation confirmée pour {patient} à {time_slot}"}), 201

if __name__ == "__main__":
    app.run(debug=True)
