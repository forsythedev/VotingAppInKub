from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)
redis_host = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.route('/vote', methods=['POST'])
def vote():
    candidate = request.json.get('candidate')
    if not candidate:
        return jsonify({"error": "No candidate provided"}), 400
    r.incr(candidate)
    return jsonify({"message": f"Vote counted for {candidate}"}), 200

@app.route('/results', methods=['GET'])
def results():
    keys = r.keys('*')
    results = {k: int(r.get(k)) for k in keys}
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
