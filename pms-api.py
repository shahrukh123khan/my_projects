from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import logging
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from urllib.parse import quote_plus
from collections import defaultdict
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict
from typing import Optional
from pydantic import BaseModel, model_validator
from fastapi import HTTPException

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
   
class Equipment(Base):
    __tablename__ = "equipments"
    equipment_id = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String)
    site_id = Column(Integer, ForeignKey("sites.site_id"))
    is_active = Column(Integer, default=1)  
    domain_id=Column(Integer)
    vendor_id=Column(Integer)
    created_at = Column(DateTime, default=func.now())  
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  

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
    frequency = relationship("YearlyFrequency", back_populates="site_types")
    site_group = relationship("SiteGroup", back_populates="site_types")
    category_id = Column(Integer)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

class SiteGroup(Base):
    __tablename__ = "site_group"
    site_group_id = Column(Integer, primary_key=True, index=True)
    site_group_name = Column(String)
    site_types = relationship("SiteType", back_populates="site_group")
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

class Sites(Base):
    __tablename__ = "sites"
    site_id = Column(Integer, primary_key=True, index=True)
    nssid = Column(String)
    subzone_id = Column(Integer, ForeignKey("subzones.subzone_id"))
    #category_id = Column(Integer, ForeignKey("category.category_id"))
    category_id = Column(Integer)
    #category = relationship("Category", back_populates="categories")  # Correct relationship to Subzones
    subzone = relationship("Subzones", back_populates="sites")  # Correct relationship to Subzones
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
class Subzones(Base):
    __tablename__ = "subzones"
    subzone_id = Column(Integer, primary_key=True, index=True)
    subzone_name = Column(String)
    zone_id = Column(Integer, ForeignKey("zones.zone_id"))
    sites = relationship("Sites", back_populates="subzone")
    zone = relationship("Zones", back_populates="subzones")
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
class Zones(Base):
    __tablename__ = "zones"
    zone_id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String)
    circle_id = Column(Integer, ForeignKey("circle.circle_id"))
    subzones = relationship("Subzones", back_populates="zone")
    circle = relationship("Circle", back_populates="zones")  # Correct relationship to Circle
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
class Circle(Base):
    __tablename__ = "circle"
    circle_id = Column(Integer, primary_key=True, index=True)
    circle_name = Column(String)
    zones = relationship("Zones", back_populates="circle")
    assigned_circles = relationship("AssignedCircle", back_populates="circle")
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
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


   
class AssignedSubzone(Base):
    __tablename__ = "assigned_subzones"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # Foreign key to Users table
    subzone_id = Column(Integer, ForeignKey("subzone.subzone_id"), nullable=False)  # Foreign key to Circle table
    created_at = Column(DateTime, default=func.now())  # Timestamp for creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Timestamp for updates

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

class EquipmentInfo(BaseModel):
    # equipment_name: str[]
    # vendor_name: str
    # domain_name: str
    equipment_name :Optional[str] = None 
    vendor_name: Optional[str] = None  # Make vendor_name optional
    domain_name: Optional[str] = None  # Make domain_name optional
    
   

# Pydantic model for response
class DomainDataResponse(BaseModel):
    # domain_name: str
    # domaintype_name : str
    # domaintype_id: int
    category_no: int
    site_type_name: str
    site_group_name: str
    frequency_no: int
    nssid: str
    subzone_name: str
    zone_name: str
    circle_name: str
    user_name: str
    last_activity: str = Field(default=None)
    completed_activity: str = Field(default=None)
    equipment_count: int  # New field for equipment count
    equipment_info: List[EquipmentInfo]  # List of equipment details


    class Config:
        from_attributes = True
class PmsInventoryResponse(BaseModel):
    totalRecords: int
    limit: int
    offset: int
    data: List[DomainDataResponse]
