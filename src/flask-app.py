from flask import Flask, render_template, jsonify, request
app = Flask(__name__, template_folder="../templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/post", methods=["POST"])
def handle_post():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    name = data.get("name", "Guest")

    return jsonify({
        "message": f"Hello, {name}! JSON received successfully.",
        "received_data": data
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
