from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    # Render the HTML frontend
    return render_template("index.html")


@app.route("/metrics")
def metrics():
    # Expose basic metrics for Prometheus
    return "app_requests_total{status='success'} 10\napp_requests_total{status='failure'} 2", 200, {
        "Content-Type": "text/plain; version=0.0.4"
    }


if __name__ == "__main__":
    # Run the app on 0.0.0.0 to allow external access
    app.run(host="0.0.0.0", port=5000)
