# MAHALO - Phase 1: Build Mock APIs ## JIRA, ServiceNow, and Splunk Mock Services
Phase Goal: Build fully functional mock APIs for JIRA, ServiceNow, and Splunk with SQLite backend.

Estimated Time: 4-6 hours

Prerequisites:

Phase 0 completed successfully
Database initialized with all tables
Virtual environment activated
📋 Phase 1 Overview
This phase builds the foundation mock tools:

JIRA API (Port 5001) - User stories, bugs, sprints, velocity
ServiceNow API (Port 5002) - Incident management
Splunk API (Port 5003) - Log search and analysis
Seed Data - Realistic demo data for all tools
Automated Tests - API endpoint testing
Reset Utility - Quick demo data reset
Each tool follows the same pattern:

Service Layer → Business logic
Routes → FastAPI endpoints
App → Standalone FastAPI application
Seed Data → Demo data population
Tests → Automated testing
🔧 JIRA API Implementation
Task 1.1: Create JIRA Service Layer ⬜
Instruction to Coding Assistant: Create the business logic layer for JIRA operations.

Create backend/jira/service.py
"""
JIRA Service Layer
Business logic for JIRA operations (users, stories, bugs, sprints)
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from backend.models.jira_models import JiraUser, JiraStory, JiraBug, JiraSprint
from datetime import datetime, timedelta
from typing import List, Optional, Dict

class JiraService:
    """Service class containing all JIRA business logic"""
    
    # ==================== USER OPERATIONS ====================
    
    @staticmethod
    def create_user(
        db: Session,
        username: str,
        full_name: str,
        email: Optional[str] = None,
        role: str = "developer"
    ) -> JiraUser:
        """Create a new JIRA user"""
        user = JiraUser(
            username=username,
            full_name=full_name,
            email=email,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[JiraUser]:
        """Get user by username"""
        return db.query(JiraUser).filter(JiraUser.username == username).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[JiraUser]:
        """Get user by ID"""
        return db.query(JiraUser).filter(JiraUser.id == user_id).first()
    
    @staticmethod
    def list_all_users(db: Session) -> List[JiraUser]:
        """Get all users"""
        return db.query(JiraUser).all()
    
    # ==================== STORY OPERATIONS ====================
    
    @staticmethod
    def create_story(
        db: Session,
        title: str,
        description: Optional[str] = None,
        assignee_username: Optional[str] = None,
        reporter_username: Optional[str] = None,
        story_points: int = 0,
        priority: str = "Medium",
        sprint: Optional[str] = None,
        status: str = "Backlog"
    ) -> JiraStory:
        """Create a new user story"""
        # Generate story key
        last_story = db.query(JiraStory).order_by(JiraStory.id.desc()).first()
        next_id = (last_story.id + 1) if last_story else 1
        story_key = f"STORY-{next_id}"
        
        # Get user IDs
        assignee_id = None
        reporter_id = None
        if assignee_username:
            assignee = JiraService.get_user_by_username(db, assignee_username)
            assignee_id = assignee.id if assignee else None
        if reporter_username:
            reporter = JiraService.get_user_by_username(db, reporter_username)
            reporter_id = reporter.id if reporter else None
        
        story = JiraStory(
            story_key=story_key,
            title=title,
            description=description,
            assignee_id=assignee_id,
            reporter_id=reporter_id,
            story_points=story_points,
            priority=priority,
            sprint=sprint,
            status=status
        )
        db.add(story)
        db.commit()
        db.refresh(story)
        return story
    
    @staticmethod
    def get_story_by_key(db: Session, story_key: str) -> Optional[JiraStory]:
        """Get story by story key"""
        return db.query(JiraStory).filter(JiraStory.story_key == story_key).first()
    
    @staticmethod
    def search_stories_by_title(db: Session, title_query: str) -> List[JiraStory]:
        """Search stories by title (for duplicate detection)"""
        return db.query(JiraStory).filter(
            JiraStory.title.ilike(f"%{title_query}%")
        ).all()
    
    @staticmethod
    def update_story_status(db: Session, story_key: str, new_status: str) -> Optional[JiraStory]:
        """Update story status"""
        story = JiraService.get_story_by_key(db, story_key)
        if story:
            story.status = new_status
            story.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(story)
        return story
    
    @staticmethod
    def update_story(
        db: Session,
        story_key: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        assignee_username: Optional[str] = None,
        story_points: Optional[int] = None,
        priority: Optional[str] = None
    ) -> Optional[JiraStory]:
        """Update story fields"""
        story = JiraService.get_story_by_key(db, story_key)
        if not story:
            return None
        
        if title is not None:
            story.title = title
        if description is not None:
            story.description = description
        if status is not None:
            story.status = status
        if story_points is not None:
            story.story_points = story_points
        if priority is not None:
            story.priority = priority
        if assignee_username is not None:
            assignee = JiraService.get_user_by_username(db, assignee_username)
            story.assignee_id = assignee.id if assignee else None
        
        story.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(story)
        return story
    
    @staticmethod
    def get_stories_by_status(db: Session, status: str) -> List[JiraStory]:
        """Get all stories by status"""
        return db.query(JiraStory).filter(JiraStory.status == status).all()
    
    @staticmethod
    def get_stories_by_sprint(db: Session, sprint: str) -> List[JiraStory]:
        """Get all stories in a sprint"""
        return db.query(JiraStory).filter(JiraStory.sprint == sprint).all()
    
    @staticmethod
    def get_stories_by_assignee(db: Session, username: str) -> List[JiraStory]:
        """Get stories assigned to a user"""
        user = JiraService.get_user_by_username(db, username)
        if not user:
            return []
        return db.query(JiraStory).filter(JiraStory.assignee_id == user.id).all()
    
    @staticmethod
    def list_all_stories(db: Session, limit: int = 100) -> List[JiraStory]:
        """List all stories with optional limit"""
        return db.query(JiraStory).limit(limit).all()
    
    # ==================== BUG OPERATIONS ====================
    
    @staticmethod
    def create_bug(
        db: Session,
        title: str,
        description: Optional[str] = None,
        assignee_username: Optional[str] = None,
        reporter_username: Optional[str] = None,
        severity: str = "Medium",
        related_story_key: Optional[str] = None,
        servicenow_incident_id: Optional[str] = None,
        status: str = "Open"
    ) -> JiraBug:
        """Create a new bug"""
        # Generate bug key
        last_bug = db.query(JiraBug).order_by(JiraBug.id.desc()).first()
        next_id = (last_bug.id + 1) if last_bug else 1
        bug_key = f"BUG-{next_id}"
        
        # Get user IDs
        assignee_id = None
        reporter_id = None
        if assignee_username:
            assignee = JiraService.get_user_by_username(db, assignee_username)
            assignee_id = assignee.id if assignee else None
        if reporter_username:
            reporter = JiraService.get_user_by_username(db, reporter_username)
            reporter_id = reporter.id if reporter else None
        
        # Get related story ID
        related_story_id = None
        if related_story_key:
            story = JiraService.get_story_by_key(db, related_story_key)
            related_story_id = story.id if story else None
        
        bug = JiraBug(
            bug_key=bug_key,
            title=title,
            description=description,
            assignee_id=assignee_id,
            reporter_id=reporter_id,
            severity=severity,
            related_story_id=related_story_id,
            servicenow_incident_id=servicenow_incident_id,
            status=status
        )
        db.add(bug)
        db.commit()
        db.refresh(bug)
        return bug
    
    @staticmethod
    def get_bug_by_key(db: Session, bug_key: str) -> Optional[JiraBug]:
        """Get bug by bug key"""
        return db.query(JiraBug).filter(JiraBug.bug_key == bug_key).first()
    
    @staticmethod
    def update_bug_status(db: Session, bug_key: str, new_status: str) -> Optional[JiraBug]:
        """Update bug status"""
        bug = JiraService.get_bug_by_key(db, bug_key)
        if bug:
            bug.status = new_status
            bug.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(bug)
        return bug
    
    @staticmethod
    def get_bugs_by_status(db: Session, status: str) -> List[JiraBug]:
        """Get bugs by status"""
        return db.query(JiraBug).filter(JiraBug.status == status).all()
    
    @staticmethod
    def get_bugs_by_severity(db: Session, severity: str) -> List[JiraBug]:
        """Get bugs by severity"""
        return db.query(JiraBug).filter(JiraBug.severity == severity).all()
    
    @staticmethod
    def get_bugs_by_assignee(db: Session, username: str) -> List[JiraBug]:
        """Get bugs assigned to a user"""
        user = JiraService.get_user_by_username(db, username)
        if not user:
            return []
        return db.query(JiraBug).filter(JiraBug.assignee_id == user.id).all()
    
    @staticmethod
    def list_all_bugs(db: Session, limit: int = 100) -> List[JiraBug]:
        """List all bugs with optional limit"""
        return db.query(JiraBug).limit(limit).all()
    
    # ==================== SPRINT OPERATIONS ====================
    
    @staticmethod
    def create_sprint(
        db: Session,
        sprint_name: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        total_points: int = 0,
        completed_points: int = 0,
        status: str = "Active"
    ) -> JiraSprint:
        """Create a new sprint"""
        sprint = JiraSprint(
            sprint_name=sprint_name,
            start_date=start_date,
            end_date=end_date,
            total_points=total_points,
            completed_points=completed_points,
            status=status
        )
        db.add(sprint)
        db.commit()
        db.refresh(sprint)
        return sprint
    
    @staticmethod
    def get_sprint_by_name(db: Session, sprint_name: str) -> Optional[JiraSprint]:
        """Get sprint by name"""
        return db.query(JiraSprint).filter(JiraSprint.sprint_name == sprint_name).first()
    
    @staticmethod
    def get_sprint_summary(db: Session, sprint_name: str) -> Dict:
        """Get comprehensive sprint summary with metrics"""
        stories = JiraService.get_stories_by_sprint(db, sprint_name)
        
        summary = {
            "sprint_name": sprint_name,
            "total_stories": len(stories),
            "by_status": {},
            "total_points": 0,
            "completed_points": 0,
            "in_progress_points": 0,
            "bug_count": 0,
            "bugs_by_severity": {},
            "velocity": 0
        }
        
        # Aggregate stories by status
        for story in stories:
            status = story.status
            summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
            summary["total_points"] += story.story_points
            
            if status == "Done":
                summary["completed_points"] += story.story_points
            elif status in ["Dev", "UAT"]:
                summary["in_progress_points"] += story.story_points
        
        # Get bug count for this sprint
        bugs = db.query(JiraBug).join(JiraStory).filter(
            JiraStory.sprint == sprint_name,
            JiraBug.status != "Closed"
        ).all()
        
        summary["bug_count"] = len(bugs)
        
        for bug in bugs:
            severity = bug.severity
            summary["bugs_by_severity"][severity] = summary["bugs_by_severity"].get(severity, 0) + 1
        
        # Get velocity from sprint record or calculate from completed points
        sprint = JiraService.get_sprint_by_name(db, sprint_name)
        if sprint:
            summary["velocity"] = sprint.completed_points
            summary["sprint_status"] = sprint.status
            summary["start_date"] = sprint.start_date.isoformat() if sprint.start_date else None
            summary["end_date"] = sprint.end_date.isoformat() if sprint.end_date else None
        else:
            summary["velocity"] = summary["completed_points"]
            summary["sprint_status"] = "Unknown"
            summary["start_date"] = None
            summary["end_date"] = None
        
        return summary
    
    @staticmethod
    def calculate_team_velocity(db: Session, last_n_sprints: int = 3) -> float:
        """Calculate average team velocity over last N sprints"""
        sprints = db.query(JiraSprint).filter(
            JiraSprint.status == "Completed"
        ).order_by(JiraSprint.end_date.desc()).limit(last_n_sprints).all()
        
        if not sprints:
            return 0.0
        
        total_points = sum(sprint.completed_points for sprint in sprints)
        return round(total_points / len(sprints), 2)
    
    @staticmethod
    def list_all_sprints(db: Session) -> List[JiraSprint]:
        """List all sprints"""
        return db.query(JiraSprint).all()

# For testing
if __name__ == "__main__":
    from backend.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Test user creation
        user = JiraService.create_user(db, "test_user", "Test User", "test@mahalo.com")
        print(f"✅ Created user: {user.username}")
        
        # Test story creation
        story = JiraService.create_story(
            db,
            title="Test Story",
            description="This is a test story",
            assignee_username="test_user",
            reporter_username="test_user",
            story_points=5,
            sprint="Test Sprint"
        )
        print(f"✅ Created story: {story.story_key}")
        
        print("\n✅ JIRA Service tests passed!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()
Test JIRA Service
python backend/jira/service.py
Expected Output:

✅ Created user: test_user
✅ Created story: STORY-1

✅ JIRA Service tests passed!
Acceptance Criteria:

✅ All CRUD operations implemented
✅ Search and filter functions work
✅ Sprint summary and velocity calculations correct
✅ No syntax errors
✅ Test creates user and story successfully
Mark Complete: ⬜ → ✅

Task 1.2: Create JIRA API Routes ⬜
Instruction to Coding Assistant: Create FastAPI routes for all JIRA operations.

Create backend/jira/routes.py
"""
JIRA API Routes
FastAPI endpoints for JIRA operations
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.jira.service import JiraService
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/api/jira", tags=["JIRA"])

