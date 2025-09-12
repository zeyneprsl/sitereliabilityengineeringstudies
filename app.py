from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration in seconds')
ERROR_COUNT = Counter('http_errors_total', 'Total HTTP errors', ['status_code'])

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    REQUEST_DURATION.observe(duration) 
    REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint, status=response.status_code).inc()
    if response.status_code >= 400:
        ERROR_COUNT.labels(status_code=response.status_code).inc()
    
    return response

@app.route('/')
def hello():
    return jsonify({
        "message": "Merhaba Dünya!",
        "status": "success"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    })

@app.route('/slow')
def slow_endpoint():
    delay = random.uniform(2.0, 3.0)
    time.sleep(delay)
    return jsonify({
        "message": f"Slow response after {delay:.2f} seconds",
        "status": "success",
        "delay": delay
    })

@app.route('/error')
def trigger_error():
    error_codes = [400, 401, 403, 404, 500, 502, 503]
    error_code = random.choice(error_codes)
    return jsonify({"error": f"Test error {error_code}"}), error_code

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 
   