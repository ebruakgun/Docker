import os
from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS  # CORS'ı import ettik

app = Flask(__name__)
CORS(app)  # React ile bağlantı için CORS izinleri

# Veritabanı bağlantısı
def get_db_connection():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])  # DATABASE_URL çevresel değişkenini kullanıyoruz
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

# Tablo oluşturulması
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

create_table()  # Uygulama başlarken tabloyu oluştur

@app.route("/items", methods=["GET"])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items")
    items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": row[0], "name": row[1]} for row in items])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
