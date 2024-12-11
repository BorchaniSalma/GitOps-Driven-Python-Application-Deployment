from flask import Flask, render_template
import time
import random
from prometheus_client import Counter, Summary, Gauge, generate_latest

app = Flask(__name__)

# DORA Metrics
deployment_frequency = Counter(
    'deployment_frequency', 'Number of successful deployments'
)
lead_time_for_changes = Summary(
    'lead_time_for_changes', 'Lead time for changes (in seconds)'
)
mean_time_to_recovery = Gauge(
    'mean_time_to_recovery', 'Mean time to recovery (in seconds)'
)
change_failure_rate = Counter(
    'change_failure_rate', 'Number of failed changes'
)
successful_changes = Counter(
    'successful_changes', 'Number of successful changes'
)

# Custom metric for endpoint health checks
endpoint_status = Gauge(
    'endpoint_status', 'Health of specific endpoints', ['endpoint'])

# Variables for tracking recovery and lead time
start_time = None  # Start time for lead time calculation
failure_time = None  # Time of last failure for MTTR calculation
is_healthy = True  # Flag to simulate the endpoint's health


@app.route("/")
def index():
    # """Main index route with simulated failure."""
    # global is_healthy, failure_time

    # # Simulate a failure randomly (e.g., 1 in 5 requests fail)
    # if random.randint(1, 5) == 1:
    #     # Mark the endpoint as unhealthy
    #     is_healthy = False
    #     endpoint_status.labels(endpoint='/').set(0)  # Unhealthy
    #     change_failure_rate.inc()
    #     failure_time = time.time() if failure_time is None else failure_time
    #     return "Simulated failure occurred!", 500

    # # If healthy, mark the endpoint as healthy
    # if is_healthy:
    #     endpoint_status.labels(endpoint='/').set(1)  # Healthy

    # Render the frontend
    return "stable version"


@app.route("/deploy")
def deploy():
    """Simulate a successful deployment and calculate lead time."""
    global start_time
    if start_time is not None:
        # Calculate lead time for changes
        lead_time = time.time() - start_time
        lead_time_for_changes.observe(lead_time)
    # Increment deployment frequency
    deployment_frequency.inc()
    # Update start time for the next deployment
    start_time = time.time()
    return "Deployment successful!", 200


@app.route("/recover")
def recover():
    """Simulate recovery and calculate MTTR."""
    global failure_time, is_healthy
    if failure_time is not None:
        # Calculate mean time to recovery
        recovery_time = time.time() - failure_time
        mean_time_to_recovery.set(recovery_time)
        # Reset failure time after recovery
        failure_time = None
    # Mark the endpoint as healthy
    is_healthy = True
    endpoint_status.labels(endpoint='/').set(1)  # Healthy
    return "System recovered!", 200


@app.route("/metrics")
def metrics():
    """Expose metrics in Prometheus format."""
    return generate_latest(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    # Run the app on 0.0.0.0 to allow external access
    app.run(host="0.0.0.0", port=5000)
