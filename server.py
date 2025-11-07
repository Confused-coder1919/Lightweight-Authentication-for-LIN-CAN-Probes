# server.py
import asyncio, json, os, time
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ---- Your Python core modules ----
from quick_test import quick_demo             # quick_demo(return_json=True, seed=...)  <-- make sure it supports seed
from attack_simulator import run_attacks
from performance_analyzer import run_perf
from test_suite import main as run_suite

app = FastAPI(title="Automotive MAC Protocol API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# ---------- Models ----------
class AttackReq(BaseModel):
    replay: bool = True
    spoof: bool = True
    attack_rate: float = 0.2
    probes: int = 3

class PerfReq(BaseModel):
    duration_s: int = 3
    probes: int = 3

# ---------- Health ----------
@app.get("/api/health")
def health():
    return {"status": "ok", "time": time.time()}

# ---------- API Endpoints ----------
@app.post("/api/run/quick")
async def api_quick(seed: Optional[int] = None):
    """Run the quick demo; seed is optional ?seed=42 in the URL."""
    # If quick_demo doesn't accept 'seed', remove it here:
    result = quick_demo(return_json=True, seed=seed)  # or quick_demo(return_json=True)
    return JSONResponse(result)

@app.post("/api/run/attacks")
async def api_attacks(req: AttackReq):
    result = run_attacks(req.replay, req.spoof, req.attack_rate, req.probes)
    return JSONResponse(result)

@app.post("/api/run/perf")
async def api_perf(req: PerfReq):
    result = run_perf(req.duration_s, req.probes)
    return JSONResponse(result)

@app.post("/api/run/suite")
async def api_suite():
    result = run_suite(return_json=True)
    return JSONResponse(result)

# ---------- Live Logs (SSE demo) ----------
@app.get("/api/stream/logs/{run_id}")
async def stream_logs(run_id: str):
    async def eventgen():
        for i in range(30):
            yield f"data: {json.dumps({'run_id': run_id, 'line': f'Step {i}'})}\n\n"
            await asyncio.sleep(0.05)
    return StreamingResponse(eventgen(), media_type="text/event-stream")

# ---------- Static frontend ----------
BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
IMAGES_DIR = os.path.join(FRONTEND_DIR, "images")

# Serve /images/*  -> frontend/images/*
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

# (Optional) expose all frontend files under /frontend/*
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

# Serve index.html at /
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
