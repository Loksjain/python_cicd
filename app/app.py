from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    version = os.environ.get("APP_VERSION", "dev")
    return f"🚀 Flask CI/CD running on Kubernetes! Version: {version}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
