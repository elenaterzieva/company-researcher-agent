import asyncio
import uuid
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from backend.graph import ResearchGraph

# In-memory job store (swap for Redis via backend/services/cache.py when needed)
job_store: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Company Researcher", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    company: str
    website: Optional[str] = None


async def run_research(job_id: str, company: str, website: Optional[str]):
    job_store[job_id] = {"status": "running", "node": "grounding", "report": None, "error": None}
    try:
        graph = ResearchGraph()
        async for update in graph.stream({"company": company, "website": website or ""}):
            node_name = list(update.keys())[0]
            job_store[job_id]["node"] = node_name
        final_state = update[node_name]
        job_store[job_id]["status"] = "completed"
        job_store[job_id]["report"] = final_state.get("report", "")
        job_store[job_id]["node"] = "done"
    except Exception as e:
        job_store[job_id]["status"] = "failed"
        job_store[job_id]["error"] = str(e)


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/research")
async def start_research(req: ResearchRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    background_tasks.add_task(run_research, job_id, req.company, req.website)
    return {"job_id": job_id}


@app.get("/research/{job_id}")
def get_job(job_id: str):
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/research/{job_id}/stream")
async def stream_job(job_id: str):
    async def event_generator():
        while True:
            job = job_store.get(job_id)
            if not job:
                yield f"data: {{\"error\": \"job not found\"}}\n\n"
                break
            yield f"data: {{\"status\": \"{job['status']}\", \"node\": \"{job['node']}\"}}\n\n"
            if job["status"] in ("completed", "failed"):
                break
            await asyncio.sleep(0.5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/research/{job_id}/report")
def get_report(job_id: str):
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] != "completed":
        return JSONResponse(status_code=202, content={"status": job["status"], "node": job["node"]})
    return {"report": job["report"]}
