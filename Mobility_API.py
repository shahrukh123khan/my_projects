
# from sqlalchemy.orm import aliased

# def fetch_data_for_filter(db, circle_id=None, zone_id=None, subzone_id=None):
#     # Start building the query with the base table (assuming Circle as the starting point)
#     query = db.query(
#         Circle, Zone, SubZone, Domain, DomainType, Category, SiteType
#     ).join(Zone, Zone.circle_id == Circle.circle_id)  # Join Circle with Zone
#     query = query.join(SubZone, SubZone.zone_id == Zone.zone_id)  # Join Zone with SubZone
#     query = query.join(Domain, Domain.subzone_id == SubZone.subzone_id)  # Join SubZone with Domain
#     query = query.join(DomainType, Domain.domaintype_id == DomainType.domaintype_id)  # Domain with DomainType
#     query = query.join(Category, Category.category_id == Domain.category_id)  # Domain with Category
#     query = query.join(SiteType, SiteType.sitetype_id == Domain.sitetype_id)  # Domain with SiteType
    
#     # Apply filters based on the provided filter values
#     if circle_id:
#         query = query.filter(Circle.circle_id == circle_id)
#     if zone_id:
#         query = query.filter(Zone.zone_id == zone_id)
#     if subzone_id:
#         query = query.filter(SubZone.subzone_id == subzone_id)
    
#     # Execute the query and fetch results
#     results = query.all()
    
#     return results


# import logging
# import psycopg2
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, model_validator
# from typing import Optional
# from contextlib import contextmanager

# # Set up logging for debugging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# # Database URL (PostgreSQL connection string)
# #DATABASE_URL = "postgresql://psqladm:R%e6DgyQ@10.19.71.176/alarms"

# # Define a Pydantic model for the filters
# class FilterData(BaseModel):
#     zone: Optional[str] = None
#     subzone: Optional[str] = None
#     user_id: Optional[int] = None
#     domain_type: Optional[str] = None

#     # Convert fields to lowercase using model_validator
   

# # Context manager to handle the PostgreSQL connection and cursor
# @contextmanager
# def get_db_connection():
#     connection = psycopg2.connect(
#         host="10.19.71.176",
#         database="alarms",
#         user="psqladm",
#         password="R%e6DgyQ"
#     )
#     cursor = connection.cursor()
#     try:
#         yield cursor
#     finally:
#         cursor.close()
#         connection.commit()  
#         connection.close()

# # Initialize FastAPI app
# app = FastAPI()


# @app.post("/data")
# async def get_filtered_data(filters: FilterData):
#     # Start query with a base select
#     query = "SELECT * FROM site_type_data"
#     params = {}

#     # Add filters if provided
#     conditions = []
#     if filters.zone:
#         conditions.append("LOWER(zone) = %s")
#         params["zone"] = filters.zone  # Already converted to lowercase by Pydantic model
#     if filters.subzone:
#         conditions.append("LOWER(subzone) = %s")
#         params["subzone"] = filters.subzone  # Already converted to lowercase
#     if filters.user_id :
#         conditions.append("user_id = %s")
#         params["user_id"] = filters.user_id
#     if filters.domain_type:
#         conditions.append("LOWER(domain_type) = %s")
#         params["domain_type"] = filters.domain_type  # Already converted to lowercase

#     # If there are conditions, add them to the query
#     if conditions:
#         query += " WHERE " + " AND ".join(conditions)
    
#     # Add limit at the end
#     #query += " LIMIT "

#     # Debug: Print final query and parameters
#     print("Executing Query:", query)
#     print("With Parameters:", tuple(params.values()))

#     try:
#         with get_db_connection() as cursor:
#             # Execute query and fetch results
#             cursor.execute(query, tuple(params.values()))
#             results = cursor.fetchall()
#             #print("Result:", results)

#         # Return the results in a structured response
#         return {"data": results}

#     except Exception as e:
#         logger.error(f"Error occurred while querying the database: {e}")
#         raise HTTPException(status_code=500, detail="Database query failed")





# zone {    
#         int zoneID PK
#         string zone_name
#         int circleID FK
#     }

#     subZone {
#         int subZoneID PK
#         string subZoneHame
#         int zoneID FK
#     }


# equpmentType {
#         int equpmentTypeID PK
#         string equpmentTypeName
#         bool is_active

# CREATE TABLE zones (
#     zone_id SERIAL PRIMARY KEY,
#     zone_name VARCHAR(300) NOT NULL,
#     circle_id INT,
#     FOREIGN KEY (circle_id) REFERENCES circle(circle_id)
# );


