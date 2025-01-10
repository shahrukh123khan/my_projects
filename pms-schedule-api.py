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
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends
from sqlalchemy.orm import aliased
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

# class DomainDataResponse(BaseModel):
#     nssid: str
#     site_type_name: str
#     engineer_domain: str
#     frequency_no: int
#     schedule_type: str = Field(default='System')
#     tentative_start_date: str = Field(default=None)  
#     tentative_end_date: str = Field(default=None)    
#     total_task_completed: int = Field(default=5)
#     last_activity_date: str = Field(default=None)    
#     schedule_status: str = Field(default='Pending')  
#     engineer_available: str = Field(default='Pending')
#     ticket_aging_in_days: int = Field(default=1)     
#     ticket_status: str = Field(default='Open')
#     subzone_name: str
#     zone_name: str
#     circle_name: str
#     kpi: str
#     alarm: Optional[str] = Field(default=None)  # Made alarm optional
#     monsoon: str = Field(default='False')            

#     class Config:
#         from_attributes = True

# class ResponseModel(BaseModel):
#     # totalRecords: int
#     limit: int
#     offset: int
#     data: List[DomainDataResponse]
from pydantic import BaseModel, Field
from typing import List, Optional

# Response Model for individual domain data
class DomainDataResponse(BaseModel):
    nssid: str
    site_type_name: str
    frequency_no: int
    schedule_type: str = Field(default='System')
    tentative_start_date: Optional[str] = None  
    tentative_end_date: Optional[str] = None    
    total_task_completed: int = Field(default=5)
    last_activity_date: Optional[str] = None    
    schedule_status: str = Field(default='Pending')  
    engineer_available: str = Field(default='Pending')
    ticket_aging_in_days: int = Field(default=1)     
    ticket_status: str = Field(default='Open')
    subzone_name: str
    zone_name: str
    circle_name: str
    kpi: bool  # Boolean for KPI matching
    alarm: Optional[str] = Field(default=None)  # Alarm status ('Yes' or 'No')
    monsoon: str = Field(default='False') 
    users: List[dict] = Field(default=[])  # List of users (id, name)

    class Config:
        from_attributes = True

# Response Model for the full response with pagination
class ResponseModel(BaseModel):
    limit: int
    offset: int
    data: List[DomainDataResponse]
    
    class Config:
        from_attributes = True

# Define ORM models
class Kpis(Base):
    __tablename__ = "kpis"
    id = Column(Integer, primary_key=True)
    nssid = Column(String)

class Alarms(Base):
    __tablename__ = "site_alarms"
    id = Column(Integer, primary_key=True)
    days_between = Column(String)
    circle_id = Column(Integer)
    nss_id = Column(String)



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


class Domain(Base):
    __tablename__ = "domains"
    domain_id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String, index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    domain_mappings = relationship("DomainMapping", back_populates="domain")

class DomainType(Base):
    __tablename__ = "domain_type"
    domaintype_id = Column(Integer, primary_key=True, index=True)
    domaintype_name = Column(String, index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    domain_mappings = relationship("DomainMapping", back_populates="domain_type")

class DomainMapping(Base):
    __tablename__ = "domain_type_mapping"
    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.domain_id"))
    domain_name = Column(String, index=True)
    domaintype_id = Column(Integer, ForeignKey("domain_type.domaintype_id"))
    category_id = Column(Integer, ForeignKey("category.category_id"))
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    domain_type = relationship("DomainType", back_populates="domain_mappings")
    category = relationship("Category", back_populates="domain_mappings")
    domain = relationship("Domain", back_populates="domain_mappings")

class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)
    category_no = Column(Integer)
    frequencies = relationship("YearlyFrequency", back_populates="category")
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    domain_mappings = relationship("DomainMapping", back_populates="category")

class YearlyFrequency(Base):
    __tablename__ = "yearly_frequency"
    frequency_id = Column(Integer, primary_key=True, index=True)
    frequency_name = Column(String)
    frequency_count = Column(Integer)
    category_id = Column(Integer, ForeignKey("category.category_id"))
    category = relationship("Category", back_populates="frequencies")
    site_types = relationship("SiteTypeMapping", back_populates="frequency")
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

