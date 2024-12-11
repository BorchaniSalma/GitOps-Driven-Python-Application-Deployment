from flask import Flask

app = Flask(__name__)

# Simulated failure: crash on startup


@app.route("/")
def index():
    raise RuntimeError("Intentional failure for testing rollback.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
