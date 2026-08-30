import os
from pathlib import Path
import sqlite3

from flask import Flask, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DATA_DIR", "/data" if os.getenv("AMVERA") else BASE_DIR / "data"))
DATABASE_PATH = DATA_DIR / "items.sqlite3"
app = Flask(__name__)


def connect():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with connect() as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)"
        )


initialize_database()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify(ok=True, framework="Flask", storage=str(DATABASE_PATH))


@app.get("/api/items")
def get_items():
    with connect() as connection:
        rows = connection.execute("SELECT id, name FROM items ORDER BY id DESC").fetchall()
    items = [dict(row) for row in rows]
    return jsonify(items=items, count=len(items))


@app.post("/api/items")
def add_item():
    data = request.get_json() or {}
    name = str(data.get("name", "")).strip()
    if not name or len(name) > 120:
        return jsonify(error="Name must contain from 1 to 120 characters"), 400
    with connect() as connection:
        cursor = connection.execute("INSERT INTO items (name) VALUES (?)", (name,))
    return jsonify(item={"id": cursor.lastrowid, "name": name}), 201


@app.delete("/api/items/<int:item_id>")
def delete_item(item_id):
    with connect() as connection:
        cursor = connection.execute("DELETE FROM items WHERE id = ?", (item_id,))
    if cursor.rowcount == 0:
        return jsonify(error="Item not found"), 404
    return jsonify(deleted=True, id=item_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
