from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # React ile bağlantı için CORS izinleri

# Veritabanı bağlantısı
def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="mydb",
        user="user",
        password="password"
    )
    return conn

@app.route("/")
def home():
    return jsonify({"message": "Hello from Flask Backend!"})

@app.route("/data")
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from PostgreSQL!' ")
    data = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({"database_message": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
