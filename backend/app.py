from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://mongo:27017/")
db = client["userdb"]
collection = db["users"]

# Insert example data if collection is empty
if collection.count_documents({}) == 0:
    collection.insert_many([
        {"name": "Alice"},
        {"name": "Bob"},
        {"name": "Charlie"}
    ])

# Prometheus metric
REQUEST_COUNT = Counter("app_requests_total", "Total requests count", ["endpoint"])

@app.route("/users")
def get_users():
    REQUEST_COUNT.labels("/users").inc()
    users = [user["name"] for user in collection.find()]
    return jsonify(users)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/health")
def health():
    REQUEST_COUNT.labels("/health").inc()
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
