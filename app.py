import jwt
import os

import redis
from flask import Flask, request, jsonify, Response
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DEMO_SECRET_KEY'

redis_host = "redis"
redis_port = int(6379)
redis_client = redis.Redis(host=redis_host, port=redis_port)

start_time = datetime.now()


def get_hit_count():
    return redis_client.incr('hits')


@app.route('/')
def hello():
    count = get_hit_count()
    return jsonify({'message': 'Hello there!', 'counter': f'{count}'}), 200


@app.route('/login', methods=['POST'])
def login():
    count = get_hit_count()

    auth = request.form
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Invalid username or password!'}), 401

    username = auth.get('username')
    password = auth.get('password')

    # for demo accept only if username and password are same
    if username != password:
        return jsonify({'message': 'Invalid username or password!'}), 401

    token = jwt.encode({
        'sub': username,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'message': f'Hello {username}!', 'counter': f'{count}', 'token': token})


@app.route('/metrics', methods=['GET'])
def metrics():
    hits = redis_client.get('hits')
    if hits is not None:
        hits = int(hits)
    else:
        hits = 0
    metrics_output = (
        "# HELP http_requests_total Total request count metric\n"
        "# TYPE http_requests_total counter\n"
        f"http_requests_total {hits}\n"
    )
    return Response(metrics_output, content_type='text/plain; version=0.0.4; charset=utf-8')


@app.route('/health', methods=['GET'])
def health_check():
    current_time = datetime.now()
    uptime = current_time - start_time
    uptime_seconds = int(uptime.total_seconds())
    health_status = {
        'status': 'healthy',
        'uptime': str(uptime),  # Human-readable uptime
        'uptime_seconds': uptime_seconds,  # Uptime in seconds
    }
    return jsonify(health_status), 200


def main():
    app.run(port=int(os.environ.get('PORT', 8000)), debug=True)


if __name__ == "__main__":
    main()
