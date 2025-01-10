
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import logging
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from urllib.parse import quote_plus
from collections import defaultdict
from sqlalchemy.orm import Session, aliased
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import create_engine
import logging
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import joinedload
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
    #allow_origins=["http://frontend-domain.com", "http://localhost:3000"],  # Frontend origins
    allow_origins=["*"],  # Frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

# Define ORM models
class Vendors(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True)
    vendor_name = Column(String)
    domain_id = Column(Integer, ForeignKey("domain.domain_id"))
    equipments = relationship("Equipment", back_populates="vendor")

class Equipment(Base):
    __tablename__ = "equipments"
    equipment_id = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String)
    site_id = Column(Integer, ForeignKey("sites.site_id"))
    domain_id = Column(Integer, ForeignKey("domain.domain_id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    # Defining relationship from Equipment to Vendors
    vendor = relationship("Vendors", back_populates="equipments")
class DomainType(Base):
    __tablename__ = "domain_type"
    domaintype_id = Column(Integer, primary_key=True, index=True)
    domaintype_name = Column(String, index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    domains = relationship("Domain", back_populates="domain_type")

class Domain(Base):
    __tablename__ = "domain"
    domain_id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String, index=True)
    domaintype_id = Column(Integer, ForeignKey("domain_type.domaintype_id"))
    category_id = Column(Integer, ForeignKey("category.category_id"))
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    domain_type = relationship("DomainType", back_populates="domains")
    category = relationship("Category", back_populates="domains")

class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)
    category_no = Column(Integer)
    domains = relationship("Domain", back_populates="category")
    frequencies = relationship("YearlyFrequency", back_populates="category")
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

class YearlyFrequency(Base):
    __tablename__ = "yearly_frequency"
    frequency_id = Column(Integer, primary_key=True, index=True)
    frequency_name = Column(String)
    frequency_count = Column(Integer)
    category_id = Column(Integer, ForeignKey("category.category_id"))
    category = relationship("Category", back_populates="frequencies")
    site_types = relationship("SiteType", back_populates="frequency")
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

class SiteType(Base):
    __tablename__ = "site_type"
    site_type_id = Column(Integer, primary_key=True, index=True)
    site_type_name = Column(String)
    frequency_id = Column(Integer, ForeignKey("yearly_frequency.frequency_id"))
    site_group_id = Column(Integer, ForeignKey("site_group.site_group_id"))
    site_id = Column(Integer, ForeignKey("sites.site_id"))
    frequency = relationship("YearlyFrequency", back_populates="site_types")
    site_group = relationship("SiteGroup", back_populates="site_types")
    site = relationship("Sites", back_populates="site_types")

class SiteGroup(Base):
    __tablename__ = "site_group"
    site_group_id = Column(Integer, primary_key=True, index=True)
    site_group_name = Column(String)
    site_types = relationship("SiteType", back_populates="site_group")

class Sites(Base):
    __tablename__ = "sites"
    site_id = Column(Integer, primary_key=True, index=True)
    nssid = Column(String)
    subzone_id = Column(Integer, ForeignKey("subzones.subzone_id"))
    site_types = relationship("SiteType", back_populates="site")
    subzone = relationship("Subzones", back_populates="sites")  # Correct relationship to Subzones

class Subzones(Base):
    __tablename__ = "subzones"
    subzone_id = Column(Integer, primary_key=True, index=True)
    subzone_name = Column(String)
    zone_id = Column(Integer, ForeignKey("zones.zone_id"))
    sites = relationship("Sites", back_populates="subzone")
    zone = relationship("Zones", back_populates="subzones")

class Zones(Base):
    __tablename__ = "zones"
    zone_id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String)
    circle_id = Column(Integer, ForeignKey("circle.circle_id"))
    subzones = relationship("Subzones", back_populates="zone")
    circle = relationship("Circle", back_populates="zones")  # Correct relationship to Circle

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
    # Relationships can be defined here if needed, for example:
    # assigned_circles = relationship("AssignedCircles", back_populates="users")

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


from pydantic import BaseModel, Field

# class EquipmentInfo(BaseModel):
#     equipment_name: str
#     vendor_name: str
#     domain_name: str


# class DomainDataResponse(BaseModel):
#     nssid: str
#     subzone_name: str
#     zone_name: str
#     circle_name: str
#     user_name: str
#     equipment_count: int
#     equipment_info: List[EquipmentInfo]

#     class Config:
#         from_attributes = True

# FastAPI app instance
app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/data")
def get_data_by_circle_zone_subzone(
    circle_id: int = None,
    zone_id: int = None,
    subzone_id: int = None,
    db: Session = Depends(get_db),
):
    query = db.query(Circle).options(
        joinedload(Circle.zones)
        .joinedload(Zones.subzones)
        .joinedload(Subzones.sites)
    )
    
    # Applying filters if the parameters are provided
    if circle_id:
        query = query.filter(Circle.circle_id == circle_id)
    
    if zone_id:
        query = query.filter(Zones.zone_id == zone_id)
    
    if subzone_id:
        query = query.filter(Subzones.subzone_id == subzone_id)
    
    return query.all()