# CREATE TABLE subzones (
#     subzone_id SERIAL PRIMARY KEY,
#     subzone_name VARCHAR(300) NOT NULL,
#     zone_id INT,
#     FOREIGN KEY (zone_id) REFERENCES zones(zone_id)
# );


# DROP TABLE subzones;


# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Circle(Base):
#     __tablename__ = 'circles'
    
#     circle_id = Column(Integer, primary_key=True)
#     circle_name = Column(String)

# class Zone(Base):
#     __tablename__ = 'zones'
    
#     zone_id = Column(Integer, primary_key=True)
#     zone_name = Column(String)
#     circle_id = Column(Integer, ForeignKey('circles.circle_id'))  # Foreign key to circles
    
#     circle = relationship("Circle")  # This creates a relationship to the Circle table

# class Subzone(Base):
#     __tablename__ = 'subzones'
    
#     subzone_id = Column(Integer, primary_key=True)
#     subzone_name = Column(String)
#     zone_id = Column(Integer, ForeignKey('zones.zone_id'))  # Foreign key to zones
    
#     zone = relationship("Zone")  # This creates a relationship to the Zone table

# class ZTM(Base):
#     __tablename__ = 'ztm'
    
#     ztm_id = Column(Integer, primary_key=True)
#     ztm_name = Column(String)


# from fastapi import FastAPI, HTTPException, Depends
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from pydantic import BaseModel

# # Database connection setup
# DATABASE_URL = "postgresql://username:password@localhost/dbname"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # FastAPI app setup
# app = FastAPI()

# # Pydantic models for request validation
# class RequestPayload(BaseModel):
#     circle_id: int
#     zone_id: int
#     subzone_id: int
#     ztm_id: int

# # Function to get a session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # FastAPI endpoint
# @app.post("/get-records/")
# async def get_records(payload: RequestPayload, db: Session = Depends(get_db)):
#     # Fetch records from circle, zone, subzone, and ztm tables based on the provided IDs
#     circle = db.query(Circle).filter(Circle.circle_id == payload.circle_id).first()
#     zone = db.query(Zone).filter(Zone.zone_id == payload.zone_id).first()
#     subzone = db.query(Subzone).filter(Subzone.subzone_id == payload.subzone_id).first()
#     ztm = db.query(ZTM).filter(ZTM.ztm_id == payload.ztm_id).first()

#     # If any record is not found, raise an HTTP exception
#     if not circle:
#         raise HTTPException(status_code=404, detail="Circle not found")
#     if not zone:
#         raise HTTPException(status_code=404, detail="Zone not found")
#     if not subzone:
#         raise HTTPException(status_code=404, detail="Subzone not found")
#     if not ztm:
#         raise HTTPException(status_code=404, detail="ZTM not found")

#     # Return the data as a dictionary
#     return {
#         "circle": {"circle_id": circle.circle_id, "circle_name": circle.circle_name},
#         "zone": {"zone_id": zone.zone_id, "zone_name": zone.zone_name, "circle_id": zone.circle_id},
#         "subzone": {"subzone_id": subzone.subzone_id, "subzone_name": subzone.subzone_name, "zone_id": subzone.zone_id},
#         "ztm": {"ztm_id": ztm.ztm_id, "ztm_name": ztm.ztm_name}
#     }



# ###################################direct postgres #######################
# import psycopg2
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, model_validator
# from typing import Optional

# # FastAPI app initialization
# app = FastAPI()

# # PostgreSQL connection details
# DB_HOST = "10.19.71.176"
# DB_PORT = "5432"
# DB_NAME = "alarms"
# DB_USER = "psqladm"
# DB_PASSWORD = "R%e6DgyQ"

# # Pydantic model for request validation
# class RequestData(BaseModel):
#     circle_id: Optional[str] = None
#     zone_id: Optional[str] = None
#     subzone_id: Optional[str] = None
#     user_id: Optional[int] = None

#     # @model_validator(mode='before')
#     # def convert_fields_to_lower(cls, values):
#     #     for field in ["zone_id", "subzone_id"]:
#     #         if field in values and values[field]:
#     #             values[field] = values[field].lower()
#     #     return values

# # Function to connect to PostgreSQL
# def get_db_connection():
#     conn = psycopg2.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD
#     )
#     return conn

# @app.post("/fetch-details/")
# async def fetch_details(request_data: RequestData):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Initialize response dictionary
#         response = {}

