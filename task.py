
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import logging
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func,case, and_
from urllib.parse import quote_plus
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends
from datetime import datetime, timezone
# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Database connection configuration
DB_HOST = "10.19.71.176"
DB_NAME = "alarms"
DB_USER = "psqladm"
DB_PORT = "5432"
DB_PASSWORD = "R%e6DgyQ"

# URL-encode the password to handle special characters properly
encoded_password = quote_plus(DB_PASSWORD)

# Build the DATABASE_URL for SQLAlchemy
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=False)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for ORM models
Base = declarative_base()

app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Setup the database
DATABASE_URL = "postgresql://username:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Pydantic Models (for request validation)
class ScheduleData(BaseModel):
    nssid: str
    tentative_start_date: str
    tentative_end_date: str
    users: List[int]

class TaskCreateRequest(BaseModel):
    schedule_data: List[ScheduleData]

# DB Models
class TaskStatus(Base):
    __tablename__ = "task_status"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "task"
    task_id = Column(Integer, primary_key=True, index=True)
    created_by = Column(Integer)
    task_planner_id = Column(Integer)
    status = Column(Integer, ForeignKey('task_status.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class TicketStatus(Base):
    __tablename__ = "ticket_status"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Ticket(Base):
    __tablename__ = "ticket"
    ticket_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('task.task_id'))
    assigned_by = Column(Integer)
    nssid = Column(String, ForeignKey('sites.nssid'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Integer, ForeignKey('ticket_status.id'))

class Site(Base):
    __tablename__ = "sites"
    site_id = Column(Integer, primary_key=True, index=True)
    nssid = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app initialization
app = FastAPI()

# Endpoint to create tasks and tickets from the input
@app.post("/create_tasks_and_tickets/")
def create_tasks_and_tickets(request: TaskCreateRequest, db: Session = Depends(get_db)):
    try:
        # Fetch "Scheduled" status for task and ticket statuses from the database
        task_status = db.query(TaskStatus).filter(TaskStatus.status == "Scheduled").first()
        if not task_status:
            raise HTTPException(status_code=404, detail="Task status 'Scheduled' not found.")
        
        ticket_status = db.query(TicketStatus).filter(TicketStatus.status == "Scheduled").first()
        if not ticket_status:
            raise HTTPException(status_code=404, detail="Ticket status 'Scheduled' not found.")

        # Iterate over schedule data to create tasks and tickets
        for schedule in request.schedule_data:
            # Create task with 'Scheduled' status
            task = Task(
                created_by=1,  # Example user ID, this can be dynamic
                task_planner_id=1,  # Example planner ID, this can be dynamic
                status=task_status.id,  # Set 'Scheduled' status for the task
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            db.add(task)
            db.commit()
            db.refresh(task)

            # Create ticket for each user in the schedule
            for user_id in schedule.users:
                ticket = Ticket(
                    task_id=task.task_id,
                    assigned_by=1,  # Example assigned by user, this can be dynamic
                    nssid=schedule.nssid,
                    start_date=datetime.strptime(schedule.tentative_start_date, "%Y-%m-%d"),
                    end_date=datetime.strptime(schedule.tentative_end_date, "%Y-%m-%d"),
                    comment="Task for user " + str(user_id),  # Custom comment
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                    status=ticket_status.id  # Set 'Scheduled' status for the ticket
                )
                db.add(ticket)
                db.commit()
                db.refresh(ticket)

        return {"message": "Tasks and tickets created successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


######### 

# 08/01/25
# Meeting with tarun  and mayank for scheduling .ScheduleData
# worked on shceduling api . and its filter apis 
# worked on inventory api for new circle code and transport data fixing .
# worked on task and ticket apis     