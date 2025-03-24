from cryptography.fernet import Fernet
from config import Config

cipher = Fernet(Config.FERNET_KEY)

def encrypt_id(user_id):
    return cipher.encrypt(str(user_id).encode('utf-8')).decode('utf-8')

def decrypt_id(encrypted_id):
    return int(cipher.decrypt(encrypted_id.encode('utf-8')).decode('utf-8'))
