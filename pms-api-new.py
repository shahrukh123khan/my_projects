#nssid --184385 complete
# select c.circle_name, str_aagg(z.zone_name)
# from circle c join zones z on c.circle_id=z.circle_id
# group by circle_name


# SELECT 
#     c.circle_name, 
#     STRING_AGG(z.zone_name, '/') AS zone_names
# FROM 
#     circle c 
# JOIN 
#     zones z ON c.circle_id = z.circle_id
# GROUP BY 
#     c.circle_name;

# INDL002867_GZBD_H_H_R101  --microwave
# uvicorn app.main:app --host 10.19.71.175 --port 8084 --reload
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

class EquipmentInfo(BaseModel):
    # equipment_name: str[]
    # vendor_name: str
    # domain_name: str
    equipment_name :Optional[str] = None 
    vendor_name: Optional[str] = None  # Make vendor_name optional
    domain_name: Optional[str] = None  # Make domain_name optional
    
   

# Pydantic model for response
class DomainDataResponse(BaseModel):
    domain_name: str
    domaintype_name : str
    # domaintype_id: int
    category_no: int
    site_type_name: str
    site_group_name: str
    frequency_count: int
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
class InventoryResponse(BaseModel):
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


from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func

@app.post("/api/pms-inventory", response_model=InventoryResponse)
def get_inventory(request: dict, db: Session = Depends(get_db)):
    domaintype_name = request.get("domaintype_name", None)
    circle_id = request.get("circle_id", None)
    zone_id = request.get("zone_id", None)
    subzone_id = request.get("subzone_id", None)
    user_id = request.get("user_id", None) 
    limit = request.get("limit",20)  
    offset = request.get("offset", 0) 
    
    query = db.query(
        Users.user_name.label("user_name"),
        Sites.nssid.label("nssid"), 
        Circle.circle_name.label("circle_name"),
        Zones.zone_name.label("zone_name"),
        Subzones.subzone_name.label("subzone_name"),
        #Domain.domain_name.label("domain_name"),
        func.string_agg(Domain.domain_name.distinct(), '/').label("domain_name"),  # Concatenate distinct domain names
        DomainType.domaintype_name.label("domaintype_name"),
        Category.category_no.label("category_no"),
        SiteType.site_type_name.label("site_type_name"),
        SiteGroup.site_group_name.label("site_group_name"),
        YearlyFrequency.frequency_count.label("frequency_count"),
        func.count(Equipment.equipment_id.distinct()).label("equipment_count"),
        Vendors.vendor_name.label("vendor_name"),
        Equipment.equipment_name.label("equipment_name")
    ).join(
        Subzones, Subzones.subzone_id == Sites.subzone_id
    ).join(
        Zones, Zones.zone_id == Subzones.zone_id
    ).join(
        Circle, Circle.circle_id == Zones.circle_id
    ).join(
        Equipment, Equipment.site_id == Sites.site_id
    ).join(
        Domain, Domain.domain_id == Equipment.domain_id
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
        Vendors, Vendors.id == Equipment.domain_id
    ).join(
        AssignedCircle, AssignedCircle.circle_id == Circle.circle_id
    ).join(
        Users, Users.user_id == AssignedCircle.user_id
    )
    
    # Filters
    if domaintype_name:
        query = query.filter(DomainType.domaintype_name.ilike(domaintype_name))
    if circle_id:
        query = query.filter(Circle.circle_id == circle_id)
    if zone_id:
        query = query.filter(Zones.zone_id == zone_id)
    if subzone_id:
        query = query.filter(Subzones.subzone_id == subzone_id)
    if user_id:
        query = query.filter(Users.user_id == user_id)

    if circle_id and zone_id:
        query = query.filter(Circle.circle_id == circle_id)
        query = query.filter(Zones.zone_id == zone_id)
    if circle_id and subzone_id:
        query = query.filter(Circle.circle_id == circle_id)
        query = query.filter(Subzones.subzone_id == subzone_id)
    if circle_id and user_id:
        query = query.filter(Circle.circle_id == circle_id)
        query = query.filter(Users.user_id == user_id)
    if zone_id and subzone_id:
        query = query.filter(Zones.zone_id == zone_id)
        query = query.filter(Subzones.subzone_id == subzone_id)
    if zone_id and user_id:
        query = query.filter(Zones.zone_id == zone_id)
        query = query.filter(Users.user_id == user_id)
    if subzone_id and user_id:
        query = query.filter(Subzones.subzone_id == subzone_id)
        query = query.filter(Users.user_id == user_id)    

    # Group by all non-aggregated fields
    query = query.group_by(
        #Domain.domain_name,
        Users.user_name,
        Sites.nssid,
        Circle.circle_name,
        Zones.zone_name,
        Subzones.subzone_name,
        DomainType.domaintype_name,
        Category.category_no,
        SiteType.site_type_name,
        SiteGroup.site_group_name,
        YearlyFrequency.frequency_count,
        Vendors.vendor_name,
        Equipment.equipment_name
    )
    total_records = query.count()
    paginated_query = query.offset(offset).limit(limit)
    results = paginated_query.all()
    
    final_results = []
    grouped_results = defaultdict(list)
    
    for row in results:
        nssid = row.nssid
        equipment_name = row.equipment_name
        vendor_name = row.vendor_name
        domain_name = row.domain_name
        domaintype_name = row.domaintype_name.lower()

        # Create equipment_info entry
        if domaintype_name == "enterprise":
            # Only include equipment_name if domaintype_name is "enterprise"
            equipment_info = {
                "equipment_name": equipment_name
            }
        else:
            equipment_info = {
                "equipment_name": equipment_name,
                "vendor_name": vendor_name,
                "domain_name": domain_name
            }

        # Append equipment_info to the grouped result for the nssid
        grouped_results[nssid].append({
            "row": row,  # Store the full row for reference
            "equipment_info": equipment_info,
            "domain_name": domain_name
        })

    # Process grouped results
    for nssid, items in grouped_results.items():
        # Extract the first row for general fields
        row = items[0]["row"]

        # Extract unique domain names
        unique_domains = set(item["domain_name"] for item in items if item["domain_name"])

        # Extract unique equipment_info entries
        unique_equipment_info = []
        seen_equipment_names = set()
        for item in items:
            equipment = item["equipment_info"]
            if equipment["equipment_name"] not in seen_equipment_names:
                unique_equipment_info.append(equipment)
                seen_equipment_names.add(equipment["equipment_name"])

        # Append the processed result
        final_results.append({
            "nssid": nssid,
            "user_name": row.user_name,  # Include user information
            "circle_name": row.circle_name,
            "zone_name": row.zone_name,
            "subzone_name": row.subzone_name,  # Correct subzone-specific logic
            "domain_name": "/".join(unique_domains),  # Concatenate unique domains
            #"domain_name": row.domain_name, # Concatenate unique domains
            "domaintype_name": row.domaintype_name,
            "category_no": row.category_no,
            "site_type_name": row.site_type_name,
            "site_group_name": row.site_group_name,
            "frequency_count": row.frequency_count,
            "equipment_count": len(unique_equipment_info),
            "equipment_info": unique_equipment_info
        })

    return {
        "totalRecords": total_records,
        "limit": limit,
        "offset": offset,
        "data": final_results
    }
  





















