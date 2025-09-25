from flask import Flask, render_template, jsonify, request
import psycopg2
import requests
import confluent_kafka
import json

NUMAFLOW_URL = "https://test-pipeline-in.default.svc:8443/vertices/in"
#NUMAFLOW_URL = "https://localhost:9001/vertices/in"

app = Flask(__name__, template_folder="../templates")

def connection():
    conn = psycopg2.connect(
        host="postgres-service",
        database="flaskdb",
        user="flaskuser",
        password="flaskpass",
        port=5432
    )
    cursor = conn.cursor()
    return conn, cursor

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/users")
def get_users():
    conn, cur = connection()
    cur.execute("SELECT id, name, age FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "age": row[2]
        })
    
    return jsonify(users), 200

@app.route("/post", methods=["POST"])
def add_to_db():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    name = data.get("name")
    age = data.get("age")

    conn, cursor = connection()
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s);", (name, age))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": f"Hello, {name}! JSON received successfully.",
        "received_data": data
    }), 200

#@app.route("/numaflow_post", methods=["GET"])
#def numaflow_post():
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    try:
        resp = requests.post(NUMAFLOW_URL, json=data)
        if resp.status_code == 200:
            return jsonify({"message": "Event sent to Numaflow", "data": data}), 200
        else:
            return jsonify({
                "error": "Failed to send event to Numaflow",
                "status_code": resp.status_code,
                "response": resp.text
            }), 500
    except Exception as e:
        return jsonify({"error": "Exception sending to Numaflow", "details": str(e)}), 500
    """
    #resp = requests.post(NUMAFLOW_URL, data='hi', verify=False)
    #return resp.text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
