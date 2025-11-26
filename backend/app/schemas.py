from pydantic import BaseModel
from typing import Optional

class ImportResponse(BaseModel):
    job_id: str
    message: str