# FastAPI app instance
app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/pms-inventory", response_model=PmsInventoryResponse)
def get_inventory(request: dict, db: Session = Depends(get_db)):
    domaintype_name = request.get("domaintype_name", "Mobility").lower()
    print("domain type name ",domaintype_name)
    circle_id = request.get("circle_id", None)
    zone_id = request.get("zone_id", None)
    subzone_id = request.get("subzone_id", None)
    user_id = request.get("user_id", None) 
    limit = request.get("limit",20)  
    offset = request.get("offset", 0) 
    base_query = db.query(
        Domain.category_id.label("category_no")
    ).join(
        DomainType, Domain.domaintype_id == DomainType.domaintype_id
    ).filter(
        func.lower(DomainType.domaintype_name) == domaintype_name
    ).group_by(
        Domain.category_id
    )
    result = base_query.all()  
    print("result",result)
    category_no = int(result[0][0])

    query = db.query(
        Circle.circle_name.label("circle_name"),
        Zones.zone_name.label("zone_name"),
        Subzones.subzone_name.label("subzone_name"),
        Sites.site_id.label("site_id"),
        Sites.nssid.label("nssid"),
        Sites.subzone_id.label("subzone_id"),
        Sites.category_id.label("category_no"),
        SiteType.site_type_name.label("site_type_name"),
        YearlyFrequency.frequency_count.label("frequency_no"),
        SiteGroup.site_group_name.label("site_group_name"),
        Users.user_name.label("user_name"),
        func.count(Equipment.equipment_id).label("equipment_count"),
        func.json_agg(
            func.json_build_object(
                'equipment_name', Equipment.equipment_name,
                'domain_name', Domain.domain_name,
                'vendor_name', Vendors.vendor_name
            )
        ).label("equipment_info")
    ).join(
        Subzones, Subzones.subzone_id == Sites.subzone_id
    ).join(
        Zones, Zones.zone_id == Subzones.zone_id
    ).join(
        Circle, Circle.circle_id == Zones.circle_id
    ).join(
        SiteType, SiteType.category_id == Sites.category_id
    ).join(
        YearlyFrequency, YearlyFrequency.frequency_id == SiteType.frequency_id
    ).join(
        SiteGroup, SiteGroup.site_group_id == SiteType.site_group_id
    ).join(
        AssignedSubzone, AssignedSubzone.subzone_id == Sites.subzone_id
    ).join(
        Users, Users.user_id == AssignedSubzone.user_id
    ).outerjoin(
        Equipment, Equipment.site_id == Sites.site_id
    ).outerjoin(
        Vendors, Vendors.id == Equipment.vendor_id
    ).outerjoin(
        Domain, Domain.category_id == Sites.category_id
    ).filter(
        Sites.category_id == category_no
    ).group_by(
        Circle.circle_name,
        Zones.zone_name,
        Subzones.subzone_name,
        Sites.site_id,
        Sites.nssid,
        Sites.subzone_id,
        Sites.category_id,
        SiteType.site_type_name,
        SiteGroup.site_group_name,  
        Users.user_name,
        YearlyFrequency.frequency_count
    )

    
    if circle_id:
        query = query.filter(Circle.circle_id == circle_id)
    if zone_id:
        query = query.filter(Zones.zone_id == zone_id)
    if subzone_id:
        query = query.filter(Subzones.subzone_id == subzone_id)
    if user_id:
        query = query.filter(Users.user_id == user_id)

    # total_records_query = query.with_entities(func.count(Sites.site_id))
    # total_records = total_records_query.scalar()
    total_records = query.count()

    # Apply limit and offset for pagination
    final_result = query.offset(offset).limit(limit).all()

    return {
        "totalRecords": total_records,
        "limit": limit,
        "offset": offset,
        "data": final_result
    }    


    
# 1) Zone should have poper values as per ZTM name selection
# 2) Sub Zone should have poper values as per ZTM name selection
# 3) Export button to be enabled 
# 4) Frequecy to be set from API