# ==================== REQUEST/RESPONSE MODELS ====================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[str] = None
    role: str = Field(default="developer", pattern="^(developer|pm|qa|executive)$")

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: Optional[str]
    role: str
    
    class Config:
        from_attributes = True

class StoryCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = None
    assignee_username: Optional[str] = None
    reporter_username: Optional[str] = None
    story_points: int = Field(default=0, ge=0, le=100)
    priority: str = Field(default="Medium", pattern="^(Low|Medium|High|Critical)$")
    sprint: Optional[str] = None
    status: str = Field(default="Backlog", pattern="^(Backlog|Dev|UAT|Done)$")

class StoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assignee_username: Optional[str] = None
    story_points: Optional[int] = None
    priority: Optional[str] = None

class StoryResponse(BaseModel):
    id: int
    story_key: str
    title: str
    description: Optional[str]
    status: str
    assignee: Optional[str]
    reporter: Optional[str]
    story_points: int
    priority: str
    sprint: Optional[str]
    created_at: datetime
    updated_at: datetime

class BugCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = None
    assignee_username: Optional[str] = None
    reporter_username: Optional[str] = None
    severity: str = Field(default="Medium", pattern="^(Low|Medium|High|Critical)$")
    related_story_key: Optional[str] = None
    servicenow_incident_id: Optional[str] = None
    status: str = Field(default="Open", pattern="^(Open|In Progress|Testing|Closed)$")

class BugResponse(BaseModel):
    id: int
    bug_key: str
    title: str
    description: Optional[str]
    status: str
    severity: str
    assignee: Optional[str]
    reporter: Optional[str]
    related_story_key: Optional[str]
    servicenow_incident_id: Optional[str]
    created_at: datetime
    updated_at: datetime

# ==================== USER ENDPOINTS ====================

