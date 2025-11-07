from flask import Flask, jsonify, send_from_directory, render_template
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

SCRIPTS = {
    "quick": "quick_test.py",
    "attack": "attack_simulator.py",
    "perf": "performance_analyzer.py",
    "suite": "test_suite.py",
}

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/run/<name>")
def run(name):
    if name not in SCRIPTS:
        return jsonify({"error": "invalid script"}), 400
    proc = subprocess.run(["python3", SCRIPTS[name]], capture_output=True, text=True)
    return jsonify({
        "ok": proc.returncode == 0,
        "stdout": proc.stdout,
        "stderr": proc.stderr
    })

# serve generated images easily
@app.get("/images/<path:filename>")
def images(filename):
    return send_from_directory(".", filename)

if __name__ == "__main__":
    app.run(debug=True)
