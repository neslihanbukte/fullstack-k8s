from flask import Flask, jsonify, Response
import sqlite3
import os
import random

app = Flask(__name__)

DB_PATH = "data.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("CREATE TABLE entries (id INTEGER PRIMARY KEY AUTOINCREMENT, value TEXT)")
        c.execute("INSERT INTO entries (value) VALUES ('first entry')")
        conn.commit()
        conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM entries ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return jsonify({
        "message": "Hello from Demo-App!",
        "last_entry": {"id": row[0], "value": row[1]} if row else None
    })

@app.route("/metrics")
def metrics():
    number = random.randint(0, 100)

    
    metric_output = f"""# HELP demo_app_random_metric A random metric for demo
# TYPE demo_app_random_metric gauge
demo_app_random_metric {number}
"""
    return Response(metric_output, mimetype="text/plain")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
