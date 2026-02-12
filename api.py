from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tasks

app = FastAPI(title="Cognexa Worker API")


class FileProcessRequest(BaseModel):
    file_id: str
    project_id: str
    storage_key: str


@app.post("/process-file")
async def process_file(request: FileProcessRequest):
    """
    Enqueues a file for processing by the worker.
    """
    try:
        # Enqueue the task
        tasks.process_file.send(
            request.file_id, request.project_id, request.storage_key
        )
        return {
            "message": "File processing task enqueued successfully",
            "file_id": request.file_id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "ok"}
