from flask import Flask
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import random
import time

app = Flask(__name__)

# ========== 定义指标 ==========
# Counter：请求总数（只增不减）
REQUEST_COUNT = Counter("app_http_requests_total", "Total HTTP requests", ["method", "endpoint"])
# Counter：错误数
ERROR_COUNT = Counter("app_http_errors_total", "Total HTTP errors", ["endpoint"])
# Gauge：当前正在处理的请求（可涨可跌）
IN_FLIGHT = Gauge("app_http_in_flight_requests", "Requests in flight")

@app.route('/')
def index():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    IN_FLIGHT.inc()
    time.sleep(random.uniform(0.01, 0.1))
    IN_FLIGHT.dec()
    return "Hello from our custom Flask App! ✅"

@app.route('/error')
def error():
    REQUEST_COUNT.labels(method="GET", endpoint="/error").inc()
    ERROR_COUNT.labels(endpoint="/error").inc()
    IN_FLIGHT.inc()
    time.sleep(random.uniform(0.01, 0.05))
    IN_FLIGHT.dec()
    return "Something wrong!", 500

# prometheus metrics 端点
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