######   new query working for mobility and enterprise #####

# SELECT 
#     u.user_name AS user_name,
#     c.circle_name AS circle_name,
#     z.zone_name AS zone_name,
#     sz.subzone_name AS subzone_name,
#     s.nssid AS nssid,
#     dt.domaintype_name AS domaintype_name,
#     string_agg(DISTINCT d.domain_name, '/') AS domain_name,
#     cat.category_no AS category_no,
#     yf.frequency_count AS frequency_count,
#     st.site_type_name AS site_type_name,
#     e.equipment_name AS equipment_name,
#     v.vendor_name AS vendor_name
# FROM 
#     users u
# JOIN 
#     assigned_circles ac ON u.user_id = ac.user_id
# JOIN 
#     circle c ON ac.circle_id = c.circle_id
# JOIN 
#     zones z ON c.circle_id = z.circle_id
# JOIN 
#     subzones sz ON z.zone_id = sz.zone_id
# JOIN 
#     sites s ON sz.subzone_id = s.subzone_id
# JOIN 
#     equipments e ON s.site_id = e.site_id
# JOIN 
#     domain d ON e.domain_id = d.domain_id
# JOIN 
#     domain_type dt ON d.domaintype_id = dt.domaintype_id
# JOIN 
#     category cat ON d.category_id = cat.category_id
# JOIN 
#     yearly_frequency yf ON cat.category_id = yf.category_id
# JOIN 
#     site_type st ON yf.frequency_id = st.frequency_id
# JOIN 
#     vendors v ON v.id = e.domain_id  -- Corrected to use domain_id
# WHERE 
#     dt.domaintype_name ILIKE '%Mobility%'  -- Filter for 'Enterprise' domaintype
# GROUP BY 
#     u.user_name, c.circle_name, z.zone_name, sz.subzone_name, s.nssid, dt.domaintype_name, 
#     cat.category_no, yf.frequency_count, st.site_type_name, e.equipment_name, v.vendor_name;



