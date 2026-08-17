from fastapi import APIRouter

from backend.config import settings
from backend.database import SessionLocal, init_db
from backend.utils.reset_data import reset_demo_data
from agents.context_manager import context_manager

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/status")
def status():
    return {
        "overall_status": "healthy",
        "healthy_services": 1,
        "total_services": 1,
        "services": {"main_api": {"status": "healthy", "port": settings.MAIN_API_PORT}},
    }


@router.get("/info")
def info():
    return {
        "name": "MAHALO",
        "version": "1.0.0",
        "description": "AI Harness for SDLC",
        "demo_reset_enabled": True,
    }


@router.post("/reset-data")
def reset_data():
    reset_demo_data()
    context_manager.clear()
    return {"message": "Demo data reset successful", "status": "success"}


@router.get("/stats")
def stats():
    history = context_manager.get_conversation_history(last_n=None)
    return {
        "conversations": {
            "total_messages": len(history),
            "user_messages": sum(message["role"] == "user" for message in history),
            "assistant_messages": sum(message["role"] == "assistant" for message in history),
        }
    }
