import os
from cryptography.fernet import Fernet

class Config:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback_jwt_key')
    FERNET_KEY = os.environ.get('FERNET_KEY', Fernet.generate_key())
    DB_SETTINGS = {
        "host": "localhost",
        "database": "reserverkine",
        "user": os.environ.get('DB_USER', 'default_user'),
        "password": os.environ.get('DB_PASSWORD', 'default_password')
    }