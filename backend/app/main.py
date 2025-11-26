import os
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .utils import temp_filename
from .tasks import celery, process_csv_task
from .schemas import ImportResponse
import shutil, logging

logger = logging.getLogger("uvicorn.error")
app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/import", response_model=ImportResponse)
async def import_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")
    local_path = temp_filename(file.filename)
    # stream write to disk to avoid loading fully in memory
    with open(local_path, "wb") as buffer:
        while True:
            chunk = await file.read(settings.CHUNK_SIZE)
            if not chunk:
                break
            buffer.write(chunk)
    # enqueue Celery task
    task = process_csv_task.delay(local_path)
    return {"job_id": task.id, "message": "Upload accepted, processing started"}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    res = celery.AsyncResult(job_id)
    return {"job_id": job_id, "status": res.status, "result": res.result}