# select circle.circle_name,zones.zone_name,subzones.subzone_name,users.user_name,domain.domain_name from circle 
# join zones on zones.circle_id=circle.circle_id 
# join subzones on subzones.zone_id=zones.zone_id 
# join assigned_circles on  assigned_circles.circle_id=circle.circle_id
# join users on users.user_id=assigned_circles.user_id
# join domain_type on domain_type.domaintype_id=3
# join domain on domain.domaintype_id=domain_type.domaintype_id




# select circle.circle_name,zones.zone_name,subzones.subzone_name,domain_type.domaintype_name,users.user_name,
# sites.site_id,sites.nssid,sites.subzone_id,sites.category_id,site_type.site_type_name,site_group.site_group_name from sites
# join subzones on subzones.subzone_id=sites.subzone_id
# join zones on zones.zone_id=subzones.zone_id
# join circle on circle.circle_id=zones.circle_id
# join assigned_subzones on assigned_subzones.subzone_id=sites.subzone_id
# join users on users.user_id=assigned_subzones.user_id
# join category on category.category_no=sites.category_id
# join site_type on site_type.category_id=category.category_no
# join site_group on site_group.site_group_id=site_type.site_group_id 
# join domain_type on domain_type.domaintype_id=1



# select circle.circle_name,zones.zone_name,subzones.subzone_name,domain_type.domaintype_name,users.user_name,
# sites.site_id,sites.nssid,sites.subzone_id,sites.category_id,site_type.site_type_name,site_group.site_group_name ,
# from sites
# join subzones on subzones.subzone_id=sites.subzone_id
# join zones on zones.zone_id=subzones.zone_id
# join circle on circle.circle_id=zones.circle_id
# join assigned_subzones on assigned_subzones.subzone_id=sites.subzone_id
# join users on users.user_id=assigned_subzones.user_id
# join category on category.category_no=sites.category_id
# join site_type on site_type.category_id=category.category_no
# join site_group on site_group.site_group_id=site_type.site_group_id 
# join domain_type on domain_type.domaintype_id=1


####################

# select users.user_name,sites.nssid
# from circle 
# join assigned_circles on  assigned_circles.circle_id=circle.circle_id
# join users on users.user_id=assigned_circles.user_id
# join domain_type on domain_type.domaintype_id=1
# join domain on domain.domaintype_id=domain_type.domaintype_id
# join category on category.category_no=domain.category_id
# join sites on sites.category_id=category.category_no
# join site_type on site_type.category_id=category.category_no
# join site_group on site_group.site_group_id=site_type.site_group_id 
# where users.user_id=1

# --join equipments on equipments.site_id=sites.site_id


########### working ########### 


# select domain.category_id from domain_type 
# join domain on domain.domaintype_id=domain_type.domaintype_id
# where domain_type.domaintype_name='Mobility'
# group by domain.category_id


########## new ###########

# select domain_type_mapping.category_id from domain_type 
# join domain_type_mapping on domain_type_mapping.domaintype_id=domain_type.domaintype_id
# where domain_type.domaintype_name='Transport'
# group by domain_type_mapping.category_id






############ new working ############


# SELECT nssid.nssid,site_type.site_type_name,yearly_frequency.frequency_count,
# domain_type.domaintype_name,circle.circle_name,zones.zone_name,subzones.subzone_name
# from nssid 
# JOIN site_type ON site_type.category_id = nssid.category_id
# JOIN domain_type_mapping on domain_type_mapping.category_id=site_type.category_id
# JOIN domain_type ON domain_type.domaintype_id=domain_type_mapping.domaintype_id
# JOIN site_group ON site_group.site_group_id = site_type.site_group_id
# JOIN yearly_frequency on yearly_frequency.frequency_id=site_type.frequency_id
# JOIN assigned_subzones ON assigned_subzones.subzone_id = nssid.subzone_id 
# JOIN users ON users.user_id = assigned_subzones.user_id
# JOIN subzones ON subzones.subzone_id = assigned_subzones.subzone_id 
# JOIN zones ON zones.zone_id = subzones.zone_id
# JOIN circle ON circle.circle_id = zones.circle_id 
# GROUP BY circle.circle_name, zones.zone_name, subzones.subzone_name,yearly_frequency.frequency_count,nssid.nssid,
# site_type.site_type_name,users.user_name,domain_type.domaintype_name



