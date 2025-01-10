
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
import requests
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

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app initialization
app = FastAPI()

  
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
   

class SiteUsers(Base):
    __tablename__ = "site_users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))  # Assuming there is a 'users' table with 'user_id' column
    manager_id = Column(Integer)  # Assuming managers are also in the 'users' table
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Define relationships
    user = relationship("Users", foreign_keys=[user_id]) 

class UserResponse(BaseModel):
    total_count : int
    user_id: int
    user_name: str
    manager_id: int

    class Config:
        from_attributes = True
class UsersListResponse(BaseModel):
    total_count: int
    limit: int
    offset: int
    data: List[UserResponse]

@app.post("/site_users", response_model=UsersListResponse)
def get_users(request: dict, db: Session = Depends(get_db)):
    manager_id = request.get("manager_id", 1)
    limit = request.get("limit", 10)
    offset = request.get("offset", 0)
    query = db.query(Users.user_id, Users.user_name, SiteUsers.manager_id).join(
        SiteUsers, Users.user_id == SiteUsers.user_id
    ).filter(SiteUsers.manager_id == manager_id)
    total_count=query.count()
    final_result = query.offset(offset).limit(limit).all()
    
    return {
        "total_count":total_count,
        "limit": limit,
        "offset": offset,
        "data": final_result
    }




# select u.user_id,u.user_name from users u
# join site_users su on u.user_id =su.user_id
# JOIN assigned_subzones asub ON asub.user_id = su.manager_id
# where asub.subzone_id=3




# select u.user_id,u.user_name,su.manager_id from users u
# join site_users su on u.user_id =su.user_id
# where su.manager_id=1