# SELECT circle.circle_name,zones.zone_name,subzones.subzone_name,  
# sites.site_id,sites.nssid,sites.subzone_id,sites.category_id,site_type.site_type_name,  
# site_group.site_group_name,users.user_name,COUNT(equipments.equipment_id) AS equipment_count, 
# JSON_AGG(JSON_BUILD_OBJECT
# ('equipment_name', equipments.equipment_name,
# 'domain_name', domain.domain_name,     
# 'vendor_name', vendors.vendor_name)) AS equipment_info 
# FROM sites 
# JOIN subzones ON subzones.subzone_id = sites.subzone_id 
# JOIN zones ON zones.zone_id = subzones.zone_id
# JOIN circle ON circle.circle_id = zones.circle_id 
# JOIN site_type ON site_type.category_id = sites.category_id
# JOIN site_group ON site_group.site_group_id = site_type.site_group_id 
# JOIN assigned_subzones ON assigned_subzones.subzone_id = sites.subzone_id 
# JOIN users ON users.user_id = assigned_subzones.user_id
# LEFT JOIN equipments ON equipments.site_id = sites.site_id 
# LEFT JOIN vendors ON vendors.id = equipments.vendor_id
# LEFT JOIN domain ON domain.category_id = sites.category_id
# where sites.category_id=1
# GROUP BY circle.circle_name, zones.zone_name, subzones.subzone_name, sites.site_id, sites.nssid,
# sites.subzone_id, sites.category_id, site_type.site_type_name, site_group.site_group_name, users.user_name;




 # query = db.query(
    #     Circle.circle_name.label("circle_name"),
    #     Zones.zone_name.label("zone_name"),
    #     Subzones.subzone_name.label("subzone_name"),
    #     Sites.nssid.label("nssid"),
    #     Sites.category_id.label("category_no"),
    #     SiteType.site_type_name.label("site_type_name"),
    #     SiteGroup.site_group_name.label("site_group_name"),
    #     Users.user_name.label("user_name"),
    #     func.count(Equipment.equipment_id).label("equipment_count"),
    #     func.string_agg(Equipment.equipment_name, '/').label("equipment_name")

    # ).join(
    #     Subzones, Subzones.subzone_id == Sites.subzone_id
    # ).join(
    #     Zones, Zones.zone_id == Subzones.zone_id
    # ).join(
    #     Circle, Circle.circle_id == Zones.circle_id
    # ).join(
    #     SiteType, SiteType.category_id == Sites.category_id
    # ).join(
    #     SiteGroup, SiteGroup.site_group_id == SiteType.site_group_id
    # ).join(
    #     AssignedSubzone, AssignedSubzone.subzone_id == Sites.subzone_id
    # ).join(
    #     Users, Users.user_id == AssignedSubzone.user_id
    # ).outerjoin(  
    #     Equipment, Equipment.site_id == Sites.site_id
    # ).filter(
    #     Sites.category_id == category_no
    # ).group_by(
    #     Circle.circle_name,
    #     Zones.zone_name,
    #     Subzones.subzone_name,
    #     Sites.site_id,
    #     Sites.nssid,
    #     Sites.subzone_id,
    #     Sites.category_id,
    #     SiteType.site_type_name,
    #     SiteGroup.site_group_name,
    #     Users.user_name
    # )

# ################    new working query ###########
# SELECT circle.circle_name,zones.zone_name,subzones.subzone_name,users.user_name,equipments_backup.site_id,yearly_frequency.frequency_count,
# sites_backup.nssid,site_type.site_type_name,  site_group.site_group_name,
# COUNT(equipments_backup.equipment_id) AS equipment_count,
# JSON_AGG(JSON_BUILD_OBJECT(
# 	'equipment_name', equipments_backup.equipment_name,
# 	'domain_name', domain.domain_name,
# 	'vendor_name', vendors.vendor_name
# 	)) AS equipment_info
# FROM equipments_backup
# JOIN sites_backup ON sites_backup.site_id = equipments_backup.site_id
# JOIN domain ON domain.domain_id = equipments_backup.domain_id
# JOIN site_type ON site_type.category_id = domain.category_id
# JOIN site_group ON site_group.site_group_id = site_type.site_group_id
# JOIN yearly_frequency on yearly_frequency.frequency_id=site_type.frequency_id
# JOIN assigned_subzones ON assigned_subzones.subzone_id = sites_backup.subzone_id 
# JOIN users ON users.user_id = assigned_subzones.user_id
# JOIN subzones ON subzones.subzone_id = assigned_subzones.subzone_id 
# JOIN zones ON zones.zone_id = subzones.zone_id
# JOIN circle ON circle.circle_id = zones.circle_id 
# LEFT JOIN vendors ON vendors.id = equipments_backup.vendor_id
# WHERE domain.category_id = 2
#   AND equipments_backup.site_id IS NOT NULL
# GROUP BY circle.circle_name, zones.zone_name, subzones.subzone_name,equipments_backup.site_id,yearly_frequency.frequency_count,sites_backup.nssid,
# site_type.site_type_name, site_group.site_group_name,users.user_name