class SiteTypeMapping(Base):
    __tablename__ = "site_type_mapping"
    site_type_id = Column(Integer, primary_key=True, index=True)
    site_type_name = Column(String)
    frequency_id = Column(Integer, ForeignKey("yearly_frequency.frequency_id"))
    site_group_id = Column(Integer, ForeignKey("site_group.site_group_id"))
    frequency = relationship("YearlyFrequency", back_populates="site_types")
    site_group = relationship("SiteGroup", back_populates="site_types")
    category_id = Column(Integer)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

class SiteType(Base):
    __tablename__ = "site_type"
    
    # Define the columns
    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    site_type_name = Column(String, nullable=False)  # Name of the site type
    created_at = Column(DateTime, default=func.now())  # Timestamp when record is created
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Timestamp when record is updated

class SiteMapping(Base):
    __tablename__ = "site_mapping"
    
    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    # site_type_id = Column(Integer, ForeignKey("site_type.id"), nullable=False)  # Foreign key to site_type
    site_type_id  = Column(String)
    site_id = Column(Integer, ForeignKey("sites.site_id"), nullable=False)  # Foreign key to sites
    subzone_id = Column(Integer, ForeignKey("subzones.subzone_id"), nullable=False)  # Foreign key to subzones
    created_at = Column(DateTime, default=func.now())  # Timestamp when record is created
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Timestamp when record is updated
    
    site = relationship("Sites", back_populates="site_mappings")
    subzone = relationship("Subzones", back_populates="site_mappings")

class SiteGroup(Base):
    __tablename__ = "site_group"
    site_group_id = Column(Integer, primary_key=True, index=True)
    site_group_name = Column(String)
    site_types = relationship("SiteTypeMapping", back_populates="site_group")
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

    site_mappings = relationship("SiteMapping", back_populates="site")
    
class Subzones(Base):
    __tablename__ = "subzones"
    subzone_id = Column(Integer, primary_key=True, index=True)
    subzone_name = Column(String)
    zone_id = Column(Integer, ForeignKey("zones.zone_id"))
    sites = relationship("Sites", back_populates="subzone")
    zone = relationship("Zones", back_populates="subzones")
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    site_mappings = relationship("SiteMapping", back_populates="subzone")
    
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
   
    roles = relationship("UserRoles", back_populates="user")

class SiteUsers(Base):
    __tablename__ = "site_users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))  # Assuming there is a 'users' table with 'user_id' column
    manager_id = Column(Integer)  # Assuming managers are also in the 'users' table
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Define relationships
    user = relationship("Users", foreign_keys=[user_id]) 


