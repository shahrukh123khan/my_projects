from sqlalchemy.orm import Session, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from urllib.parse import quote_plus
import logging

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

# Create FastAPI instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (modify as needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define Base
Base = declarative_base()

# Database Models

class Subzones(Base):
    __tablename__ = "subzones"
    subzone_id = Column(Integer, primary_key=True, index=True)
    subzone_name = Column(String)
    zone_id = Column(Integer, ForeignKey("zones.zone_id"))
    zone = relationship("Zones", back_populates="subzones")
    assigned_subzones = relationship("AssignedSubzone", back_populates="subzone")  # Add this

class Zones(Base):
    __tablename__ = "zones"
    zone_id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String)
    circle_id = Column(Integer, ForeignKey("circle.circle_id"))
    subzones = relationship("Subzones", back_populates="zone")
    circle = relationship("Circle", back_populates="zones")  # Add this

class Circle(Base):
    __tablename__ = "circle"
    circle_id = Column(Integer, primary_key=True, index=True)
    circle_name = Column(String)
    zones = relationship("Zones", back_populates="circle")
    assigned_circles = relationship("AssignedCircle", back_populates="circle")

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_id_extra = Column(String, nullable=True)  # Assuming it's a string; adjust as needed
    user_name = Column(String, nullable=False, unique=True)  # Unique for login purposes
    full_name = Column(String, nullable=True)  # Optional full name
    email = Column(String, nullable=False, unique=True)  # Unique for email
    is_active = Column(Integer, default=1)  # Assuming 1 for active, 0 for inactive
    is_hide = Column(Integer, default=0)  # Assuming 1 for hidden, 0 for visible
    hpsm_user_id = Column(String, nullable=True)  # HPSM User ID
    wfms_user_id = Column(String, nullable=True)  # WFMS User ID
    vms_user_id = Column(String, nullable=True)  # VMS User ID
    created_at = Column(DateTime, default=func.now())  # Timestamp for creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Timestamp for updates
    assigned_circles = relationship("AssignedCircle", back_populates="user")
    assigned_subzones = relationship("AssignedSubzone", back_populates="user")

class AssignedSubzone(Base):
    __tablename__ = "assigned_subzones"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))  # ForeignKey to Users table
    subzone_id = Column(Integer, ForeignKey("subzones.subzone_id"))  # ForeignKey to Subzones table
    created_at = Column(DateTime, default=func.now())  # Timestamp for assignment creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Timestamp for updates

    # Relationships to access user and subzone data
    user = relationship("Users", back_populates="assigned_subzones")
    subzone = relationship("Subzones", back_populates="assigned_subzones")

class AssignedCircle(Base):
    __tablename__ = "assigned_circles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # Foreign key to Users table
    circle_id = Column(Integer, ForeignKey("circle.circle_id"), nullable=False)  # Foreign key to Circle table
    created_at = Column(DateTime, default=func.now())  # Timestamp for creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Timestamp for updates

    # Relationships
    user = relationship("Users", back_populates="assigned_circles")
    circle = relationship("Circle", back_populates="assigned_circles")


class UserResponse(BaseModel):
    user_name: Optional[str] = None
    user_id: Optional[int] = None


    class Config:
        from_attributes = True


@app.post("/users", response_model=List[UserResponse])
def get_users(request: dict, db: Session = Depends(get_db)):

    try:
        subzone_id = request.get("subzone_id", None)  # New filter for zone_id
        user_name = request.get("user_name", None)

        # Log the incoming request
        logging.debug(f"Request Received: {request}")

        # Base query
        query = db.query(Users)

        # Apply filters from the request payload
        if user_name:
            logging.debug(f"Filtering by subzone name starting with: {user_name}")
            query = query.filter(Users.user_name.ilike(f"{user_name}%"))
        
        
        if subzone_id:
            logging.debug(f"Filtering by subzone_id: {request['subzone_id']}")
            # Apply join with AssignedSubzone table to filter by subzone_id
            query = query.join(AssignedSubzone).filter(AssignedSubzone.subzone_id == subzone_id)

        # Apply default limit
        #query = query.limit(20)

        # Log the query for debugging
        logging.debug(f"Generated Query: {query}")

        # Execute the query and fetch results
        results = query.all()
        logging.debug(f"Query Results: {results}")

        if not results:
            logging.debug("No subzones found for the given filters.")
        return results

    except Exception as e:
        logging.error(f"Error fetching subzones: {e}")
        return {"error": str(e)}











