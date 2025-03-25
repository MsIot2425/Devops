from db import get_db_connection

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")  # Test simple
    result = cursor.fetchone()
    print("✅ Connexion réussie ! Résultat :", result)
    cursor.close()
    conn.close()
except Exception as e:
    print("❌ Erreur de connexion :", e)