# SELECT circle.circle_name,zones.zone_name,subzones.subzone_name,  
# sites_backup.site_id,sites_backup.nssid,sites_backup.subzone_id,sites_backup.category_id,site_type.site_type_name,  
# site_group.site_group_name,users.user_name,COUNT(equipments_backup.equipment_id) AS equipment_count, 
# JSON_AGG(JSON_BUILD_OBJECT
# ('equipment_name', equipments_backup.equipment_name,
# 'domain_name', domain.domain_name,     
# 'vendor_name', vendors.vendor_name)) AS equipment_info 
# FROM sites_backup 
# JOIN subzones ON subzones.subzone_id = sites_backup.subzone_id 
# JOIN zones ON zones.zone_id = subzones.zone_id
# JOIN circle ON circle.circle_id = zones.circle_id 
# JOIN site_type ON site_type.category_id = sites_backup.category_id
# JOIN site_group ON site_group.site_group_id = site_type.site_group_id 
# JOIN assigned_subzones ON assigned_subzones.subzone_id = sites_backup.subzone_id 
# JOIN users ON users.user_id = assigned_subzones.user_id
# LEFT JOIN equipments_backup ON equipments_backup.site_id = sites_backup.site_id 
# LEFT JOIN vendors ON vendors.id = equipments_backup.vendor_id
# LEFT JOIN domain ON domain.category_id = sites_backup.category_id
# where sites_backup.category_id=2
# GROUP BY circle.circle_name, zones.zone_name, subzones.subzone_name, sites_backup.site_id, sites_backup.nssid,
# sites_backup.subzone_id, sites_backup.category_id, site_type.site_type_name, site_group.site_group_name,users.user_name


# SELECT circle.circle_name,zones.zone_name,subzones.subzone_name,  
# sites.site_id,sites.nssid,sites.subzone_id,sites.category_id,site_type.site_type_name,  
# site_group.site_group_name,users.user_name,COUNT(equipments.equipment_id) AS equipment_count, 
# JSON_AGG(JSON_BUILD_OBJECT
# ('equipment_name', equipments.equipment_name,
# 'domain_name', domain.domain_name,     
# 'vendor_name', vendors.vendor_name)) AS equipment_info 
# FROM sites 
# JOIN subzones ON subzones.subzone_id = sites.subzone_id 
# JOIN zones ON zones.zone_id = subzones.zone_id
# JOIN circle ON circle.circle_id = zones.circle_id 
# JOIN site_type ON site_type.category_id = sites.category_id
# JOIN site_group ON site_group.site_group_id = site_type.site_group_id 
# JOIN assigned_subzones ON assigned_subzones.subzone_id = sites.subzone_id 
# JOIN users ON users.user_id = assigned_subzones.user_id
# LEFT JOIN equipments ON equipments.site_id = sites.site_id 
# LEFT JOIN vendors ON vendors.id = equipments.vendor_id
# LEFT JOIN domain ON domain.category_id = sites.category_id
# where sites.category_id=2
# GROUP BY circle.circle_name, zones.zone_name, subzones.subzone_name, sites.site_id, sites.nssid,
# sites.subzone_id, sites.category_id, site_type.site_type_name, site_group.site_type_group,users.user_name



######### ztm query #################

