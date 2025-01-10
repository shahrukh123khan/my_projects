import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from urllib.parse import quote_plus
from pydantic import BaseModel
from typing import List
from datetime import datetime

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

class Equipment(Base):
    __tablename__ = "equipments"
    equipment_id = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String)
    site_id = Column(Integer, ForeignKey("sites.site_id"))
    domain_id = Column(Integer, ForeignKey("domain.domain_id"))


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

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_id_extra = Column(Integer)
    user_name = Column(String)
    full_name = Column(String)
    email = Column(String)
    is_active = Column(Boolean)
    is_hide = Column(Boolean)
    hpsm_user_id = Column(Integer)
    
class AssignedSubzone(Base):
    __tablename__ = "assigned_subzones"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    subzone_id = Column(Integer)

class EquipmentInfo(BaseModel):
    equipment_name: str
    vendor_name: str
    domain_name: str


# Pydantic response schema
class DomainDataResponse(BaseModel):
    domain_name: str
    domaintype_name: str
    category_name: str
    site_type_name: str
    site_group_name: str
    frequency_name: str
    site_name: str
    subzone_name: str
    zone_name: str
    circle_name: str
    equipment_count: int
    # node_name: str
    # vendor_name: str
    equipment_info: List[EquipmentInfo]
    # domain: str
    # latitude: float
    # longitude: float

    class Config:
        ofrom_attributes = True

# FastAPI app instance
app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoint
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List

# API endpoint
    
from sqlalchemy.sql import func
@app.get("/domain_data/", response_model=List[DomainDataResponse])
def get_domain_data(domaintype_id: int, db: Session = Depends(get_db)):
    try:
        # Modified query to include vendor name and fix grouping issues
        query = db.query(
            Domain.domain_name,
            DomainType.domaintype_name,
            Category.category_name,
            SiteType.site_type_name,
            SiteGroup.site_group_name,
            YearlyFrequency.frequency_name,
            Sites.nssid.label("site_name"),
            Subzones.subzone_name,
            Zones.zone_name,
            Circle.circle_name,
            func.count(Equipment.equipment_id).label("equipment_count"),
            Vendors.vendor_name,
            Equipment.equipment_name.label("node_name")  # Include the equipment name
        ).join(
            DomainType, Domain.domaintype_id == DomainType.domaintype_id
        ).join(
            Category, Domain.category_id == Category.category_id
        ).join(
            YearlyFrequency, Category.category_id == YearlyFrequency.category_id
        ).join(
            SiteType, YearlyFrequency.frequency_id == SiteType.frequency_id
        ).join(
            SiteGroup, SiteType.site_group_id == SiteGroup.site_group_id
        ).join(
            Sites, SiteType.site_id == Sites.site_id
        ).join(
            Equipment, Equipment.site_id == Sites.site_id  # Correct join condition
        ).join(
            Vendors, Vendors.domain_id == Domain.domain_id
        ).join(
            Subzones, Sites.subzone_id == Subzones.subzone_id
        ).join(
            Zones, Subzones.zone_id == Zones.zone_id
        ).join(
            Circle, Zones.circle_id == Circle.circle_id
        ).filter(
            Domain.domaintype_id == domaintype_id
        ).group_by(  # Group by all the necessary columns
            Domain.domain_name,
            DomainType.domaintype_name,
            Category.category_name,
            SiteType.site_type_name,
            SiteGroup.site_group_name,
            YearlyFrequency.frequency_name,
            Sites.nssid,
            Subzones.subzone_name,
            Zones.zone_name,
            Circle.circle_name,
            Vendors.vendor_name,
            Equipment.equipment_name  # Include equipment name in the group by
        ).all()

        if not query:
            raise HTTPException(status_code=404, detail="No data found")

        # Prepare the response with equipment info
        response = []
        for record in query:
            # Build the equipment info for each site
            equipment_info = {
                "equipment_name": record.node_name,  # Adjusted to match 'node_name'
                "vendor_name": record.vendor_name or "None",
                "domain_name": record.domain_name
            }

            # Check if the site already exists in the response
            domain_data = next((item for item in response if item['site_name'] == record.site_name), None)
            
            if domain_data:
                domain_data['equipment_info'].append(equipment_info)  # Append equipment info
            else:
                # Create new entry for the site
                response.append(
                    {
                        "domain_name": record.domain_name,
                        "domaintype_name": record.domaintype_name,
                        "category_name": record.category_name,
                        "site_type_name": record.site_type_name,
                        "site_group_name": record.site_group_name,
                        "frequency_name": record.frequency_name,
                        "site_name": record.site_name,
                        "subzone_name": record.subzone_name,
                        "zone_name": record.zone_name,
                        "circle_name": record.circle_name,
                        "equipment_count": 1,  # Initial equipment count
                        "equipment_info": [equipment_info]  # Start with the first equipment
                    }
                )

        # Update the equipment count after aggregating the data
        for domain_data in response:
            domain_data['equipment_count'] = len(domain_data['equipment_info'])

        return response

    except (SQLAlchemyError, OperationalError) as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")