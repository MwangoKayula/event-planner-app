from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary in-memory storage
events = []

@app.route("/", methods=["GET"])
def home():
    return "Event Planner App is running!"

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(events)

@app.route("/events", methods=["POST"])
def add_event():
    data = request.json
    event = {
        "id": len(events) + 1,
        "title": data.get("title"),
        "date": data.get("date"),
        "location": data.get("location")
    }
    events.append(event)
    return jsonify(event), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
