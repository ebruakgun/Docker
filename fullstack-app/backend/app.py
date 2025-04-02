from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

# GET: Tüm öğeleri al
@app.route("/items", methods=["GET"])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items")
    items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": row[0], "name": row[1]} for row in items])

# GET: ID'ye göre bir öğe al
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items WHERE id = %s", (item_id,))
    item = cur.fetchone()
    cur.close()
    conn.close()
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"id": item[0], "name": item[1]})

# POST: Yeni bir öğe oluştur
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    name = data.get("name")
    
    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id", (name,))
    item_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": item_id, "name": name}), 201

# PUT: Var olan bir öğeyi güncelle
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    name = data.get("name")
    
    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE items SET name = %s WHERE id = %s", (name, item_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": item_id, "name": name})

# DELETE: Bir öğeyi sil
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Item deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
