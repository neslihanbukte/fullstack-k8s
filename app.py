from flask import Flask, jsonify, Response
import sqlite3
import os
import socket
import time

app = Flask(__name__)

DB_PATH = "data.db"
POD_NAME = socket.gethostname()


request_count = 0

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
    global request_count
    request_count += 1
    
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
    metrics_output = f"""# HELP app_requests_total Total number of requests to the app
# TYPE app_requests_total counter
app_requests_total{{pod="{POD_NAME}"}} {request_count}
"""
    return Response(metrics_output, mimetype="text/plain; version=0.0.4; charset=utf-8")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
