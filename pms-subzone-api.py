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


class Zones(Base):
    __tablename__ = "zones"
    zone_id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String)
    circle_id = Column(Integer, ForeignKey("circle.circle_id"))
    subzones = relationship("Subzones", back_populates="zone")


class Circle(Base):
    __tablename__ = "circle"
    circle_id = Column(Integer, primary_key=True, index=True)
    circle_name = Column(String)
    zones = relationship("Zones", back_populates="circle")

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



class SubzoneRequest(BaseModel):
    user_name: Optional[str] = None
    subzone_id: Optional[int] = None


    class Config:
        from_attributes = True


@app.post("/subzones", response_model=List[SubzoneRequest])
def get_subzones(request: dict, db: Session = Depends(get_db)):

    try:
        # Log the incoming request
        logging.debug(f"Request Received: {request}")

        # Base query
        query = db.query(Subzones)

        # Apply filters from the request payload
        if request.subzone_name:
            logging.debug(f"Filtering by subzone name starting with: {request.subzone_name}")
            query = query.filter(Subzones.subzone_name.ilike(f"{request.subzone_name}%"))
        if request.zone_id:
            logging.debug(f"Filtering by zone_id: {request.zone_id}")
            query = query.filter(Subzones.zone_id == request.zone_id)

        # Apply default limit
        query = query.limit(20)

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

# @app.post("/subzones", response_model=List[SubzoneResponse])
# def get_subzones(request: SubzoneRequest, db: Session = Depends(get_db)):

#     try:
#         # Log the incoming request
#         logging.debug(f"Request Received: {request}")

#         # Base query
#         query = db.query(Subzones)

#         # Apply filters from the request payload
#         if request.subzone_name:
#             logging.debug(f"Filtering by subzone name starting with: {request.subzone_name}")
#             query = query.filter(Subzones.subzone_name.ilike(f"{request.subzone_name}%"))
#         if request.zone_id:
#             logging.debug(f"Filtering by zone_id: {request.zone_id}")
#             query = query.filter(Subzones.zone_id == request.zone_id)

#         # Apply default limit
#         query = query.limit(20)

#         # Log the query for debugging
#         logging.debug(f"Generated Query: {query}")

#         # Execute the query and fetch results
#         results = query.all()
#         logging.debug(f"Query Results: {results}")

#         if not results:
#             logging.debug("No subzones found for the given filters.")
#         return results

#     except Exception as e:
#         logging.error(f"Error fetching subzones: {e}")
#         return {"error": str(e)}