######### raw query of working query #########
# SELECT 
#     c.circle_name AS circle_name,
#     z.zone_name AS zone_name,
#     sz.subzone_name AS subzone_name,
#     u.user_name AS user_name,
#     e.site_id AS site_id,
#     yf.frequency_count AS frequency_no,
#     s.nssid AS nssid,
#     st.site_type_name AS site_type_name,
#     sg.site_group_name AS site_group_name,
#     COUNT(e.equipment_id) AS equipment_count,
#     JSON_AGG(
#         JSON_BUILD_OBJECT(
#             'equipment_name', e.equipment_name,
#             'domain_name', d.domain_name,
#             'vendor_name', v.vendor_name
#         )
#     ) AS equipment_info
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
# JOIN 
#     subzones sz ON sz.subzone_id = asz.subzone_id
# JOIN 
#     zones z ON z.zone_id = sz.zone_id
# JOIN 
#     circle c ON c.circle_id = z.circle_id
# LEFT JOIN 
#     vendors v ON v.id = e.vendor_id
# WHERE 
#     dm.category_id = 3
# GROUP BY 
#     c.circle_name,
#     z.zone_name,
#     sz.subzone_name,
#     u.user_name,
#     e.site_id,
#     yf.frequency_count,
#     s.nssid,
#     st.site_type_name,
#     sg.site_group_name;
































































# 24/12/24
# Meeting with VI team for the pms update and progress .
# Meeting with mayank,shubham,tarun and trapti for the alarm and kpi disscusion for 
# the scheduling api and database for alarms and kpi . understanding to match the proper data . (4-5 hrs)
# Worked on the sheduling api . 


# SELECT n.nssid,st.site_type_name,yf.frequency_count,dt.domaintype_name,c.circle_name,z.zone_name,sz.subzone_name,
# CASE
#         WHEN fk.nssid LIKE '%' || n.nssid || '%' 
#              AND c.circle_name = fk.standard_name_uim THEN 'Yes'
#         ELSE 'No'
#     END AS Kpis,
# CASE
#         WHEN ra.circle_code = c.circle_name
#              AND ra.nss_id = n.nssid
#              AND ra.days_between = 'YES' THEN 'Yes'
#         ELSE 'No'
#     END AS Alarms
# FROM 
#     nssid n
# JOIN 
#     site_type st ON st.category_id = n.category_id
# JOIN 
#     domain_type_mapping dtm ON dtm.category_id = st.category_id
# JOIN 
#     domain_type dt ON dt.domaintype_id = dtm.domaintype_id
# JOIN 
#     site_group sg ON sg.site_group_id = st.site_group_id
# JOIN 
#     yearly_frequency yf ON yf.frequency_id = st.frequency_id
# JOIN 
#     assigned_subzones asz ON asz.subzone_id = n.subzone_id 
# JOIN 
#     users u ON u.user_id = asz.user_id
# JOIN 
#     subzones sz ON sz.subzone_id = asz.subzone_id 
# JOIN 
#     zones z ON z.zone_id = sz.zone_id
# JOIN 
#     circle c ON c.circle_id = z.circle_id 
# LEFT JOIN 
#     final_kpi fk ON fk.nssid LIKE '%' || n.nssid || '%'
#                  AND c.circle_name = fk.standard_name_uim
# LEFT JOIN 
#     ran_alarms ra ON ra.circle_code = c.circle_name
#                  AND ra.nss_id = n.nssid

# GROUP BY c.circle_name, z.zone_name, sz.subzone_name, yf.frequency_count, n.nssid, st.site_type_name, dt.domaintype_name, 
# fk.nssid, fk.standard_name_uim,ra.circle_code,ra.nss_id, ra.days_between 

# UPDATE site_type_data
# SET kpi = 'Yes'
# FROM final_kpi
# WHERE final_kpi.nssid LIKE '%' || site_type_data.nssid || '%'
#   AND site_type_data.circle_code = final_kpi.standard_name_uim;


