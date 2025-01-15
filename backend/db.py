import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_db_connection():
    try:
        return psycopg2.connect(**Config.DB_SETTINGS)
    except psycopg2.Error as e:
        raise RuntimeError(f"Erreur de connexion à la base de données : {e}")