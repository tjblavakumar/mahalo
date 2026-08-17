from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.splunk.service import SplunkService

router = APIRouter(prefix="/api/splunk", tags=["Splunk"])


class LogCreate(BaseModel):
    source: str
    level: str = "INFO"
    message: str
    service: str


@router.get("/logs")
def list_logs(db: Session = Depends(get_db)):
    return {"items": SplunkService.list_logs(db)}


@router.post("/logs")
def create_log(payload: LogCreate, db: Session = Depends(get_db)):
    log = SplunkService.create_log(db, **payload.model_dump())
    return {"id": log.id, "source": log.source, "level": log.level, "service": log.service}


@router.get("/search")
def search_logs(query: str, db: Session = Depends(get_db)):
    return {"items": SplunkService.search_logs(db, query)}
