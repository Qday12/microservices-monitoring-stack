from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://mongo:27017/")
db = client["userdb"]
collection = db["users"]

# Prometheus metric
REQUEST_COUNT = Counter("app_requests_total", "Total requests count", ["endpoint"])

@app.route("/users", methods=["GET", "POST"])
def users():
    REQUEST_COUNT.labels("/users").inc()
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        if not name:
            return {"error": "Name is required"}, 400
        collection.insert_one({"name": name})
        return {"message": f"User '{name}' added successfully!"}, 201
    users = [user["name"] for user in collection.find()]
    return jsonify(users)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/")
def helloworld():    
    return "Hello World!"

@app.route("/health")
def health():
    REQUEST_COUNT.labels("/health").inc()
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