# select distinct(users.user_id),users.user_name from users
# join user_roles on user_roles.user_id=users.user_id
# join roles on roles.role_id=user_roles.role_id
# join assigned_circles on assigned_circles.user_id=users.user_id
# join assigned_subzones on assigned_subzones.user_id=users.user_id
# join subzones on subzones.subzone_id=assigned_subzones.subzone_id
# where roles.role_name='Manager' and assigned_circles.circle_id=1 and assigned_subzones.subzone_id=1 and subzones.zone_id=1 


# select domain.category_id from domain_type 
# join domain on domain.domaintype_id=domain_type.domaintype_id
# where domain_type.domaintype_name='Mobility'
# group by domain.category_id


# select domain_type_mapping.category_id from domain_type 
# join domain_type_mapping on domain_type_mapping.domaintype_id=domain_type.domaintype_id
# where domain_type.domaintype_name='Transport'
# group by domain_type_mapping.category_id




# select subzones.subzone_name from subzones
# join assigned_subzones on assigned_subzones.subzone_id=subzones.subzone_id
# join users on users.user_id=assigned_subzones.user_id
# where users.user_id=1


################### user query ##############

# select users.user_name from users
# join assigned_subzones on assigned_subzones.user_id=users.user_id
# join subzones on subzones.subzone_id=assigned_subzones.subzone_id
# join zones on zones.zone_id=subzones.subzone_id
# join circle on circle.circle_id=zones.circle_id
# where circle.circle_id=1 or zones.zone_id=1 or subzones.subzone_id=1
	

# select distinct(users.user_id),users.user_name from users
# join user_roles on user_roles.user_id=users.user_id
# join roles on roles.role_id=user_roles.role_id
# join assigned_circles on assigned_circles.user_id=users.user_id
# join assigned_subzones on assigned_subzones.user_id=users.user_id
# join subzones on subzones.subzone_id=assigned_subzones.subzone_id
# where roles.role_name='Manager' and assigned_circles.circle_id=1 and assigned_subzones.subzone_id=1 and subzones.zone_id=1 



######## 30/12/24########
# select eq.site_id,s.nssid,st.frequency_id,dt.domaintype_name from equipments eq
# Join sites s ON s.site_id=eq.site_id
# JOIN domain_type_mapping dm ON dm.domain_id = eq.domain_id
# JOIN domain_type dt ON dt.domaintype_id=dm.domaintype_id
# JOIN site_type st ON st.category_id=dm.category_id
# where dm.category_id=2
# group by eq.site_id,s.nssid,st.frequency_id,dt.domaintype_name


# select users.user_id,users.full_name,site_users.manager_id from site_users
# JOIN users ON users.user_id=site_users.user_id
# where manager_id=1

# select users.user_id,users.full_name,site_users.manager_id from users
# JOIN site_users ON site_users.user_id=users.user_id
# where manager_id=1


# select site_users.manager_id,
# JSON_AGG(JSON_BUILD_OBJECT
#  ('user_name', users.full_name,
#  'user_id', users.user_id)) AS engineer_info 
# from site_users
# JOIN users ON users.user_id=site_users.user_id
# where site_users.manager_id=1
# group by site_users.manager_id


# SELECT 
#     c.circle_name AS circle_name,
#     z.zone_name AS zone_name,
#     sz.subzone_name AS subzone_name,
#     u.user_name AS user_name,
#     e.site_id AS site_id,
#     yf.frequency_count AS frequency_no,
#     s.nssid AS nssid,
#     st.site_type_name AS site_type_name,
#     sg.site_group_name AS site_group_name,site_users.manager_id,
#     JSON_AGG(JSON_BUILD_OBJECT
#     ('user_name', u.full_name,
#      'user_id', u.user_id)) AS engineer_info 
# FROM 
#     equipments e
# JOIN 
#     sites s ON s.site_id = e.site_id
# JOIN 
#     domains d ON d.domain_id = e.domain_id
# JOIN 
#     domain_type_mapping dm ON dm.domain_id = d.domain_id
# JOIN 
#     site_type st ON st.category_id = dm.category_id
# JOIN 
#     site_group sg ON sg.site_group_id = st.site_group_id
# JOIN 
#     yearly_frequency yf ON yf.frequency_id = st.frequency_id
# JOIN 
#     assigned_subzones asz ON asz.subzone_id = s.subzone_id
# JOIN 
#     users u ON u.user_id = asz.user_id