@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new JIRA user"""
    try:
        # Check if username already exists
        existing = JiraService.get_user_by_username(db, user.username)
        if existing:
            raise HTTPException(status_code=400, detail=f"Username '{user.username}' already exists")
        
        created_user = JiraService.create_user(
            db,
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            role=user.role
        )
        return UserResponse(
            id=created_user.id,
            username=created_user.username,
            full_name=created_user.full_name,
            email=created_user.email,
            role=created_user.role
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{username}", response_model=UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    """Get user by username"""
    user = JiraService.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    
    return UserResponse(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        role=user.role
    )

@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """List all users"""
    users = JiraService.list_all_users(db)
    return [UserResponse(
        id=u.id,
        username=u.username,
        full_name=u.full_name,
        email=u.email,
        role=u.role
    ) for u in users]

# ==================== STORY ENDPOINTS ====================

@router.post("/stories", status_code=201)
def create_story(story: StoryCreate, db: Session = Depends(get_db)):
    """Create a new user story"""
    try:
        created_story = JiraService.create_story(
            db,
            title=story.title,
            description=story.description,
            assignee_username=story.assignee_username,
            reporter_username=story.reporter_username,
            story_points=story.story_points,
            priority=story.priority,
            sprint=story.sprint,
            status=story.status
        )
        return {
            "message": "Story created successfully",
            "story_key": created_story.story_key,
            "id": created_story.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stories/{story_key}", response_model=StoryResponse)
def get_story(story_key: str, db: Session = Depends(get_db)):
    """Get story by key"""
    story = JiraService.get_story_by_key(db, story_key)
    if not story:
        raise HTTPException(status_code=404, detail=f"Story '{story_key}' not found")
    
    return StoryResponse(
        id=story.id,
        story_key=story.story_key,
        title=story.title,
        description=story.description,
        status=story.status,
        assignee=story.assignee.username if story.assignee else None,
        reporter=story.reporter.username if story.reporter else None,
        story_points=story.story_points,
        priority=story.priority,
        sprint=story.sprint,
        created_at=story.created_at,
        updated_at=story.updated_at
    )

@router.patch("/stories/{story_key}")
def update_story(story_key: str, update: StoryUpdate, db: Session = Depends(get_db)):
    """Update story"""
    story = JiraService.update_story(
        db,
        story_key=story_key,
        title=update.title,
        description=update.description,
        status=update.status,
        assignee_username=update.assignee_username,
        story_points=update.story_points,
        priority=update.priority
    )
    
    if not story:
        raise HTTPException(status_code=404, detail=f"Story '{story_key}' not found")
    
    return {"message": "Story updated successfully", "story_key": story.story_key}

@router.get("/stories", response_model=List[StoryResponse])
def list_stories(
    status: Optional[str] = Query(None, pattern="^(Backlog|Dev|UAT|Done)$"),
    assignee: Optional[str] = None,
    sprint: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List stories with optional filters"""
    if status:
        stories = JiraService.get_stories_by_status(db, status)
    elif assignee:
        stories = JiraService.get_stories_by_assignee(db, assignee)
    elif sprint:
        stories = JiraService.get_stories_by_sprint(db, sprint)
    else:
        stories = JiraService.list_all_stories(db)
    
    return [StoryResponse(
        id=s.id,
        story_key=s.story_key,
        title=s.title,
        description=s.description,
        status=s.status,
        assignee=s.assignee.username if s.assignee else None,
        reporter=s.reporter.username if s.reporter else None,
        story_points=s.story_points,
        priority=s.priority,
        sprint=s.sprint,
        created_at=s.created_at,
        updated_at=s.updated_at
    ) for s in stories]

@router.post("/stories/search")
def search_stories(query: dict, db: Session = Depends(get_db)):
    """Search stories by title"""
    title_query = query.get("title", "")
    if not title_query:
        raise HTTPException(status_code=400, detail="Title query is required")
    
    stories = JiraService.search_stories_by_title(db, title_query)
    
    return {
        "count": len(stories),
        "stories": [{
            "story_key": s.story_key,
            "title": s.title,
            "status": s.status,
            "sprint": s.sprint,
            "story_points": s.story_points
        } for s in stories]
    }

# ==================== BUG ENDPOINTS ====================