#         # Fetch circle name
#         if request_data.circle_id:
#             cursor.execute("SELECT circle_name FROM circle WHERE circle_id = %s", (request_data.circle_id,))
#             circle = cursor.fetchone()
#             if not circle:
#                 raise HTTPException(status_code=404, detail="Circle not found")
#             response["circle_name"] = circle[0]

#         # Fetch zone name
#         if request_data.zone_id:
#             cursor.execute("SELECT zone_name FROM zones WHERE zone_id = %s", (request_data.zone_id,))
#             zone = cursor.fetchone()
#             if not zone:
#                 raise HTTPException(status_code=404, detail="Zone not found")
#             response["zone_name"] = zone[0]

#         # Fetch subzone name
#         if request_data.subzone_id:
#             cursor.execute("SELECT subzone_name FROM subzones WHERE subzone_id = %s", (request_data.subzone_id,))
#             subzone = cursor.fetchone()
#             if not subzone:
#                 raise HTTPException(status_code=404, detail="Subzone not found")
#             response["subzone_name"] = subzone[0]

#         # Fetch details from another table based on these names
#         query = """
#             SELECT nssid, domain, user_name
#             FROM site_type_data
#             WHERE 1=1
#         """
#         params = []

#         # Dynamically add conditions based on available filters
#         if request_data.circle_id:
#             query += " AND circle_name = %s"
#             params.append(response["circle_name"])
#         if request_data.zone_id:
#             query += " AND zone_name = %s"
#             params.append(response["zone_name"])
#         if request_data.subzone_id:
#             query += " AND subzone_name = %s"
#             params.append(response["subzone_name"])
#         if request_data.user_id:
#             query += " AND user_id = %s"
#             params.append(request_data.user_id)

#         # Execute the query to fetch data from site_type_data
#         cursor.execute(query, tuple(params))
#         details = cursor.fetchall()

#         if not details:
#             raise HTTPException(status_code=404, detail="No details found")

#         # Include the fetched details in the response
#         response["details"] = details
#         return response

#     except psycopg2.Error as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

#     finally:
#         if conn:
#             cursor.close()
#             conn.close()




##############prefix processing ################
# def remove_prefix(input_string: str) -> str:
    
#     # Check and remove specific prefixes
#     prefixes = ["vi", "id"]
#     for prefix in prefixes:
#         if input_string.upper().startswith(prefix):  # Case-insensitive check
#             return input_string[len(prefix):].lstrip("_").strip()

#     # Check and remove anything before an underscore
#     if "_" in input_string:
#         return input_string.split("_", 1)[1].strip()

#     return input_string.strip()

# # Example usage
# strings = [
#     "vi_example",
#     "sd_example",
#     "prefix_example_with_details",
#     "example_name",
#     "example"
# ]

# # Testing the function
# for s in strings:
#     print(f"Original: '{s}' -> Processed: '{remove_prefix(s)}'")



# Repo - pms-web-apis
# Gitlab url : http://10.19.71.166/


# https://fastapi.tiangolo.com/tutorial/sql-databases/#herobase-the-base-class
# https://medium.com/@kasperjuunge/using-an-orm-with-fastapi-7eb6e54f5707

https://gitlab.com/akurmi@opentext.com/pms-web-api.git

# SELECT
#     d.domain_name,
#     c.category_no,
#     f.frequency_count,
#     dt.domaintype_name,
#     cir.circle_name,
#     z.zone_name,
#     sz.subzone_name,
#     s.nssid_name  -- Selecting nssid_name from the sites table
# FROM
#     domain d
# JOIN
#     domain_type dt ON d.domaintype_id = dt.domaintype_id  -- Join domain with domain_type on domaintype_id
# JOIN
#     category c ON d.category_id = c.category_id  -- Join domain with category on category_id
# JOIN
#     yearly_frequency f ON f.category_id = c.category_id  -- Join category with frequency on category_id
# JOIN
#     circle cir ON d.circle_id = cir.circleid  -- Join domain with circle on circle_id
# JOIN
#     zone z ON cir.circleid = z.circleid  -- Join circle with zone on circle_id
# JOIN
#     subzone sz ON z.zoneid = sz.zoneid  -- Join zone with subzone on zone_id
# JOIN
#     sites s ON d.domain_id = s.domain_id  -- Join domain with sites on domain_id (assuming domain_id is the linking column)
# WHERE
#     dt.domaintype_name = ?;  -- Pass domain_type_name dynamically


#############################################################################

# app/database.py
# mobility.py

import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List
import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus

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
   
# Build the DATABASE_URL for SQLAlchemy with SSL mode if required
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
   
