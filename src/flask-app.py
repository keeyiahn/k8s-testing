from flask import Flask, render_template, jsonify, request
import psycopg2
def connection():
    conn = psycopg2.connect(
        host="localhost",
        database="flaskdb",
        user="flaskuser",
        password="flaskpassword",
        port=5432
    )
    cursor = conn.cursor()
    return conn, cursor

app = Flask(__name__, template_folder="../templates")

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/post", methods=["POST"])
def add_to_db():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    name = data.get("name")
    age = data.get("age")

    conn, cursor = connection()
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": f"Hello, {name}! JSON received successfully.",
        "received_data": data
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