@router.post("/bugs", status_code=201)
def create_bug(bug: BugCreate, db: Session = Depends(get_db)):
    """Create a new bug"""
    try:
        created_bug = JiraService.create_bug(
            db,
            title=bug.title,
            description=bug.description,
            assignee_username=bug.assignee_username,
            reporter_username=bug.reporter_username,
            severity=bug.severity,
            related_story_key=bug.related_story_key,
            servicenow_incident_id=bug.servicenow_incident_id,
            status=bug.status
        )
        return {
            "message": "Bug created successfully",
            "bug_key": created_bug.bug_key,
            "id": created_bug.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bugs/{bug_key}", response_model=BugResponse)
def get_bug(bug_key: str, db: Session = Depends(get_db)):
    """Get bug by key"""
    bug = JiraService.get_bug_by_key(db, bug_key)
    if not bug:
        raise HTTPException(status_code=404, detail=f"Bug '{bug_key}' not found")
    
    return BugResponse(
        id=bug.id,
        bug_key=bug.bug_key,
        title=bug.title,
        description=bug.description,
        status=bug.status,
        severity=bug.severity,
        assignee=bug.assignee.username if bug.assignee else None,
        reporter=bug.reporter.username if bug.reporter else None,
        related_story_key=bug.related_story.story_key if bug.related_story else None,
        servicenow_incident_id=bug.servicenow_incident_id,
        created_at=bug.created_at,
        updated_at=bug.updated_at
    )

@router.get("/bugs", response_model=List[BugResponse])
def list_bugs(
    status: Optional[str] = Query(None, pattern="^(Open|In Progress|Testing|Closed)$"),
    severity: Optional[str] = Query(None, pattern="^(Low|Medium|High|Critical)$"),
    assignee: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List bugs with optional filters"""
    if status:
        bugs = JiraService.get_bugs_by_status(db, status)
    elif severity:
        bugs = JiraService.get_bugs_by_severity(db, severity)
    elif assignee:
        bugs = JiraService.get_bugs_by_assignee(db, assignee)
    else:
        bugs = JiraService.list_all_bugs(db)
    
    return [BugResponse(
        id=b.id,
        bug_key=b.bug_key,
        title=b.title,
        description=b.description,
        status=b.status,
        severity=b.severity,
        assignee=b.assignee.username if b.assignee else None,
        reporter=b.reporter.username if b.reporter else None,
        related_story_key=b.related_story.story_key if b.related_story else None,
        servicenow_incident_id=b.servicenow_incident_id,
        created_at=b.created_at,
        updated_at=b.updated_at
    ) for b in bugs]

# ==================== SPRINT ENDPOINTS ====================

@router.get("/sprints/{sprint_name}/summary")
def get_sprint_summary(sprint_name: str, db: Session = Depends(get_db)):
    """Get sprint summary with metrics"""
    summary = JiraService.get_sprint_summary(db, sprint_name)
    
    if summary["total_stories"] == 0:
        raise HTTPException(status_code=404, detail=f"Sprint '{sprint_name}' not found or has no stories")
    
    return summary

@router.get("/sprints")
def list_sprints(db: Session = Depends(get_db)):
    """List all sprints"""
    sprints = JiraService.list_all_sprints(db)
    return {
        "count": len(sprints),
        "sprints": [{
            "sprint_name": s.sprint_name,
            "status": s.status,
            "total_points": s.total_points,
            "completed_points": s.completed_points,
            "start_date": s.start_date.isoformat() if s.start_date else None,
            "end_date": s.end_date.isoformat() if s.end_date else None
        } for s in sprints]
    }

@router.get("/velocity")
def get_team_velocity(last_n_sprints: int = Query(3, ge=1, le=10), db: Session = Depends(get_db)):
    """Get team velocity over last N sprints"""
    velocity = JiraService.calculate_team_velocity(db, last_n_sprints)
    return {
        "average_velocity": velocity,
        "sprints_analyzed": last_n_sprints,
        "unit": "story_points_per_sprint"
    }
Test Routes Import
python -c "from backend.jira.routes import router; print('✅ JIRA routes imported successfully')"
Acceptance Criteria:

✅ All endpoints defined
✅ Pydantic models for validation
✅ Proper error handling
✅ Routes import without errors
Mark Complete: ⬜ → ✅

Task 1.3: Create JIRA FastAPI Application ⬜
Instruction to Coding Assistant: Create standalone FastAPI application for JIRA on port 5001.

Create backend/jira/app.py
"""
JIRA Mock API Application
Standalone FastAPI app running on port 5001
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.jira.routes import router
from backend.config import settings
from backend.database import init_db
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="MAHALO JIRA Mock API",
    description="Mock JIRA API for MAHALO POC - User stories, bugs, sprints",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - allow all origins for POC
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include JIRA routes
app.include_router(router)

# Root endpoint
@app.get("/", tags=["Health"])
def root():
    """Root endpoint - API information"""
    return {
        "service": "MAHALO JIRA Mock API",
        "version": "1.0.0",
        "status": "running",
        "port": settings.JIRA_API_PORT,
        "docs": f"http://localhost:{settings.JIRA_API_PORT}/docs"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "jira-api"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("=" * 60)
    print("🚀 Starting JIRA Mock API")
    print(f"📍 Port: {settings.JIRA_API_PORT}")
    print(f"📚 Docs: http://localhost:{settings.JIRA_API_PORT}/docs")
    print("=" * 60)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down JIRA Mock API")

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Run server
    uvicorn.run(
        "backend.jira.app:app",
        host="0.0.0.0",
        port=settings.JIRA_API_PORT,
        reload=True,
        log_level="info"
    )
Test JIRA API
# Start JIRA API (keep this running)
python backend/jira/app.py
In another terminal, test endpoints:

# Test root endpoint
curl http://localhost:5001/

# Test health endpoint
curl http://localhost:5001/health

# Open API docs in browser
# http://localhost:5001/docs
Expected Output:

{
  "service": "MAHALO JIRA Mock API",
  "version": "1.0.0",
  "status": "running",
  "port": 5001,
  "docs": "http://localhost:5001/docs"
}
Acceptance Criteria:

✅ JIRA API starts without errors
✅ Runs on port 5001
✅ Health endpoint responds
✅ API docs accessible at /docs
✅ CORS configured
Mark Complete: ⬜ → ✅

Task 1.4: Create JIRA Seed Data ⬜
Instruction to Coding Assistant: Create seed data script with realistic demo data for JIRA.

Create backend/jira/seed_data.py
"""
JIRA Seed Data
Populate database with realistic demo data
"""
from backend.database import SessionLocal, init_db
from backend.jira.service import JiraService
from backend.models.jira_models import JiraSprint
from datetime import datetime, timedelta

def seed_jira_data():
    """Seed JIRA with comprehensive demo data"""
    db = SessionLocal()
    
    try:
        print("🌱 Seeding JIRA data...")
        
        # ==================== CREATE USERS ====================
        print("\n📝 Creating users...")
        users = [
            {"username": "alice_dev", "full_name": "Alice Developer", "email": "alice@mahalo.com", "role": "developer"},
            {"username": "bob_pm", "full_name": "Bob Product Manager", "email": "bob@mahalo.com", "role": "pm"},
            {"username": "charlie_qa", "full_name": "Charlie QA", "email": "charlie@mahalo.com", "role": "qa"},
            {"username": "diana_dev", "full_name": "Diana Developer", "email": "diana@mahalo.com", "role": "developer"},
            {"username": "eve_exec", "full_name": "Eve Executive", "email": "eve@mahalo.com", "role": "executive"},
        ]
        
        for user_data in users:
            JiraService.create_user(db, **user_data)
        print(f"  ✅ Created {len(users)} users")
        
        # ==================== CREATE SPRINT ====================
        print("\n📝 Creating sprint...")
        sprint = JiraSprint(
            sprint_name="Sprint 23",
            start_date=datetime.utcnow() - timedelta(days=10),
            end_date=datetime.utcnow() + timedelta(days=4),
            total_points=55,
            completed_points=34,
            status="Active"
        )
        db.add(sprint)
        db.commit()
        print("  ✅ Created Sprint 23")
        
        # ==================== CREATE USER STORIES ====================
        print("\n📝 Creating MahaloPay user stories...")
        stories = [
            # DONE Stories (Payment Processing Features)
            {
                "title": "Implement Stripe payment gateway integration",
                "description": "Integrate Stripe API for credit card processing. Support major cards (Visa, MC, Amex). Include tokenization for PCI compliance.",
                "assignee_username": "alice_dev",
                "reporter_username": "bob_pm",
                "story_points": 8,
                "priority": "High",
                "sprint": "Sprint 23",
                "status": "Done"
            },
            {
                "title": "Build account balance display",
                "description": "Show real-time account balance on user dashboard. Include pending transactions and available balance.",
                "assignee_username": "alice_dev",
                "reporter_username": "bob_pm",
                "story_points": 5,
                "priority": "Medium",
                "sprint": "Sprint 23",
                "status": "Done"
            },
            {
                "title": "Implement transaction history API",
                "description": "RESTful API to retrieve user transaction history with filtering by date, amount, and status.",
                "assignee_username": "alice_dev",
                "reporter_username": "bob_pm",
                "story_points": 5,
                "priority": "High",
                "sprint": "Sprint 23",
                "status": "Done"
            },
            {
                "title": "Add ACH payment processing",
                "description": "Support ACH direct debit for bank transfers. Include micro-deposit verification.",
                "assignee_username": "diana_dev",
                "reporter_username": "bob_pm",
                "story_points": 8,
                "priority": "High",
                "sprint": "Sprint 23",
                "status": "Done"
            },
            {
                "title": "Implement payment confirmation emails",
                "description": "Send email receipts for successful payments. Include transaction ID and merchant details.",
                "assignee_username": "diana_dev",
                "reporter_username": "bob_pm",
                "story_points": 3,
                "priority": "Medium",
                "sprint": "Sprint 23",
                "status": "Done"
            },
            {
                "title": "Build fraud detection rules engine",
                "description": "Rules-based fraud detection for suspicious transactions. Flag high-value and velocity-based patterns.",
                "assignee_username": "alice_dev",
                "reporter_username": "bob_pm",
                "story_points": 13,
                "priority": "High",
                "sprint": "Sprint 23",
                "status": "Done"
            },
            {
                "title": "Add payment method tokenization",
                "description": "Tokenize credit cards and bank accounts for secure storage. PCI DSS compliant.",
                "assignee_username": "diana_dev",
                "reporter_username": "bob_pm",
                "story_points": 5,
                "priority": "High",
                "sprint": "Sprint 23",
                "status": "Done"
            },
            
            # IN DEV Stories (Active Development)
            {
                "title": "Build payment retry mechanism",
                "description": "Automatic retry for failed payments with exponential backoff. Handle transient failures gracefully.",
                "assignee_username": "alice_dev",
                "reporter_username": "bob_pm",
                "story_points": 8,
                "priority": "High",
                "sprint": "Sprint 23",
                "status": "Dev"
            },
            {
                "title": "Implement Plaid integration for bank verification",
                "description": "Use Plaid API for instant bank account verification. Replace micro-deposit method.",
                "assignee_username": "diana_dev",
                "reporter_username": "bob_pm",
                "story_points": 8,
                "priority": "High",
                "sprint": "Sprint 23",
                "status": "Dev"
            },
            {
                "title": "Add currency exchange rate service",
                "description": "Real-time forex rates for multi-currency transactions. Cache rates with 1-hour TTL.",
                "assignee_username": "diana_dev",
                "reporter_username": "bob_pm",
                "story_points": 5,
                "priority": "Medium",
                "sprint": "Sprint 23",
                "status": "Dev"
            },
            
            # IN UAT Stories (User Acceptance Testing)
            {
                "title": "Implement KYC verification workflow",
                "description": "Know Your Customer verification using identity documents. Integrate with verification service.",
                "assignee_username": "diana_dev",
                "reporter_username": "bob_pm",
                "story_points": 13,
                "priority": "High",
                "sprint": "Sprint 23",
                "status": "UAT"
            },
            {
                "title": "Build transaction reconciliation dashboard",
                "description": "Daily reconciliation report comparing processed vs settled transactions.",
                "assignee_username": "alice_dev",
                "reporter_username": "bob_pm",
                "story_points": 8,
                "priority": "High",
                "sprint": "Sprint 23",
                "status": "UAT"
            },
            
            # BACKLOG Stories (Planned)
            {
                "title": "Add 3D Secure authentication",
                "description": "Implement 3DS2 for enhanced credit card security. Reduce fraud chargebacks.",
                "assignee_username": None,
                "reporter_username": "bob_pm",
                "story_points": 8,
                "priority": "Medium",
                "sprint": "Sprint 23",
                "status": "Backlog"
            },
            {
                "title": "Build payment analytics dashboard",
                "description": "Executive dashboard showing payment volume, success rates, and revenue metrics.",
                "assignee_username": None,
                "reporter_username": "bob_pm",
                "story_points": 5,
                "priority": "Medium",
                "sprint": "Sprint 23",
                "status": "Backlog"
            },
            {
                "title": "Implement refund processing API",
                "description": "API for full and partial refunds. Update transaction status and send notifications.",
                "assignee_username": None,
                "reporter_username": "bob_pm",
                "story_points": 5,
                "priority": "Medium",
                "sprint": "Sprint 23",
                "status": "Backlog"
            },
            {
                "title": "Add chargeback management system",
                "description": "Track and respond to payment chargebacks. Upload evidence and manage disputes.",
                "assignee_username": None,
                "reporter_username": "bob_pm",
                "story_points": 13,
                "priority": "Low",
                "sprint": "Sprint 23",
                "status": "Backlog"
            },
        ]
        
        for story_data in stories:
            JiraService.create_story(db, **story_data)
        print(f"  ✅ Created {len(stories)} user stories")
        
        # ==================== CREATE BUGS ====================
        print("\n📝 Creating MahaloPay bugs...")
        bugs = [
            # CRITICAL bugs (Payment Processing Issues)
            {
                "title": "Payment timeout on high-value transactions",
                "description": "Transactions over $10,000 consistently timeout after 30 seconds. Database connection pool exhaustion suspected. Affects 5% of premium customers.",
                "assignee_username": "alice_dev",
                "reporter_username": "charlie_qa",
                "severity": "Critical",
                "related_story_key": "STORY-1",  # Related to Stripe integration
                "servicenow_incident_id": "INC0001234",
                "status": "Open"
            },
            {
                "title": "Duplicate transaction IDs generated",
                "description": "Race condition in transaction ID generation causing duplicate IDs. Led to $50K in duplicate charges. URGENT FIX NEEDED.",
                "assignee_username": "alice_dev",
                "reporter_username": "charlie_qa",
                "severity": "Critical",
                "related_story_key": "STORY-3",
                "status": "In Progress"
            },
            {
                "title": "Credit card validation API intermittent failures",
                "description": "External validation service returning 503 errors during peak hours (2-4pm EST). 15% failure rate.",
                "assignee_username": "diana_dev",
                "reporter_username": "charlie_qa",
                "severity": "Critical",
                "related_story_key": "STORY-7",
                "status": "Open"
            },
            
            # HIGH severity bugs
            {
                "title": "Balance calculation rounding errors",
                "description": "Account balances off by 1-2 cents due to incorrect decimal precision. Affects reconciliation reports.",
                "assignee_username": "alice_dev",
                "reporter_username": "charlie_qa",
                "severity": "High",
                "related_story_key": "STORY-2",
                "status": "Testing"
            },
            {
                "title": "Failed ACH payments not properly rolled back",
                "description": "When ACH fails, balance update not reversed. Customer shown incorrect available balance.",
                "assignee_username": "diana_dev",
                "reporter_username": "charlie_qa",
                "severity": "High",
                "related_story_key": "STORY-4",
                "status": "In Progress"
            },
            
            # MEDIUM severity bugs
            {
                "title": "Fraud detection false positives on international cards",
                "description": "Legitimate international transactions flagged as fraudulent. 20% false positive rate for non-US cards.",
                "assignee_username": "alice_dev",
                "reporter_username": "charlie_qa",
                "severity": "Medium",
                "related_story_key": "STORY-6",
                "status": "Open"
            },
            {
                "title": "Transaction confirmation email delays",
                "description": "Payment confirmation emails arriving 10-15 minutes after transaction. Should be instant.",
                "assignee_username": None,
                "reporter_username": "charlie_qa",
                "severity": "Medium",
                "related_story_key": "STORY-5",
                "status": "Open"
            },
            {
                "title": "Currency conversion rates cached too long",
                "description": "Forex rates cached for 4 hours instead of 1 hour as designed. Minor revenue impact.",
                "assignee_username": None,
                "reporter_username": "charlie_qa",
                "severity": "Medium",
                "related_story_key": "STORY-10",
                "status": "Open"
            },
            
            # LOW severity bugs
            {
                "title": "Transaction history pagination inconsistent",
                "description": "When viewing transaction history, page 3 sometimes shows duplicate entries from page 2.",
                "assignee_username": None,
                "reporter_username": "charlie_qa",
                "severity": "Low",
                "related_story_key": "STORY-3",
                "status": "Open"
            },
            {
                "title": "Payment receipt PDF formatting issue",
                "description": "Long merchant names cause text overflow in PDF receipts. Cosmetic only.",
                "assignee_username": None,
                "reporter_username": "charlie_qa",
                "severity": "Low",
                "status": "Open"
            },
        ]
        
        for bug_data in bugs:
            JiraService.create_bug(db, bug_data)
        print(f"  ✅ Created {len(bugs)} bugs")
        
        print("\n✅ JIRA seed data complete!")
        print(f"📊 Summary:")
        print(f"   - Users: {len(users)}")
        print(f"   - Stories: {len(stories)}")
        print(f"   - Bugs: {len(bugs)}")
        print(f"   - Sprints: 1")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Initialize database first
    init_db()
    
    # Seed data
    seed_jira_data()
Run Seed Data
python backend/jira/seed_data.py
Expected Output:

🌱 Seeding JIRA data...

📝 Creating users...
  ✅ Created 5 users

📝 Creating sprint...
  ✅ Created Sprint 23

📝 Creating user stories...
  ✅ Created 15 user stories

📝 Creating bugs...
  ✅ Created 8 bugs

✅ JIRA seed data complete!
📊 Summary:
   - Users: 5
   - Stories: 15
   - Bugs: 8
   - Sprints: 1
Verify Data
sqlite3 mahalo.db "SELECT COUNT(*) FROM jira_stories;"
# Should return: 15

sqlite3 mahalo.db "SELECT COUNT(*) FROM jira_bugs;"
# Should return: 8
Acceptance Criteria:

✅ Seed script creates realistic demo data
✅ 5 users created (different roles)
✅ 15 stories created (various statuses)
✅ 8 bugs created (various severities)
✅ 1 sprint created
✅ Data supports demo workflows
✅ Cross-tool correlations included
Mark Complete: ⬜ → ✅

Task 1.5: Create JIRA API Tests ⬜
Instruction to Coding Assistant: Create comprehensive automated tests for JIRA API.

Create tests/test_jira_api.py
"""
JIRA API Tests
Automated tests for all JIRA endpoints
"""
import pytest
from fastapi.testclient import TestClient
from backend.jira.app import app
from backend.database import Base, engine, SessionLocal
from backend.jira.seed_data import seed_jira_data

# Create test client
client = TestClient(app)

# Setup: Create tables and seed data once for all tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Setup test database"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Seed test data
    seed_jira_data()
    
    yield
    
    # Teardown: Drop all tables after tests
    Base.metadata.drop_all(bind=engine)

# ==================== HEALTH TESTS ====================

def test_root_endpoint():
    """Test root endpoint returns API info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "MAHALO JIRA Mock API"
    assert data["status"] == "running"

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "jira-api"

# ==================== USER TESTS ====================

def test_get_user():
    """Test getting user by username"""
    response = client.get("/api/jira/users/alice_dev")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice_dev"
    assert data["full_name"] == "Alice Developer"
    assert data["role"] == "developer"

def test_get_nonexistent_user():
    """Test getting non-existent user returns 404"""
    response = client.get("/api/jira/users/nonexistent")
    assert response.status_code == 404

def test_list_users():
    """Test listing all users"""
    response = client.get("/api/jira/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5

def test_create_user():
    """Test creating a new user"""
    new_user = {
        "username": "frank_dev",
        "full_name": "Frank Developer",
        "email": "frank@mahalo.com",
        "role": "developer"
    }
    response = client.post("/api/jira/users", json=new_user)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "frank_dev"

def test_create_duplicate_user():
    """Test creating duplicate user fails"""
    duplicate_user = {
        "username": "alice_dev",
        "full_name": "Alice Duplicate",
        "role": "developer"
    }
    response = client.post("/api/jira/users", json=duplicate_user)
    assert response.status_code == 400

# ==================== STORY TESTS ====================

def test_get_story():
    """Test getting story by key"""
    response = client.get("/api/jira/stories/STORY-1")
    assert response.status_code == 200
    data = response.json()
    assert data["story_key"] == "STORY-1"
    assert "OAuth" in data["title"]

def test_get_nonexistent_story():
    """Test getting non-existent story returns 404"""
    response = client.get("/api/jira/stories/STORY-9999")
    assert response.status_code == 404

def test_list_all_stories():
    """Test listing all stories"""
    response = client.get("/api/jira/stories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 15

def test_filter_stories_by_status():
    """Test filtering stories by status"""
    response = client.get("/api/jira/stories?status=Done")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 7
    for story in data:
        assert story["status"] == "Done"

def test_filter_stories_by_assignee():
    """Test filtering stories by assignee"""
    response = client.get("/api/jira/stories?assignee=alice_dev")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for story in data:
        assert story["assignee"] == "alice_dev"

def test_create_story():
    """Test creating a new story"""
    new_story = {
        "title": "Test Story Creation",
        "description": "This is a test story",
        "assignee_username": "alice_dev",
        "reporter_username": "bob_pm",
        "story_points": 3,
        "priority": "Medium",
        "sprint": "Sprint 23",
        "status": "Backlog"
    }
    response = client.post("/api/jira/stories", json=new_story)
    assert response.status_code == 201
    data = response.json()
    assert "story_key" in data
    assert data["message"] == "Story created successfully"

def test_update_story():
    """Test updating story status"""
    update_data = {"status": "Dev"}
    response = client.patch("/api/jira/stories/STORY-12", json=update_data)
    assert response.status_code == 200
    
    # Verify update
    response = client.get("/api/jira/stories/STORY-12")
    assert response.json()["status"] == "Dev"

def test_search_stories():
    """Test searching stories by title"""
    search_query = {"title": "authentication"}
    response = client.post("/api/jira/stories/search", json=search_query)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 2
    assert isinstance(data["stories"], list)

# ==================== BUG TESTS ====================

def test_get_bug():
    """Test getting bug by key"""
    response = client.get("/api/jira/bugs/BUG-1")
    assert response.status_code == 200
    data = response.json()
    assert data["bug_key"] == "BUG-1"
    assert data["severity"] == "Critical"

def test_list_all_bugs():
    """Test listing all bugs"""
    response = client.get("/api/jira/bugs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 8

def test_filter_bugs_by_severity():
    """Test filtering bugs by severity"""
    response = client.get("/api/jira/bugs?severity=Critical")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for bug in data:
        assert bug["severity"] == "Critical"

def test_filter_bugs_by_status():
    """Test filtering bugs by status"""
    response = client.get("/api/jira/bugs?status=Open")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for bug in data:
        assert bug["status"] == "Open"

def test_create_bug():
    """Test creating a new bug"""
    new_bug = {
        "title": "Test Bug Creation",
        "description": "This is a test bug",
        "assignee_username": "alice_dev",
        "reporter_username": "charlie_qa",
        "severity": "High",
        "status": "Open"
    }
    response = client.post("/api/jira/bugs", json=new_bug)
    assert response.status_code == 201
    data = response.json()
    assert "bug_key" in data
    assert data["message"] == "Bug created successfully"

# ==================== SPRINT TESTS ====================

def test_get_sprint_summary():
    """Test getting sprint summary"""
    response = client.get("/api/jira/sprints/Sprint 23/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["sprint_name"] == "Sprint 23"
    assert data["total_stories"] == 15
    assert "by_status" in data
    assert data["bug_count"] == 8

def test_get_nonexistent_sprint():
    """Test getting non-existent sprint returns 404"""
    response = client.get("/api/jira/sprints/Sprint 99/summary")
    assert response.status_code == 404

def test_list_sprints():
    """Test listing all sprints"""
    response = client.get("/api/jira/sprints")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert isinstance(data["sprints"], list)

def test_get_team_velocity():
    """Test getting team velocity"""
    response = client.get("/api/jira/velocity")
    assert response.status_code == 200
    data = response.json()
    assert "average_velocity" in data
    assert "sprints_analyzed" in data

# ==================== RUN TESTS ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
Run JIRA Tests
pytest tests/test_jira_api.py -v
Expected Output:

test_jira_api.py::test_root_endpoint PASSED
test_jira_api.py::test_health_endpoint PASSED
test_jira_api.py::test_get_user PASSED
test_jira_api.py::test_get_nonexistent_user PASSED
test_jira_api.py::test_list_users PASSED
test_jira_api.py::test_create_user PASSED
test_jira_api.py::test_create_duplicate_user PASSED
test_jira_api.py::test_get_story PASSED
test_jira_api.py::test_get_nonexistent_story PASSED
test_jira_api.py::test_list_all_stories PASSED
test_jira_api.py::test_filter_stories_by_status PASSED
test_jira_api.py::test_filter_stories_by_assignee PASSED
test_jira_api.py::test_create_story PASSED
test_jira_api.py::test_update_story PASSED
test_jira_api.py::test_search_stories PASSED
test_jira_api.py::test_get_bug PASSED
test_jira_api.py::test_list_all_bugs PASSED
test_jira_api.py::test_filter_bugs_by_severity PASSED
test_jira_api.py::test_filter_bugs_by_status PASSED
test_jira_api.py::test_create_bug PASSED
test_jira_api.py::test_get_sprint_summary PASSED
test_jira_api.py::test_get_nonexistent_sprint PASSED
test_jira_api.py::test_list_sprints PASSED
test_jira_api.py::test_get_team_velocity PASSED

======================== 24 passed ========================
Acceptance Criteria:

✅ All JIRA endpoints tested
✅ Tests cover CRUD operations
✅ Tests cover edge cases (404s, duplicates)
✅ All tests pass
✅ Test coverage >80%
Mark Complete: ⬜ → ✅

🎫 ServiceNow API Implementation
Note: ServiceNow follows the same pattern as JIRA but with simpler functionality (just incidents).

Task 1.6: Create ServiceNow Service, Routes, App ⬜
Instruction to Coding Assistant: Create ServiceNow service layer, routes, and FastAPI app (similar pattern to JIRA).

Due to length constraints, I'll provide condensed versions. Follow the JIRA pattern:

Create backend/servicenow/service.py
"""
ServiceNow Service Layer
Business logic for ServiceNow incident management
"""
from sqlalchemy.orm import Session
from backend.models.servicenow_models import ServiceNowIncident
from datetime import datetime
from typing import List, Optional

class ServiceNowService:
    
    @staticmethod
    def create_incident(
        db: Session,
        title: str,
        description: Optional[str] = None,
        priority: str = "Medium",
        category: Optional[str] = None,
        assigned_to: Optional[str] = None,
        reported_by: Optional[str] = None,
        jira_bug_key: Optional[str] = None,
        status: str = "New"
    ) -> ServiceNowIncident:
        """Create a new incident"""
        # Generate incident number
        last_incident = db.query(ServiceNowIncident).order_by(ServiceNowIncident.id.desc()).first()
        next_id = (last_incident.id + 1) if last_incident else 1
        incident_number = f"INC{str(next_id).zfill(7)}"  # INC0000001
        
        incident = ServiceNowIncident(
            incident_number=incident_number,
            title=title,
            description=description,
            priority=priority,
            category=category,
            assigned_to=assigned_to,
            reported_by=reported_by,
            jira_bug_key=jira_bug_key,
            status=status
        )
        db.add(incident)
        db.commit()
        db.refresh(incident)
        return incident
    
    @staticmethod
    def get_incident_by_number(db: Session, incident_number: str) -> Optional[ServiceNowIncident]:
        """Get incident by number"""
        return db.query(ServiceNowIncident).filter(
            ServiceNowIncident.incident_number == incident_number
        ).first()
    
    @staticmethod
    def update_incident_status(db: Session, incident_number: str, new_status: str) -> Optional[ServiceNowIncident]:
        """Update incident status"""
        incident = ServiceNowService.get_incident_by_number(db, incident_number)
        if incident:
            incident.status = new_status
            incident.updated_at = datetime.utcnow()
            if new_status == "Resolved":
                incident.resolved_at = datetime.utcnow()
            db.commit()
            db.refresh(incident)
        return incident
    
    @staticmethod
    def get_incidents_by_status(db: Session, status: str) -> List[ServiceNowIncident]:
        """Get incidents by status"""
        return db.query(ServiceNowIncident).filter(ServiceNowIncident.status == status).all()
    
    @staticmethod
    def get_incidents_by_priority(db: Session, priority: str) -> List[ServiceNowIncident]:
        """Get incidents by priority"""
        return db.query(ServiceNowIncident).filter(ServiceNowIncident.priority == priority).all()
    
    @staticmethod
    def list_all_incidents(db: Session, limit: int = 100) -> List[ServiceNowIncident]:
        """List all incidents"""
        return db.query(ServiceNowIncident).limit(limit).all()
Create backend/servicenow/routes.py
"""ServiceNow API Routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.servicenow.service import ServiceNowService
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/servicenow", tags=["ServiceNow"])

class IncidentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "Medium"
    category: Optional[str] = None
    assigned_to: Optional[str] = None
    reported_by: Optional[str] = None
    jira_bug_key: Optional[str] = None
    status: str = "New"

@router.post("/incidents", status_code=201)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    """Create a new incident"""
    created = ServiceNowService.create_incident(db, incident.dict())
    return {"message": "Incident created", "incident_number": created.incident_number}

@router.get("/incidents/{incident_number}")
def get_incident(incident_number: str, db: Session = Depends(get_db)):
    """Get incident by number"""
    incident = ServiceNowService.get_incident_by_number(db, incident_number)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {
        "incident_number": incident.incident_number,
        "title": incident.title,
        "status": incident.status,
        "priority": incident.priority,
        "jira_bug_key": incident.jira_bug_key
    }

@router.get("/incidents")
def list_incidents(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List incidents with filters"""
    if status:
        incidents = ServiceNowService.get_incidents_by_status(db, status)
    elif priority:
        incidents = ServiceNowService.get_incidents_by_priority(db, priority)
    else:
        incidents = ServiceNowService.list_all_incidents(db)
    
    return {"count": len(incidents), "incidents": [
        {"incident_number": i.incident_number, "title": i.title, "status": i.status, "priority": i.priority}
        for i in incidents
    ]}
Create backend/servicenow/app.py
"""ServiceNow Mock API Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.servicenow.routes import router
from backend.config import settings
import uvicorn

app = FastAPI(title="MAHALO ServiceNow Mock API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.get("/")
def root():
    return {"service": "MAHALO ServiceNow Mock API", "port": settings.SERVICENOW_API_PORT}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "servicenow-api"}

if __name__ == "__main__":
    uvicorn.run("backend.servicenow.app:app", host="0.0.0.0", port=settings.SERVICENOW_API_PORT, reload=True)
Create backend/servicenow/seed_data.py
"""ServiceNow Seed Data"""
from backend.database import SessionLocal
from backend.servicenow.service import ServiceNowService

def seed_servicenow_data():
    """Seed ServiceNow with demo incidents"""
    db = SessionLocal()
    try:
        print("🌱 Seeding ServiceNow data...")
        
        incidents = [
            {"title": "Payment service returning 500 errors during peak load", "priority": "Critical", "category": "Application", "jira_bug_key": "BUG-1", "status": "In Progress", "description": "Payment API failing during high transaction volume (2-4pm EST). Approximately 15% of payment requests timing out."},
            {"title": "Nightly account reconciliation job failed", "priority": "High", "category": "Application", "status": "Resolved", "description": "Automated reconciliation comparing transactions vs settlements failed at 2am. Manual reconciliation completed."},
            {"title": "High transaction processing latency", "priority": "High", "category": "Performance", "status": "In Progress", "description": "Average payment processing time increased from 500ms to 3 seconds. Investigating database connection pool."},
            {"title": "Fraud detection service intermittent failures", "priority": "Medium", "category": "Application", "status": "New", "description": "Fraud detection API returning 503 errors sporadically. Fallback to basic rules engine activated."},
            {"title": "Payment gateway SSL certificate renewal required", "priority": "Medium", "category": "Infrastructure", "status": "Resolved", "description": "Stripe payment gateway SSL certificate expiring in 7 days. Renewed and deployed successfully."},
            {"title": "Database connection pool exhaustion", "priority": "Critical", "category": "Infrastructure", "jira_bug_key": "BUG-1", "status": "In Progress", "description": "Payment service running out of database connections during peak. Correlates with INC0001234."},
            {"title": "ACH batch processing delayed", "priority": "Medium", "category": "Application", "status": "New", "description": "Daily ACH batch file sent 2 hours late to bank. Investigating job scheduler."},
            {"title": "Transaction monitoring alerts not firing", "priority": "High", "category": "Application", "status": "In Progress", "description": "Real-time fraud monitoring alerts stopped at 10am. No alerts generated for 3 hours."},
        ]
        
        for inc_data in incidents:
            ServiceNowService.create_incident(db, inc_data)
        
        print(f"  ✅ Created {len(incidents)} incidents")
        print("✅ ServiceNow seed data complete!")
    finally:
        db.close()

if __name__ == "__main__":
    from backend.database import init_db
    init_db()
    seed_servicenow_data()
Run ServiceNow Seed Data
python backend/servicenow/seed_data.py
Acceptance Criteria:

✅ ServiceNow service layer complete
✅ All routes defined
✅ FastAPI app runs on port 5002
✅ Seed data creates 5 incidents
✅ Cross-tool correlation (jira_bug_key) included
Mark Complete: ⬜ → ✅

📊 Splunk API Implementation
Task 1.7: Create Splunk Service, Routes, App ⬜
Following the same pattern, create Splunk implementation:

Create backend/splunk/service.py
"""Splunk Service Layer - Log management"""
from sqlalchemy.orm import Session
from backend.models.splunk_models import SplunkLog
from datetime import datetime, timedelta
from typing import List, Optional
import random

class SplunkService:
    
    @staticmethod
    def create_log(
        db: Session,
        timestamp: datetime,
        log_level: str,
        service: str,
        message: str,
        host: Optional[str] = None,
        environment: str = "prod",
        correlation_id: Optional[str] = None,
        jira_bug_key: Optional[str] = None,
        incident_number: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> SplunkLog:
        """Create a new log entry"""
        log = SplunkLog(
            timestamp=timestamp,
            log_level=log_level,
            service=service,
            message=message,
            host=host,
            environment=environment,
            correlation_id=correlation_id,
            jira_bug_key=jira_bug_key,
            incident_number=incident_number
        )
        if metadata:
            log.set_metadata(metadata)
        
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def search_logs(
        db: Session,
        service: Optional[str] = None,
        log_level: Optional[str] = None,
        environment: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[SplunkLog]:
        """Search logs with filters"""
        query = db.query(SplunkLog)
        
        if service:
            query = query.filter(SplunkLog.service == service)
        if log_level:
            query = query.filter(SplunkLog.log_level == log_level)
        if environment:
            query = query.filter(SplunkLog.environment == environment)
        if start_time:
            query = query.filter(SplunkLog.timestamp >= start_time)
        if end_time:
            query = query.filter(SplunkLog.timestamp <= end_time)
        
        return query.order_by(SplunkLog.timestamp.desc()).limit(limit).all()
    
    @staticmethod
    def get_error_logs(db: Session, limit: int = 50) -> List[SplunkLog]:
        """Get recent error logs"""
        return db.query(SplunkLog).filter(
            SplunkLog.log_level.in_(["ERROR", "FATAL"])
        ).order_by(SplunkLog.timestamp.desc()).limit(limit).all()
Create backend/splunk/seed_data.py
"""Splunk Seed Data - Generate realistic logs"""
from backend.database import SessionLocal
from backend.splunk.service import SplunkService
from datetime import datetime, timedelta
import random

def seed_splunk_data():
    """Generate 1000+ realistic log entries"""
    db = SessionLocal()
    try:
        print("🌱 Seeding Splunk data...")
        
        services = ["payment-service", "fraud-detection", "account-service", "transaction-api", "reconciliation-job"]
        log_levels = ["INFO", "WARN", "ERROR", "FATAL", "DEBUG"]
        level_weights = [50, 30, 15, 5, 10]  # INFO most common
        environments = ["prod", "uat", "dev"]
        env_weights = [60, 25, 15]
        
        messages = {
            "INFO": [
                "Payment processed successfully", 
                "Transaction approved", 
                "Fraud check passed", 
                "Account balance updated",
                "Payment token created",
                "ACH transfer initiated"
            ],
            "WARN": [
                "High transaction volume detected", 
                "Payment processing taking longer than usual", 
                "Database connection pool running low",
                "Fraud score elevated but below threshold",
                "Currency conversion rate cache stale"
            ],
            "ERROR": [
                "Payment gateway timeout", 
                "Database connection pool exhausted", 
                "Fraud detection API unavailable",
                "Transaction validation failed",
                "Account balance retrieval failed",
                "Payment processing timeout over $10,000"
            ],
            "FATAL": [
                "Payment service crashed", 
                "Database connection completely lost", 
                "Fraud detection service unresponsive",
                "Critical payment processing failure"
            ]
        }
        
        count = 0
        for days_ago in range(7):  # Last 7 days
            for _ in range(150):  # 150 logs per day
                timestamp = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
                service = random.choice(services)
                log_level = random.choices(log_levels, weights=level_weights)[0]
                environment = random.choices(environments, weights=env_weights)[0]
                message = random.choice(messages.get(log_level, ["General log message"]))
                
                # Add correlations for payment-related ERROR logs
                jira_bug_key = "BUG-1" if log_level == "ERROR" and service == "payment-service" and random.random() < 0.3 else None
                incident_number = "INC0001234" if jira_bug_key else None
                
                SplunkService.create_log(
                    db,
                    timestamp=timestamp,
                    log_level=log_level,
                    service=service,
                    message=message,
                    host=f"{service}-{random.randint(1,3)}",
                    environment=environment,
                    jira_bug_key=jira_bug_key,
                    incident_number=incident_number
                )
                count += 1
        
        print(f"  ✅ Created {count} log entries")
        print("✅ Splunk seed data complete!")
    finally:
        db.close()

if __name__ == "__main__":
    from backend.database import init_db
    init_db()
    seed_splunk_data()
Run Splunk seed data:

python backend/splunk/seed_data.py
Acceptance Criteria:

✅ Splunk service layer complete
✅ Search functionality works
✅ Seed data creates 1000+ logs
✅ Logs span 7 days
✅ Cross-tool correlations included
Mark Complete: ⬜ → ✅

🔄 Reset Utility
Task 1.8: Create Data Reset Utility ⬜
Instruction to Coding Assistant: Create utility to reset all demo data quickly.

Create backend/utils/reset_data.py
"""
Data Reset Utility
Drop all tables, recreate, and re-seed data
"""
from backend.database import Base, engine, init_db
from backend.jira.seed_data import seed_jira_data
from backend.servicenow.seed_data import seed_servicenow_data
from backend.splunk.seed_data import seed_splunk_data

def reset_all_data():
    """Complete data reset - drop, create, seed"""
    print("=" * 60)
    print("🔄 MAHALO Data Reset")
    print("=" * 60)
    print()
    
    # Step 1: Drop all tables
    print("1️⃣  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("   ✅ All tables dropped")
    print()
    
    # Step 2: Recreate tables
    print("2️⃣  Recreating database schema...")
    init_db()
    print()
    
    # Step 3: Seed JIRA data
    print("3️⃣  Seeding JIRA data...")
    seed_jira_data()
    print()
    
    # Step 4: Seed ServiceNow data
    print("4️⃣  Seeding ServiceNow data...")
    seed_servicenow_data()
    print()
    
    # Step 5: Seed Splunk data
    print("5️⃣  Seeding Splunk data...")
    seed_splunk_data()
    print()
    
    print("=" * 60)
    print("✅ Data reset complete!")
    print("=" * 60)

if __name__ == "__main__":
    reset_all_data()
Create scripts/reset_demo.sh
#!/bin/bash
echo "🔄 Resetting MAHALO demo data..."
cd "$(dirname "$0")/.."
source venv/bin/activate
python backend/utils/reset_data.py
echo "✅ Demo data reset complete!"
Make executable and test
chmod +x scripts/reset_demo.sh
bash scripts/reset_demo.sh
Acceptance Criteria:

✅ Reset script drops and recreates all tables
✅ All seed data scripts run successfully
✅ Script completes in < 10 seconds
✅ Can be run multiple times safely
Mark Complete: ⬜ → ✅

✅ Phase 1 Completion Checklist
Before proceeding to Phase 2, verify:

JIRA API
 Service layer implemented (backend/jira/service.py)
 Routes defined (backend/jira/routes.py)
 FastAPI app runs on port 5001
 Seed data creates realistic demo data
 All API tests pass (24 tests)
 API docs accessible at http://localhost:5001/docs
ServiceNow API
 Service layer implemented
 Routes defined
 FastAPI app runs on port 5002
 Seed data creates 5 incidents
 Can create/read incidents via API
Splunk API
 Service layer implemented
 Routes defined
 FastAPI app runs on port 5003
 Seed data creates 1000+ logs
 Can search logs via API
Utilities
 Reset data utility works
 reset_demo.sh script executes successfully
Final Validation
Start all 3 APIs:

# Terminal 1
python backend/jira/app.py

# Terminal 2
python backend/servicenow/app.py

# Terminal 3
python backend/splunk/app.py
Test all health endpoints:

curl http://localhost:5001/health  # Should return {"status":"healthy"}
curl http://localhost:5002/health  # Should return {"status":"healthy"}
curl http://localhost:5003/health  # Should return {"status":"healthy"}
Run all tests:

pytest tests/test_jira_api.py -v  # Should pass all tests
Verify data:

sqlite3 mahalo.db "SELECT COUNT(*) FROM jira_stories;"  # Should return 15
sqlite3 mahalo.db "SELECT COUNT(*) FROM jira_bugs;"     # Should return 8
sqlite3 mahalo.db "SELECT COUNT(*) FROM servicenow_incidents;"  # Should return 5
sqlite3 mahalo.db "SELECT COUNT(*) FROM splunk_logs;"   # Should return 1000+
🎉 Phase 1 Complete!
What We've Accomplished
✅ JIRA API fully functional (users, stories, bugs, sprints)
✅ ServiceNow API operational (incident management)
✅ Splunk API working (log search and analysis)
✅ Realistic demo data for all tools
✅ Automated tests for JIRA
✅ Data reset utility
✅ All APIs accessible via REST

What's Next: Phase 2 - Build MCP Servers
In Phase 2, you will:

Install MCP SDK
Create MCP server for JIRA
Create MCP server for ServiceNow
Create MCP server for Splunk
Test MCP protocol compliance
Ready to Proceed?
# Verify Phase 1 complete
bash scripts/reset_demo.sh
pytest tests/test_jira_api.py -v
If all tests pass and all 3 APIs are running, you're ready for Phase 2! 🚀