# Log the full DATABASE_URL for debugging purposes
logging.debug(f"Using DATABASE_URL: {DATABASE_URL}")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=False)  # Disable echo for now

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for ORM models
Base = declarative_base()

# Define models
class DomainType(Base):
    __tablename__ = "domain_type"
    domaintype_id = Column(Integer, primary_key=True, index=True)
    domaintype_name = Column(String, index=True)
    created_date = Column(DateTime, default=func.now())  # Automatically set when record is created
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())  
    # Reverse relationship with Domain model
    domains = relationship("Domain", back_populates="domain_type")  # Add this line

class Domain(Base):
    __tablename__ = "domain"
    domain_id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String, index=True)
    domaintype_id = Column(Integer, ForeignKey('domain_type.domaintype_id'))
    category_id = Column(Integer, ForeignKey('category.category_id'))
    created_date = Column(DateTime, default=func.now())  # Automatically set when record is created
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now()) 
    # Correctly reference the 'domain_type' from DomainType model
    domain_type = relationship("DomainType", back_populates="domains")  # Existing relationship

    category = relationship("Category", back_populates="domains")

class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)
    category_no = Column(Integer)
    domains = relationship("Domain", back_populates="category")
    created_date = Column(DateTime, default=func.now())  # Automatically set when record is created
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now()) 
    frequencies = relationship("YearlyFrequency", back_populates="category")

class YearlyFrequency(Base):
    __tablename__ = "yearly_frequency"
    frequency_id = Column(Integer, primary_key=True, index=True)
    frequency_name = Column(String)
    frequency_count = Column(Integer)
    created_date = Column(DateTime, default=func.now())  # Automatically set when record is created
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now()) 
    category_id = Column(Integer, ForeignKey('category.category_id'))
    category = relationship("Category", back_populates="frequencies")

# Pydantic Schema for response
class DomainFrequencyResponse(BaseModel):
    domain_name: str
    category_no: int
    frequency_count: int
    domaintype_name: str

    class Config:
        from_attributes = True  # This allows us to convert ORM models directly to Pydantic models

# FastAPI app instance
app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to get domain frequency by domain type
@app.get("/domain/", response_model=List[DomainFrequencyResponse])
def get_domain(domaintype_name: str, db: Session = Depends(get_db)):
    try:
        # Log the query attempt
        logging.debug(f"Fetching domain frequency for domaintype_id: {domaintype_name}")

        # Query using SQLAlchemy ORM
        results = db.query(
            Domain.domain_name,
            Category.category_no,
            YearlyFrequency.frequency_count,
            DomainType.domaintype_name
        ).join(
            DomainType, Domain.domaintype_id == DomainType.domaintype_id
        ).join(
            Category, Domain.category_id == Category.category_id
        ).join(
            YearlyFrequency, YearlyFrequency.category_id == Category.category_id
        ).filter(
            DomainType.domaintype_name == domaintype_name
        ).all()

        # If no results found, raise 404
        if not results:
            logging.warning(f"No data found for domaintype_id: {domaintype_name}")
            raise HTTPException(status_code=404, detail="No data found")

        # Log successful results
        logging.debug(f"Found {len(results)} records for domaintype_id: {domaintype_name}")

        # Return the results as a list of Pydantic models
        return [
            DomainFrequencyResponse(
                domain_name=domain_name,
                category_no=category_no,
                frequency_count=frequency_count,
                domaintype_name=domaintype_name
            )
            for domain_name, category_no, frequency_count, domaintype_name in results
        ]
    
    except OperationalError as e:
        # Catch database connection related issues
        logging.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    except SQLAlchemyError as e:
        # Catch other database-related issues
        logging.error(f"Database query error: {e}")
        raise HTTPException(status_code=500, detail="Database query error")
    
    except Exception as e:
        # Catch unexpected errors
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")


# Example usage:
# result = check_connection()
# print(result)


# import psycopg2
# from psycopg2 import OperationalError

# # Database connection configuration
# DB_HOST = "10.19.71.176"
# DB_NAME = "alarms"
# DB_USER = "psqladm"
# DB_PORT = "5432"
# DB_PASSWORD = "R%e6DgyQ"

# def check_connection():
#     try:
#         # Debugging statement for starting connection attempt
#         print(f"Attempting to connect to the database at {DB_HOST}...")

#         # Connect to the PostgreSQL database without running any queries
#         connection = psycopg2.connect(
#             dbname=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             host=DB_HOST,
#             port=DB_PORT
#         )

