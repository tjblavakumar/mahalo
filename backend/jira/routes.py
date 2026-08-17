from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.jira.service import JiraService

router = APIRouter(prefix="/api/jira", tags=["Jira"])


class JiraUserCreate(BaseModel):
    username: str
    full_name: str
    email: str | None = None
    role: str = "developer"


class JiraStoryCreate(BaseModel):
    title: str
    description: str | None = None
    assignee_username: str | None = None
    reporter_username: str | None = None
    story_points: int = 0
    priority: str = "Medium"
    sprint: str | None = None
    status: str = "Backlog"


@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    return {"items": JiraService.list_all_users(db)}


@router.post("/users")
def create_user(payload: JiraUserCreate, db: Session = Depends(get_db)):
    user = JiraService.create_user(db, **payload.model_dump())
    return {"id": user.id, "username": user.username, "full_name": user.full_name}


@router.get("/stories")
def list_stories(db: Session = Depends(get_db)):
    stories = JiraService.list_all_stories(db, limit=100)
    return {"items": [
        {
            "story_key": story.story_key,
            "title": story.title,
            "description": story.description,
            "story_points": story.story_points,
            "priority": story.priority,
            "sprint": story.sprint,
            "status": story.status,
            "assignee_username": story.assignee.username if story.assignee else None,
            "reporter_username": story.reporter.username if story.reporter else None,
        }
        for story in stories
    ]}


@router.post("/stories")
def create_story(payload: JiraStoryCreate, db: Session = Depends(get_db)):
    story = JiraService.create_story(db, **payload.model_dump())
    return {"story_key": story.story_key, "title": story.title, "status": story.status}


@router.get("/stories/{story_key}")
def get_story(story_key: str, db: Session = Depends(get_db)):
    story = JiraService.get_story_by_key(db, story_key)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return {
        "story_key": story.story_key,
        "title": story.title,
        "description": story.description,
        "status": story.status,
        "priority": story.priority,
        "sprint": story.sprint,
        "assignee_username": story.assignee.username if story.assignee else None,
        "reporter_username": story.reporter.username if story.reporter else None,
    }


@router.get("/bugs")
def list_bugs(db: Session = Depends(get_db)):
    bugs = JiraService.list_all_bugs(db, limit=100)
    return {"items": [
        {
            "bug_key": bug.bug_key,
            "title": bug.title,
            "description": bug.description,
            "severity": bug.severity,
            "status": bug.status,
            "assignee_username": bug.assignee.username if bug.assignee else None,
            "reporter_username": bug.reporter.username if bug.reporter else None,
            "related_story_key": bug.related_story.story_key if getattr(bug, "related_story", None) else None,
            "servicenow_incident_id": bug.servicenow_incident_id,
        }
        for bug in bugs
    ]}
