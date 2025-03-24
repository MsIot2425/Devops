from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet

load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback_jwt_key')
    FERNET_KEY = os.getenv('FERNET_KEY', Fernet.generate_key())
    DB_SETTINGS = {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "reserkine"),
        "user": os.getenv('DB_USER', 'default_user'),
        "password": os.getenv('DB_PASSWORD', 'default_password')
    }