class Roles(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    roler_id_extra = Column(Integer)  # Assuming it's a string; adjust as needed
    role_name = Column(String, nullable=False, unique=True)  # Unique for login purposes
    created_at = Column(DateTime, default=func.now())  # Timestamp for creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Timestamp for updates

    user_roles = relationship("UserRoles", back_populates="role")
  
class UserRoles(Base):
    __tablename__ = "user_roles"

    user_role_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    created_at = Column(DateTime, default=func.now())  # Timestamp for creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Timestamp for updates
    
    user = relationship("Users", back_populates="roles")
    role = relationship("Roles", back_populates="user_roles")

   
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


@app.post("/api/pms-schedule", response_model=ResponseModel)
def get_inventory(request: dict, db: Session = Depends(get_db)):
    # Defining limit and offset
    limit = request.get("limit", 10)
    offset = request.get("offset", 0)
    print("limit ",limit)
    # Alias for 'Kpis' table
    kpi_alias = aliased(Kpis)

    query = db.query(
        Sites.nssid.label("nssid"),
        DomainType.domaintype_name.label("domaintype_name"),
        SiteGroup.site_group_name.label("site_group_name"),
        SiteType.site_type_name.label("site_type_name"),
        SiteTypeMapping.frequency_id.label("frequency_no"),
        Subzones.subzone_name.label("subzone_name"),
        Zones.zone_name.label("zone_name"),
        Circle.circle_name.label("circle_name"),
        case(
            (Alarms.days_between == 'Yes', 'Yes'),
            else_='No'
        ).label("Alarm"),
        # Aggregate users in JSON format
        func.coalesce(
            func.json_agg(
                func.json_build_object('id', Users.user_id, 'name', Users.user_name)
            ).filter(Users.user_id.isnot(None)),
            '[]'  
        ).label("users"),
        # KPI case
        case(
            (kpi_alias.nssid.like(func.concat('%', Sites.nssid, '%')), True),
            else_=False
        ).label("kpi")
    ).select_from(Sites) \
        .join(SiteMapping, SiteMapping.site_id == Sites.site_id) \
        .join(SiteTypeMapping, SiteTypeMapping.site_type_id == SiteMapping.site_type_id) \
        .join(DomainMapping, DomainMapping.category_id == SiteTypeMapping.category_id) \
        .join(DomainType, DomainType.domaintype_id == DomainMapping.domaintype_id) \
        .join(SiteGroup, SiteGroup.site_group_id == SiteTypeMapping.site_group_id) \
        .join(SiteType, SiteType.id == SiteTypeMapping.site_type_id) \
        .outerjoin(AssignedSubzone, AssignedSubzone.subzone_id == SiteMapping.subzone_id) \
        .outerjoin(SiteUsers, SiteUsers.manager_id == AssignedSubzone.user_id) \
        .outerjoin(Users, Users.user_id == SiteUsers.user_id) \
        .join(Subzones, Subzones.subzone_id == SiteMapping.subzone_id) \
        .join(Zones, Zones.zone_id == Subzones.zone_id) \
        .join(Circle, Circle.circle_id == Zones.circle_id) \
        .join(Alarms, and_(
            Alarms.circle_id == Circle.circle_id,
            Alarms.nss_id == Sites.nssid
        )) \
        .join(kpi_alias, kpi_alias.nssid.like(func.concat('%', Sites.nssid, '%'))) \
        .filter(DomainType.domaintype_name == 'Transport') \
        .group_by(
            Sites.nssid,
            DomainType.domaintype_name,
            SiteGroup.site_group_name,
            SiteType.site_type_name,
            SiteTypeMapping.frequency_id,
            Subzones.subzone_name,
            Zones.zone_name,
            Circle.circle_name,
            Alarms.days_between,
            Alarms.circle_id,
            Alarms.nss_id,
            kpi_alias.nssid
        ) \
        .limit(limit) \
        .offset(offset)

    #print("query",query)
    final_result = query.all()
    print("result ",final_result)
   

    return {
        "limit": limit,
        "offset": offset,
        "data": final_result
    }


############ alarm kpi working with 100 limit ###########


# SELECT 
#     n.nssid,
#     st.site_type_name,
#     yf.frequency_count,
#     dt.domaintype_name,
#     c.circle_name,
#     z.zone_name,
#     sz.subzone_name,
#     a.days_between as Alarm,
# 	-- Selecting the days_between column from ran_alarms
# CASE 
#         WHEN k.nssid IS NOT NULL THEN 'YES'
#         ELSE 'NO'
#     END AS Kpi

# FROM 
#     sites n
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
#     ran_alarms a ON a.circle_code = c.circle_name AND a.nss_id = n.nssid AND a.days_between = 'YES'
# LEFT JOIN 
#     kpis k ON k.nssid LIKE CONCAT('%', n.nssid, '%')  ---added
	
# GROUP BY 
#     n.nssid, 
#     st.site_type_name, 
#     yf.frequency_count, 
#     dt.domaintype_name, 
#     c.circle_name, 
#     z.zone_name, 
#     sz.subzone_name, 
#     a.days_between, 
#     a.circle_code, 
#     a.nss_id,
# 	k.nssid

# limit 100	







# SELECT 
#     n.nssid,
#     k.nssid AS kpi_nssid,
#     CASE 
#         WHEN k.nssid IS NOT NULL THEN 'YES'
#         ELSE 'NO'
#     END AS kpi_found
# FROM 
#     sites n
# LEFT JOIN 
#     kpis k ON k.nssid LIKE CONCAT('%', n.nssid, '%') 






# SELECT n.nssid,st.site_type_name,yf.frequency_count,dt.domaintype_name,c.circle_name,z.zone_name,sz.subzone_name,

# CASE
#         WHEN ra.circle_code = c.circle_name
#              AND ra.nss_id = n.nssid
#              AND ra.days_between = 'YES' THEN 'Yes'
#         ELSE 'No'
#     END AS Alarms
# FROM 
#     sites n
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
#     ran_alarms ra ON ra.circle_code = c.circle_name
#                  AND ra.nss_id = n.nssid

# GROUP BY c.circle_name, z.zone_name, sz.subzone_name, yf.frequency_count, n.nssid, st.site_type_name, dt.domaintype_name, 
# ra.circle_code,ra.nss_id, ra.days_between 



# select site_users.user_id,users.user_name from site_users
# JOIN users ON users.user_id=site_users.user_id
# where manager_id=1
	





# select s.nssid,stm.site_type_id,st.site_type_name,sg.site_group_name from sites s
# JOIN site_mapping sm ON sm.site_id=s.site_id
# JOIN site_type_mapping stm ON stm.site_type_id=sm.site_type_id
# JOIN site_type st ON st.id=stm.site_type_id
# JOIN site_group sg ON sg.site_group_id=stm.site_group_id
# group by s.nssid,stm.site_type_id,st.site_type_name,sg.site_group_name

########## 02/01/24 ############

# select s.nssid,dt.domaintype_name,sg.site_group_name,st.site_type_name,f.frequency_count,sz.subzone_name,
# z.zone_name,c.circle_name,u.user_name,u.user_id
# from sites s
# JOIN site_mapping sm ON sm.site_id=s.site_id
# JOIN site_type_mapping stm ON stm.site_type_id=sm.site_type_id
# JOIN site_type st ON st.id=stm.site_type_id
# JOIN site_group sg ON sg.site_group_id=stm.site_group_id
# JOIN yearly_frequency f ON f.frequency_id=stm.frequency_id
# Join domain_type_mapping dtm ON dtm.category_id=stm.category_id
# JOIN domain_type dt ON dt.domaintype_id=dtm.domaintype_id
# JOIN subzones sz ON sz.subzone_id=sm.subzone_id
# JOIN zones z ON z.zone_id=sz.zone_id
# JOIN circle c ON c.circle_id=z.circle_id
# JOIN assigned_subzones asz ON asz.subzone_id=sz.subzone_id
# JOIN users u ON u.user_id=asz.user_id
# JOIN site_users su ON su.user_id=u.user_id
# group by s.nssid,stm.site_type_id,st.site_type_name,sg.site_group_name,
# f.frequency_count,dt.domaintype_name,sz.subzone_name,z.zone_name,c.circle_name,u.user_name,u.user_id

# select s.nssid,dt.domaintype_name,sg.site_group_name,st.site_type_name,f.frequency_count,sz.subzone_name,
# z.zone_name,c.circle_name,u.user_name,u.user_id
# from sites s
# JOIN site_mapping sm ON sm.site_id=s.site_id
# JOIN site_type_mapping stm ON stm.site_type_id=sm.site_type_id
# JOIN site_type st ON st.id=stm.site_type_id
# JOIN site_group sg ON sg.site_group_id=stm.site_group_id
# JOIN yearly_frequency f ON f.frequency_id=stm.frequency_id
# Join domain_type_mapping dtm ON dtm.category_id=stm.category_id
# JOIN domain_type dt ON dt.domaintype_id=dtm.domaintype_id
# JOIN subzones sz ON sz.subzone_id=sm.subzone_id
# JOIN zones z ON z.zone_id=sz.zone_id
# JOIN circle c ON c.circle_id=z.circle_id
# JOIN assigned_subzones asz ON asz.subzone_id=sm.subzone_id
# JOIN site_users su ON su.manager_id=asz.user_id
# JOIN users u ON u.user_id=su.user_id
# group by s.nssid,stm.site_type_id,st.site_type_name,sg.site_group_name,
# f.frequency_count,dt.domaintype_name,sz.subzone_name,z.zone_name,c.circle_name,u.user_name,u.user_id




# SELECT 
#     s.nssid,
#     dt.domaintype_name,
#     sg.site_group_name,
#     st.site_type_name,
#     stm.frequency_id,
#     -- Aggregate users in JSON format
#     COALESCE(
#         json_agg(
#             json_build_object('id', u.user_id, 'name', u.user_name)
#         ) FILTER (WHERE u.user_id IS NOT NULL), 
#         '[]' -- Default to empty array if no users found
#     ) AS users
# FROM 
#     sites s
# JOIN 
#     site_mapping sm ON sm.site_id = s.site_id
# JOIN 
#     site_type_mapping stm ON stm.site_type_id = sm.site_type_id
# JOIN 
#     domain_type_mapping dtm ON dtm.category_id = stm.category_id
# JOIN 
#     domain_type dt ON dt.domaintype_id = dtm.domaintype_id
# JOIN 
#     site_group sg ON sg.site_group_id = stm.site_group_id
# JOIN 
#     site_type st ON st.id = stm.site_type_id
# LEFT JOIN 
#     assigned_subzones asub ON asub.subzone_id = sm.subzone_id
# LEFT JOIN 
#     site_users su ON su.manager_id = asub.user_id
# LEFT JOIN 
#     users u ON u.user_id = su.user_id
# WHERE 
#     dt.domaintype_name = 'Mobility'
# GROUP BY 
#     s.nssid, dt.domaintype_name, sg.site_group_name, st.site_type_name, stm.frequency_id
# limit 100;

# ##### timwe 3:37#####




# SELECT 
#     s.nssid,
#     dt.domaintype_name,
#     sg.site_group_name,
#     st.site_type_name,
#     stm.frequency_id,
# 	sz.subzone_name,
# 	z.zone_name,
# 	c.circle_name,
# 	a.days_between as Alarm,
#     -- Aggregate users in JSON format
#     COALESCE(
#         json_agg(
#             json_build_object('id', u.user_id, 'name', u.user_name)
#         ) FILTER (WHERE u.user_id IS NOT NULL), 
#         '[]' -- Default to empty array if no users found
#     ) AS users
# FROM 
#     sites s
# JOIN 
#     site_mapping sm ON sm.site_id = s.site_id
# JOIN 
#     site_type_mapping stm ON stm.site_type_id = sm.site_type_id
# JOIN 
#     domain_type_mapping dtm ON dtm.category_id = stm.category_id
# JOIN 
#     domain_type dt ON dt.domaintype_id = dtm.domaintype_id
# JOIN 
#     site_group sg ON sg.site_group_id = stm.site_group_id
# JOIN 
#     site_type st ON st.id = stm.site_type_id
# LEFT JOIN 
#     assigned_subzones asub ON asub.subzone_id = sm.subzone_id
# LEFT JOIN 
#     site_users su ON su.manager_id = asub.user_id
# LEFT JOIN 
#     users u ON u.user_id = su.user_id
# JOIN subzones sz ON sz.subzone_id=sm.subzone_id
# JOIN zones z ON z.zone_id=sz.zone_id
# JOIN circle c ON c.circle_id=z.circle_id
# JOIN 
#     ran_alarms a ON a.circle_code = c.circle_name AND a.nss_id = s.nssid
# WHERE 
#     dt.domaintype_name = 'Transport'
# GROUP BY 
#     s.nssid, dt.domaintype_name, sg.site_group_name, st.site_type_name, stm.frequency_id,
# sz.subzone_name,z.zone_name,c.circle_name,a.days_between,a.circle_code,a.nss_id




# SELECT 
#     s.nssid,
#     dt.domaintype_name,
#     sg.site_group_name,
#     st.site_type_name,
#     stm.frequency_id,
# 	sz.subzone_name,
# 	z.zone_name,
# 	c.circle_name,
# 	a.days_between as Alarm,
#     -- Aggregate users in JSON format
#     COALESCE(
#         json_agg(
#             json_build_object('id', u.user_id, 'name', u.user_name)
#         ) FILTER (WHERE u.user_id IS NOT NULL), 
#         '[]' -- Default to empty array if no users found
#     ) AS users
# FROM 
#     sites s
# JOIN 
#     site_mapping sm ON sm.site_id = s.site_id
# JOIN 
#     site_type_mapping stm ON stm.site_type_id = sm.site_type_id
# JOIN 
#     domain_type_mapping dtm ON dtm.category_id = stm.category_id
# JOIN 
#     domain_type dt ON dt.domaintype_id = dtm.domaintype_id
# JOIN 
#     site_group sg ON sg.site_group_id = stm.site_group_id
# JOIN 
#     site_type st ON st.id = stm.site_type_id
# LEFT JOIN 
#     assigned_subzones asub ON asub.subzone_id = sm.subzone_id
# LEFT JOIN 
#     site_users su ON su.manager_id = asub.user_id
# LEFT JOIN 
#     users u ON u.user_id = su.user_id
# JOIN subzones sz ON sz.subzone_id=sm.subzone_id
# JOIN zones z ON z.zone_id=sz.zone_id
# JOIN circle c ON c.circle_id=z.circle_id
# --JOIN ran_alarms a ON a.circle_code = c.circle_name AND a.nss_id = s.nssid
# JOIN alarm_dump a ON a.circle_code = c.circle_id AND a.nss_id = s.nssid

# WHERE 
#     dt.domaintype_name = 'Transport'
# GROUP BY 
#     s.nssid, dt.domaintype_name, sg.site_group_name, st.site_type_name, stm.frequency_id,
# sz.subzone_name,z.zone_name,c.circle_name,a.days_between,a.circle_code,a.nss_id
# limit 10










# select * from kpis where nssid='IDUW100934_GHAZ_I_H_R5A1-IDUW107153_GHAZ_I_H_R5A1'




# SELECT sites.nssid AS nssid, domain_type.domaintype_name AS domaintype_name, site_group.site_group_name AS site_group_name, 
# site_type.site_type_name AS site_type_name, site_type_mapping.frequency_id AS frequency_no, subzones.subzone_name AS 
# subzone_name, zones.zone_name AS zone_name, circle.circle_name AS circle_name,
# CASE WHEN (alarm_dump.days_between = %(days_between_1)s) THEN %(param_1)s ELSE %(param_2)s
# END AS "Alarm", coalesce(json_agg(json_build_object(%(json_build_object_1)s, users.user_id, %(json_build_object_2)s, users.user_name))
# FILTER (WHERE users.user_id IS NOT NULL), %(coalesce_1)s) AS users, CASE WHEN (kpis_1.nssid LIKE concat(%(concat_1)s, sites.nssid, %(concat_2)s))
# THEN %(param_3)s ELSE %(param_4)s END AS kpi
# FROM sites JOIN site_mapping ON site_mapping.site_id = sites.site_id 
# JOIN site_type_mapping ON site_type_mapping.site_type_id = site_mapping.site_type_id 
# JOIN domain_type_mapping ON domain_type_mapping.category_id = site_type_mapping.category_id 
# JOIN domain_type ON domain_type.domaintype_id = domain_type_mapping.domaintype_id JOIN
# site_group ON site_group.site_group_id = site_type_mapping.site_group_id 
# JOIN site_type ON site_type.id = site_type_mapping.site_type_id 
# LEFT OUTER JOIN assigned_subzones ON assigned_subzones.subzone_id = site_mapping.subzone_id 
# JOIN subzones ON subzones.subzone_id = site_mapping.subzone_id 
# JOIN zones ON zones.zone_id = subzones.zone_id 
# JOIN circle ON circle.circle_id = zones.circle_id 
# JOIN alarm_dump ON alarm_dump.circle_code = circle.circle_id AND alarm_dump.nss_id = sites.nssid 
# JOIN kpis AS kpis_1 ON kpis_1.nssid LIKE concat(%(concat_3)s, sites.nssid, %(concat_4)s), users
# WHERE domain_type.domaintype_name = %(domaintype_name_1)s GROUP BY sites.nssid, domain_type.domaintype_name,
# site_group.site_group_name, site_type.site_type_name, site_type_mapping.frequency_id, 
# subzones.subzone_name, zones.zone_name, circle.circle_name, alarm_dump.days_between, alarm_dump.circle_code, 
# alarm_dump.nss_id, kpis_1.nssid
#  LIMIT 10


# task table--task_id,created_by,task_planner_id,status,created_at,updated_at
# task status table--id,status,created_at,updated_at
# ticket table --ticket_id,task_id,assigned_by,nssid,start_date,end_date,comment,created_at,updated_at,status
# ticket status --id,status,created_at,updated_at
# sites table -- site_is,nssid,created_at,updated_at

#  "schedule_data":[{
#   "nssid":"",
#   "tentative_start_date":"",
#   "tentative_end_date":"",
#   "users":[
#     1
#   ]
# },
# {
#   "nssid":"",
#   "tentative_start_date":"",
#   "tentative_end_date":"",
#   "users":[
#     5
#   ]
# }
# ]i will get this in request and from this data we need to create the task and tickects through the api the tables are as in the db . 

# task table--task_id,created_by,task_planner_id,status,created_at,updated_at
# task status table--id,status,created_at,updated_at
# ticket table --ticket_id,task_id,assigned_by,nssid,start_date,end_date,comment,created_at,updated_at,status
# ticket status --id,status,created_at,updated_at
# sites table -- site_is,nssid,created_at,updated_at   so what will be the api code for fast api 
# task table--task_id,created_by,task_planner_id,status,created_at,updated_at
# task status table--id,status,created_at,updated_at
# ticket table --ticket_id,task_id,assigned_by,nssid,start_date,end_date,comment,created_at,updated_at,status
# ticket status --id,status,created_at,updated_at
# sites table -- site_is,nssid,created_at,updated_at




# select  s.nssid,sz.subzone_name,su.user_id
# from sites s
# JOIN site_mapping sm ON sm.site_id = s.site_id
# JOIN subzones sz ON sz.subzone_id=sm.subzone_id
# JOIN assigned_subzones asub ON asub.subzone_id = sz.subzone_id
# LEFT JOIN site_users su ON su.manager_id = asub.user_id


# select * from site_mapping limit 10


# COALESCE(
#         JSON_AGG(
#             JSON_BUILD_OBJECT('id', u.user_id, 'name', u.user_name)
#         ) FILTER (WHERE u.user_id IS NOT NULL), 
#         '[]' 
#     ) AS users




########## new working one #########

# SELECT 
#     s.nssid,
#     dt.domaintype_name,
#     sg.site_group_name,
#     st.site_type_name,
#     stm.frequency_id,
#     c.circle_code, 
#     z.zone_name, 
#     sz.subzone_name,
  
# 	BOOL_OR(sa.days_between = 'YES') AS Alarm,
    
#     -- Use BOOL_OR to handle the repetition issue in kpis table
#     BOOL_OR(k.nssid LIKE '%' || s.nssid || '%') AS kpi

# FROM 
#     sites s

# JOIN 
#     site_mapping sm ON sm.site_id = s.site_id
# JOIN 
#     site_type_mapping stm ON stm.site_type_id = sm.site_type_id
# JOIN 
#     domain_type_mapping dtm ON dtm.category_id = stm.category_id
# JOIN 
#     domain_type dt ON dt.domaintype_id = dtm.domaintype_id
# JOIN 
#     site_group sg ON sg.site_group_id = stm.site_group_id
# JOIN 
#     site_type st ON st.id = stm.site_type_id

# JOIN 
#     subzones sz ON sz.subzone_id = sm.subzone_id
# JOIN 
#     zones z ON z.zone_id = sz.zone_id 
# JOIN 
#     circle c ON c.circle_id = z.circle_id
# JOIN 
#     site_alarms sa ON sa.nss_id = s.nssid
# JOIN 
#     kpis k ON k.nssid LIKE '%' || s.nssid || '%'


# WHERE 
#     dt.domaintype_name = 'Mobility'

# GROUP BY 
#     s.nssid, dt.domaintype_name, sg.site_group_name, st.site_type_name, stm.frequency_id, sa.days_between,
#     c.circle_code, z.zone_name, sz.subzone_name

# LIMIT 10;




######## inventory ########

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
#     COUNT(e.equipment_id) AS equipment_count
    
# FROM 
#     sites s

# JOIN 
#     site_mapping sm ON sm.site_id = s.site_id

# JOIN 
#     site_type st ON st.id = sm.site_type_id
# JOIN 
#     site_type_mapping stm ON stm.site_type_id = st.id
# JOIN 
#     domain_type_mapping dm ON dm.category_id = stm.category_id
# JOIN 
#     domains d ON d.domain_id = dm.domain_id

# JOIN 
#     site_group sg ON sg.site_group_id = stm.site_group_id
# JOIN 
#     yearly_frequency yf ON yf.frequency_id = stm.frequency_id
# JOIN 
#     assigned_subzones asz ON asz.subzone_id = sm.subzone_id
# JOIN 
#     users u ON u.user_id = asz.user_id
# JOIN 
#     subzones sz ON sz.subzone_id = asz.subzone_id
# JOIN 
#     zones z ON z.zone_id = sz.zone_id
# JOIN 
#     circle c ON c.circle_id = z.circle_id

# JOIN equipments e ON e.site_id=s.site_id
# LEFT JOIN 
#     vendors v ON v.id = e.vendor_id
# WHERE 
#     dm.category_id =2
# GROUP BY 
#     c.circle_name,
#     z.zone_name,
#     sz.subzone_name,
#     u.user_name,
#     e.site_id,
#     yf.frequency_count,
#     s.nssid,
#     st.site_type_name,
#     sg.site_group_name
# limit 10
	

############## equipments #############

# SELECT  
#     e.equipment_name, 
#     d.domain_name, 
#     v.vendor_name,
#     e.site_id AS site_id,
#     COUNT(e.site_id) OVER () AS total_equipment_count  
    
# FROM 
#     equipments e
# JOIN 
#     sites s ON s.site_id = e.site_id
# JOIN 
#     domains d ON d.domain_id = e.domain_id
# JOIN 
#     domain_type_mapping dm ON dm.domain_id = d.domain_id
# JOIN 
#     site_type_mapping stm ON stm.category_id = dm.category_id
# LEFT JOIN 
#     vendors v ON v.id = e.vendor_id

# WHERE 
#     s.nssid = 'IDUW104856'
# GROUP BY 
#     e.equipment_name, d.domain_name, v.vendor_name, e.site_id;






# SELECT  
#     jsonb_build_object(
#         'equipment_name', e.equipment_name,
#         'vendor_name', v.vendor_name,
#         'domain_name', d.domain_name
#     ) AS equipment_info,
#     e.site_id AS site_id,
#     COUNT(e.site_id) OVER () AS total_equipment_count  -- Total equipment count across all rows
    
# FROM 
#     equipments e
# JOIN 
#     sites s ON s.site_id = e.site_id
# JOIN 
#     site_mapping sm ON sm.site_id = s.site_id
# JOIN 
#     domains d ON d.domain_id = e.domain_id
# JOIN 
#     domain_type_mapping dm ON dm.domain_id = d.domain_id
# JOIN 
#     site_type_mapping stm ON stm.category_id = dm.category_id
# LEFT JOIN 
#     vendors v ON v.id = e.vendor_id

# WHERE 
#     s.nssid = 'INAS000198'
# GROUP BY 
#     e.equipment_name, d.domain_name, v.vendor_name, e.site_id;



	