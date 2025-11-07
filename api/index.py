# api/index.py
import os, sys, json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# make project root importable when running as serverless
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from quick_test import quick_demo
from attack_simulator import run_attacks
from performance_analyzer import run_perf
from test_suite import main as run_suite  # make sure main(return_json=True)

app = FastAPI(title="Automotive MAC Protocol API (Vercel)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)

# ---- API ROUTES ----
@app.post("/api/run/quick")
def api_quick():
    return quick_demo(return_json=True)

@app.post("/api/run/attacks")
def api_attacks():
    return run_attacks(replay=True, spoof=True, attack_rate=0.2, probes=3)

@app.post("/api/run/perf")
def api_perf():
    # keep it short for serverless limits
    return run_perf(duration_s=2, probes=3)

@app.post("/api/run/suite")
def api_suite():
    return run_suite(return_json=True)

# ---- STATIC FRONTEND ----
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

@app.get("/")
def index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