#         # Debugging statement for successful connection
#         print(f"Connection established successfully to database: {DB_NAME} at {DB_HOST} on port {DB_PORT}")

#         # Return success message for connection
#         return {"status": "success", "message": "Database connection is successful."}

#     except OperationalError as e:
#         # Catch any operational errors (e.g., unable to connect to the database)
#         print(f"Connection failed. Error: {str(e)}")
#         return {"status": "error", "message": f"Connection failed: {str(e)}"}

#     finally:
#         # Close the connection to clean up
#         if 'connection' in locals():
#             connection.close()
#             print("Connection closed.")

# # Example usage:
# if __name__ == "__main__":
#     result = check_connection()
#     print(result)

# import logging
# from sqlalchemy import create_engine
# from sqlalchemy.exc import OperationalError
# from urllib.parse import quote_plus

# # Set up basic logging for debugging
# logging.basicConfig(level=logging.DEBUG)

# # Database connection configuration
# DB_HOST = "10.19.71.176"
# DB_NAME = "alarms"
# DB_USER = "psqladm"
# DB_PORT = "5432"
# DB_PASSWORD = "R%e6DgyQ"
# #DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# DB_PASSWORD = "R%e6DgyQ"
# encoded_password = quote_plus(DB_PASSWORD)  # URL-encode special characters

# DATABASE_URL = f"postgresql+psycopg2://psqladm:{encoded_password}@10.19.71.176:5432/alarms"
# print(f"Using DATABASE_URL: {DATABASE_URL}")

# # Log the full DATABASE_URL for debugging purposes
# logging.debug(f"Using DATABASE_URL: {DATABASE_URL}")

# # Create the database engine
# engine = create_engine(DATABASE_URL, echo=False)  # Disable echo for now

# def check_connection():
#     try:
#         logging.debug(f"Attempting to connect to the database at {DB_HOST}...")

#         # Test the connection without running a query
#         with engine.connect() as connection:
#             # Connection is successful
#             logging.debug(f"Connection established successfully to database: {DB_NAME} at {DB_HOST} on port {DB_PORT}")
        
#         return {"status": "success", "message": "Database connection is successful."}

#     except OperationalError as e:
#         # Log the specific error for operational issues
#         logging.error(f"Connection failed. OperationalError: {str(e)}")
#         return {"status": "error", "message": f"Connection failed: {str(e)}"}

#     except Exception as e:
#         # Catch any other unexpected errors
#         logging.error(f"Unexpected error occurred: {str(e)}")
#         return {"status": "error", "message": f"Unexpected error occurred: {str(e)}"}

#     finally:
#         logging.debug("Connection attempt finished.")

# # Example usage
# if __name__ == "__main__":
#     result = check_connection()
#     print(result)


# import logging
# from sqlalchemy import create_engine
# from sqlalchemy.exc import OperationalError
# from urllib.parse import quote_plus

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# # Database connection configuration
# DB_HOST = "10.19.71.176"
# DB_NAME = "alarms"
# DB_USER = "psqladm"
# DB_PORT = "5432"
# DB_PASSWORD = "R%e6DgyQ"
   
# # URL-encode the password to handle special characters properly
# encoded_password = quote_plus(DB_PASSWORD)
   
# # Build the DATABASE_URL for SQLAlchemy with SSL mode if required
# DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
   
# # Log the full DATABASE_URL for debugging purposes
# logging.debug(f"Using DATABASE_URL: {DATABASE_URL}")

# # Create the database engine
# engine = create_engine(DATABASE_URL, echo=False)  # Disable echo for now

# def check_connection():
#     try:
#         logging.debug(f"Attempting to connect to the database at {DB_HOST}...")

#         # Test the connection without running a query
#         with engine.connect() as connection:
#             # Connection is successful
#             logging.debug(f"Connection established successfully to database: {DB_NAME} at {DB_HOST} on port {DB_PORT}")
       
#         return {"status": "success", "message": "Database connection is successful."}

#     except OperationalError as e:
#         # Log the specific error for operational issues
#         logging.error(f"Connection failed. OperationalError: {str(e)}")
#         return {"status": "error", "message": f"Connection failed: {str(e)}"}

#     except Exception as e:
#         # Catch any other unexpected errors
#         logging.error(f"Unexpected error occurred: {str(e)}")
#         return {"status": "error", "message": f"Unexpected error occurred: {str(e)}"}

#     finally:
#         logging.debug("Connection attempt finished.")

# # Example usage
# if __name__ == "__main__":
#     result = check_connection()
#     print(result)