# JOIN site_users	ON site_users.user_id=u.user_id

# JOIN 
#     subzones sz ON sz.subzone_id = asz.subzone_id
# JOIN 
#     zones z ON z.zone_id = sz.zone_id
# JOIN 
#     circle c ON c.circle_id = z.circle_id
# LEFT JOIN 
#     vendors v ON v.id = e.vendor_id

# GROUP BY 
#     c.circle_name,
#     z.zone_name,
#     sz.subzone_name,
#     u.user_name,
#     e.site_id,
#     yf.frequency_count,
#     s.nssid,
#     st.site_type_name,
#     sg.site_group_name,
# 	site_users.manager_id
	

	






















# circle table--circleid ,circle name 
# zone table ---zoneid zone name ,circleid
# subzone table --subzoneid , subzone name , zone id 

# domain table--- domain_id , domain_name ,domaintype_id,category_id,created_at,updated_at
# domaintype table -- domaintypeid , domain type name ,created_at,updated_at
# frequency table-- frequency id , frequency name , frequency count ,created_at,updated_at  ##removing cat id 
# site type table-- site type_id , site_group_id , frequency id , site type name ,priority , is_joint , is_active,created_at,updated_at  ## removing site_id
# sites tables --site_id ,nssid ,latitude,longitude,created_at ,updated_at,subzone_id
# category table---category id category name , category no ,created_at,updated_at
# site group table -- site_groupid , site_group name ,created_at,updated_at
# circle table --- circle_id , circle_name , circel_id_extra,circle_code,created_at,updated_at
# zones table -- zone_id ,zone_name,circle_id,zone_id_extra,created_at,updated_at
# subzone table --subzone_id,subzone_name,zone_id,subzone_id_extra,created_at,updated_at
# equipment table -- equipment_id,euipment_name,site_id,domain_id,site_tye_id
# users table -- user_id,user_id_extra,user_name,full_name,email,is_active,is_hide,hpsm_user_id,wfms_user_id,vms_user_id,created_at,updated_at
# assigned_subzones table -- id , user_id , subzone_id , created_at , updated_at 
# assigned_circle table -- id , user_id , circle_id , created_at , updated_at 
# vendor table --- id ,vendor_name,domain_id

# domain is connected to domain_type and category
# category s conected to yearly_frequency
# yeary_frequency is connected to site_type 
# site_type is connected to site_group 
# user is connected to circle
# circle is connected to xone is connected to subzone 
# subzone is connected to sites and site is connected to equipment_type
                      

# domain table--- domain_id , domain_name ,domaintype_id,category_id,created_at,updated_at
# domaintype table -- domaintypeid , domain type name ,created_at,updated_at
# frequency table-- frequency id , frequency name , frequency count ,created_at,updated_at 
# site type table-- site type_id , site_group_id , frequency id , site type name ,priority , is_joint , is_active,created_at,updated_at
# sites tables --site_id ,nssid ,latitude,longitude,created_at ,updated_at,subzone_id
# category table---category id category name , category no ,created_at,updated_at
# site group table -- site_groupid , site_group name ,created_at,updated_at
# circle table --- circle_id , circle_name , circel_id_extra,circle_code,created_at,updated_at
# zones table -- zone_id ,zone_name,circle_id,zone_id_extra,created_at,updated_at
# subzone table --subzone_id,subzone_name,zone_id,subzone_id_extra,created_at,updated_at
# equipment table -- equipment_id,euipment_name,site_id,domain_id
# users table -- user_id,user_id_extra,user_name,full_name,email,is_active,is_hide,hpsm_user_id,wfms_user_id,vms_user_id,created_at,updated_at
# assigned_subzones table -- id , user_id , subzone_id , created_at , updated_at 
# assigned_circle table -- id , user_id , circle_id , created_at , updated_at 
# vendor table --- id ,vendor_name,domain_id








