
import requests
import json 
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import json
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2 import sql, extras
from core import config as cfg
import pandas as pd
import threading
from psycopg2 import sql, extras
import threading
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from collections import defaultdict, Counter
from pydantic import BaseModel


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Specify a list of origins in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods. You can specify a list of methods in production.
    allow_headers=["*"],  # Allows all headers. You can specify a list of headers in production.
)

# DB configuration
UHC_DB_HOST = "10.19.71.167"
UHC_DB_NAME = "uhc_main"
UHC_DB_USER = "postgres"
UHC_DB_PASS = "mM3IRLNUX[JU-E,"
UHC_DB_PORT = "5432"

# uso confugration 
USO_DB_HOST = "10.19.71.144"
USO_DB_NAME = "uso_chm_pc"
USO_DB_USER = "postgres"
USO_DB_PASS = "ZVadoCPjaplqT8Y"
USO_DB_PORT = "5432"

semaphore = threading.Semaphore(5)

def uhc_create_connection():
    connection = psycopg2.connect(
            user = UHC_DB_USER,
            password = UHC_DB_PASS,
            host = UHC_DB_HOST, 
            port = UHC_DB_PORT,  
            database = UHC_DB_NAME
        )
    return connection

def execute_query_uhc(query,params=None):
    try:
        connection = uhc_create_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        # connection.commit()
        result=cursor.fetchall()
        #print(result)
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return result  







def execute_query_with_para_uhc(query,params=None):
    try:
        connection = uhc_create_connection()
        cursor = connection.cursor()
        if params and not isinstance(params, tuple):
            params = (params,)
        #print("params in execute query",params)
        cursor.execute(query,params)
        #connection.commit()
        result=cursor.fetchall()
        #print(result)
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return result    


semaphore = threading.Semaphore(5)


def uso_create_connection():
    connection = psycopg2.connect(
            user = USO_DB_USER,
            password = USO_DB_PASS,
            host = USO_DB_HOST,  
            port = USO_DB_PORT,  
            database = USO_DB_NAME
        )
    return connection




def execute_query_uso(query):
    try:
        connection = uso_create_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        # connection.commit()
        result=cursor.fetchall()
        #print(result)
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return result  


def truncate_query_uso(query):
    try:
        connection = uso_create_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        #result=cursor.fetchall()
        #print(result)
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    #return result  


def execute_query_with_para_uso(query,params=None):
    try:
        connection = uso_create_connection()
        cursor = connection.cursor()
        cursor.execute(query,params)
        connection.commit()
        #result=cursor.fetchall()
        #print(result)
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    #return result    


def execute_query_with_para_uso2(query,params=None):
    try:
        print(query)
        connection = uso_create_connection()
        cursor = connection.cursor()
        cursor.execute(query,params)
        connection.commit()
        result=cursor.fetchall()
        print(result)
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return result   

@app.get("/get_uso_chart")
async def query():
    uhc_chart_dict = []
    cleaned_data = []
    
    # Corrected SQL query with JOIN
    select_query = """
        WITH data AS (
            SELECT *
            FROM software_chart_version
        ),
        latest_update AS (
            SELECT MAX(updated_at) AS latest_update_time
            FROM software_chart_version
        )
        SELECT data.*, latest_update.latest_update_time
        FROM data
        CROSS JOIN latest_update;
    """
    
    try:
        result = execute_query_uso(select_query)

        for data in result:
            # Adjust index according to your query result structure
            parent = data[1]
            name = data[2]
            color = data[3]
            chartID = data[4]
            value = data[5]
            last_updated = data[7]  # Adjust index to match your query result

            # Convert `datetime` to string if necessary
            if isinstance(last_updated, datetime):
                last_updated = last_updated.isoformat()

            json_data = {
                "parent": parent,
                "name": name,
                "color": color,
                "id": chartID,
                "value": value,
            }
            cleaned_data.append(json_data)
        
    
        # for item in cleaned_data:
        #     # Create a new dictionary excluding keys with `None` values
        #     cleaned_item = {k: v for k, v in item.items() if v is not 'null'}
        #     uhc_chart_dict.append(cleaned_item)
        for item in cleaned_data:
            # Remove keys with 'null' or None values, except for 'parent'
            cleaned_item = {k: v for k, v in item.items() if v not in ['null', None]}

            # Ensure 'parent' key is included if its value is 'null'
            if 'parent' in item and item['parent'] == 'null':
                cleaned_item['parent'] = item['parent']

            uhc_chart_dict.append(cleaned_item)

        print(uhc_chart_dict) 
        final_structure = {
            "data": uhc_chart_dict,  # The original list of dictionaries
            "last_updated": last_updated  # The timestamp
        }

        
    except Exception as e:
        print(f"Data is not available: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return JSONResponse(content=final_structure)



    
@app.get("/get_uhc_version")
async def query(ne_family: str = Query(None), oem: str = Query(None), ne_type: str = Query(None), current_sw_version: str = Query(None)):
    version = 'Null'
    lt_version='Null'
    message2 = "An error occurred"
    message = "No records found new records were inserted."
    status = False  
    status_code = 200  
    respone_dict=[]
    uhc_version_dict = []

    select_query = "SELECT *, created_at AS date FROM software_version;"

    ne_family = ne_family.lower() if ne_family else None
    oem_names = oem.lower() if oem else None
    ne_type_name = ne_type.lower() if ne_type else None
    current_sw_version_name= current_sw_version.lower() if current_sw_version else None

    select_query2=f"""SELECT *, created_at AS date  FROM software_version  WHERE LOWER(ne_family)  = {ne_family}  and  LOWER(oem) = {oem_names} and  LOWER(ne_type) ={ne_type_name}  and LOWER(current_sw_version) = {current_sw_version_name} """;  
    delete_query = "TRUNCATE TABLE software_version"
    #print("ne family with query para 1=",ne_family,type(ne_family))
   
    query=""" SELECT \n \n
                a.results,i.host,i.ip,i.model_no,d.domain,o.oem_name,ot.oem_type, TO_CHAR(a.created_at, 'DD-MM-YYYY HH24:MI:SS') AS Date  FROM automation_result a \n \n
              JOIN \n \n 
                inventory i ON a.inventory_id = i.s_no \n \n
              JOIN \n \n
                domain d ON i.domain_id = d.s_no \n \n
              JOIN \n \n
                oem o ON i.oem_id=o.s_no \n \n
              JOIN \n \n
                oem_type ot ON i.oem_id=ot.oem_id and i.oem_type_id=ot.s_no WHERE a.created_at:: DATE =CURRENT_DATE AND \n\n
                
                a.created_at::TIME BETWEEN '05:00:00' AND '11:00:00'""";
   
         
    if ne_family:
       # print("inside new query")
        query=f"""SELECT \n \n
                    a.results,i.host,i.ip,i.model_no,d.domain,o.oem_name,ot.oem_type, TO_CHAR(a.created_at, 'DD-MM-YYYY HH24:MI:SS') AS Date  FROM automation_result a \n \n
                JOIN \n \n 
                    inventory i ON a.inventory_id = i.s_no \n \n
                JOIN \n \n
                    domain d ON i.domain_id = d.s_no \n \n
                JOIN \n \n
                    oem o ON i.oem_id=o.s_no \n \n
                JOIN \n \n
                    oem_type ot ON i.oem_id=ot.oem_id and i.oem_type_id=ot.s_no WHERE a.created_at:: DATE =CURRENT_DATE AND \n\n
                    
                    a.created_at::TIME BETWEEN '06:00:00' AND '11:00:00' AND LOWER(d.domain) = {ne_family}""";
          
    nth_version_query="""WITH MaxVersions AS (  \n\n
                 SELECT ne_family, oem, ne_type, MAX(current_sw_version) AS max_version FROM software_version_copy  \n\n
                 where current_sw_version not like 'NA'and current_sw_version not like 'NOK'and current_sw_version not like 'OK' \n\n
                 GROUP BY ne_family, oem, ne_type ),  \n\n

                RankedVersions AS (   \n\n
                SELECT sv.ne_family, sv.oem, sv.ne_type, sv.current_sw_version,  \n\n
                ROW_NUMBER() OVER (PARTITION BY sv.ne_family, sv.oem, sv.ne_type ORDER BY sv.current_sw_version DESC) AS rn \n\n
                FROM software_version_copy sv  \n\n
                JOIN MaxVersions mv  \n\n
                ON sv.ne_family = mv.ne_family \n\n
                AND sv.oem = mv.oem  \n\n
                AND sv.ne_type = mv.ne_type  \n\n
                AND sv.current_sw_version = mv.max_version)  \n\n
                SELECT ne_family, oem, ne_type, current_sw_version \n\n
                FROM RankedVersions \n\n
                WHERE rn = 1 \n\n
                ORDER BY current_sw_version DESC""";

    try:
        if ne_family:
            result = execute_query_with_para_uhc(query)
            #print("result =",result)
        result = execute_query_with_para_uhc(query)
        #print("result",result)

        for data in result:
            try:
                version_dict = data[0]
                hostname=data[1]
                ip_address = data[2]
                model = data[3]
                domain = data[4]
                oem_type = data[6]
                oem_name = data[5]
                created_at = data[7]
                created_at_str = str(created_at)
                dict_list = json.loads(version_dict)
                # print("ne family in data",domain)
                # print("oem_ype",oem_type)
                # print("oem name",oem_name)
                # print("model",model)
                # print("ip_address",ip_address)
            
                for item in dict_list:
                    if item.get('name') in ['Version', 'version']:
                        cell_value = item.get('cell_value', 'Null')
                        #print("cell value",cell_value,type(cell_value))
                        if cell_value == 'NOK' or cell_value =='OK':
                            cell_value='NA'
                        if isinstance('cell_value',str):
                            versions=str(cell_value).strip()
                            version = versions.strip()
                        else:
                            version=str(cell_value).strip() 
                            version = versions.strip() 
                
                json_data = {
                    "NE Family": domain,
                    "NE Type": oem_type,
                    "OEM Name": oem_name,
                    "Model": model,
                    "Hostname":hostname,
                    "Ip_Address": ip_address,
                    "Version": version,
                    "created_at":created_at_str
                }
                
                uhc_version_dict.append(json_data)
            
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                continue  # Skip this item and continue with the next one
            except Exception as e:
                print(f"Error processing data: {e}")
                continue

        print(uhc_version_dict[0], len(uhc_version_dict))

        select_result = execute_query_uso(select_query)
        # select_result = execute_query_uso()
        #print("Select query result =", select_result)

        if len(select_result) == 0:
            message = "data successfully found ."
            status = True 
            for data in uhc_version_dict:
                #print("inside if")
                ne_family = data['NE Family']
                #print("ne family",ne_family)         #uper IP Core
                domain_dict = {
                    'Core': ['STP/DRA', 'VOLTE','Paco','CLOUD','UDR/HSS/NDS','SIP TRUNKING'],
                    'IN/VAS': ['IN', 'VAS'],
                    'IP': ['IP Core', 'SDN CONTROLLER'],
                    'Optical': ['DWDM', 'OPTICAL'],
                    'Access': ['RAN', 'MW']
                }
                
                for category, items in domain_dict.items():
                    if ne_family.lower() in (item.lower() for item in items):
                        dm=category
                        
                        #print("dm value ",dm)
                domain=dm
                    
                #print("domain",domain)
                oem = data['NE Type']
                ne_type = data['OEM Name']
                model_name = data['Model']
                hostname=data['Hostname']
                ip_address = data['Ip_Address']
                current_sw_version = data['Version'].strip()
                created_at_str = data['created_at']
                latest_sw_version = None
                insert_query = """
                INSERT INTO software_version (domain, ne_family, oem, ne_type, model_name, ip_address, current_sw_version, latest_sw_version,hostname, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
                """
                query_para = (domain, ne_family, oem, ne_type, model_name, ip_address, current_sw_version, latest_sw_version,hostname,created_at_str)
                
                try:
                    response = execute_query_with_para_uso(insert_query, query_para)
                except Exception as e:
                    print(f"Error inserting data: {e}")
                    continue  # Skip this record and continue with the next one
        nth_result = execute_query_uso(nth_version_query)
        if nth_result:
            message = "data successfully found ."
            status = True 
            print("inside the nth version")
            truncate_result = truncate_query_uso(delete_query) 
            for data in uhc_version_dict:
                    for tup in nth_result:
                        tup_dict = {
                            'NE Family': tup[0],
                            'OEM Name': tup[1],
                            'NE Type': tup[2],
                            'Version': tup[3]
                        }  
                        if (data['NE Family']==tup_dict['NE Family']  and data['OEM Name']==tup_dict['OEM Name'] and data['NE Type']==tup_dict['NE Type']):
                            lt_version=tup_dict['Version']
                    
                    #print(lt_version)    
                    ne_family = data['NE Family']
                    #print("ne family",ne_family)         #uper IP Core
                    domain_dict = {
                        'Core': ['STP/DRA', 'VOLTE','Paco','CLOUD','UDR/HSS/NDS','SIP TRUNKING'],
                        'IN/VAS': ['IN', 'VAS'],
                        'IP': ['IP Core', 'SDN CONTROLLER'],
                        'Optical': ['DWDM', 'OPTICAL'],
                        'Access': ['RAN', 'MW']
                    }
                    
                    for category, items in domain_dict.items():
                        if ne_family.lower() in (item.lower() for item in items):
                            dm=category
                            
                    domain=dm
                        
                    #print("domain",domain)
                    oem = data['OEM Name']
                    ne_type = data['NE Type']
                    model_name = data['Model']
                    ip_address = data['Ip_Address']
                    current_sw_version = data['Version'].strip()
                    latest_sw_version = lt_version
                    hostname=data['Hostname']
                    created_at_str = data['created_at']
                    insert_query = """
                    INSERT INTO software_version (domain, ne_family, oem, ne_type, model_name, ip_address, current_sw_version, latest_sw_version,hostname, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    query_para = (domain, ne_family, oem, ne_type, model_name, ip_address, current_sw_version, latest_sw_version,hostname, created_at_str)
                    
                    try:
                        response = execute_query_with_para_uso(insert_query, query_para)
                    except Exception as e:
                        print(f"Error inserting data: {e}")
                        continue  # Skip this record and continue with the next one
            select_result = execute_query_uso(select_query)
            

        else:
            message = "data successfully found ."
            status = True 
            truncate_result = truncate_query_uso(delete_query)            
            for data in uhc_version_dict:
                ne_family = data['NE Family']
                #print("ne family",ne_family)
                domain_dict = {
                    'Core': ['STP/DRA', 'VOLTE','Paco','CLOUD','UDR/HSS/NDS','SIP TRUNKING'],
                    'IN/VAS': ['IN', 'VAS'],
                    'IP': ['IP Core', 'SDN CONTROLLER'],
                    'Optical': ['DWDM', 'OPTICAL'],
                    'Access': ['RAN', 'MW']
                }

                for category, items in domain_dict.items():
                    if ne_family.lower() in (item.lower() for item in items):
                        dm=category
                        
                domain=dm
                    
                oem = data['NE Type']
                ne_type = data['OEM Name']
                model_name = data['Model']
                hostname=data['Hostname']
                ip_address = data['Ip_Address']
                current_sw_version = data['Version'].strip()
                created_at_str = data['created_at']
                latest_sw_version = None
                # print("domain table=",domain)
                # print("ne family table=",ne_family)
                # print("oem down tabe=",oem)
                # print("ne type table=",ne_type)
                insert_query = """
                INSERT INTO software_version (domain, ne_family, oem, ne_type, model_name, ip_address, current_sw_version, latest_sw_version,hostname ,created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s)
                """
                query_para = (domain, ne_family, oem, ne_type, model_name, ip_address, current_sw_version, latest_sw_version,hostname, created_at_str)
                
                try:
                    response = execute_query_with_para_uso(insert_query, query_para)
                except Exception as e:
                    print(f"Error inserting data: {e}")
                    continue  # Skip this record and continue with the next one
            #select_result = execute_query_uso(select_query) 
        nth_result = execute_query_uso(nth_version_query)
        if nth_result:
            message = "data successfully found ."
            status = True 
            print("inside the nth version")
            truncate_result = truncate_query_uso(delete_query) 
            for data in uhc_version_dict:
                    for tup in nth_result:
                        tup_dict = {
                            'NE Family': tup[0],
                            'OEM Name': tup[1],
                            'NE Type': tup[2],
                            'Version': tup[3]
                        }  
                        if (data['NE Family']==tup_dict['NE Family']  and data['OEM Name']==tup_dict['OEM Name'] and data['NE Type']==tup_dict['NE Type']):
                            lt_version=tup_dict['Version']
                    
                    #print(lt_version)    
                    ne_family = data['NE Family']
                    #print("ne family",ne_family)         #uper IP Core
                    domain_dict = {
                        'Core': ['STP/DRA', 'VOLTE','Paco','CLOUD','UDR/HSS/NDS','SIP TRUNKING'],
                        'IN/VAS': ['IN', 'VAS'],
                        'IP': ['IP Core', 'SDN CONTROLLER'],
                        'Optical': ['DWDM', 'OPTICAL'],
                        'Access': ['RAN', 'MW']
                    }
                    
                    for category, items in domain_dict.items():
                        if ne_family.lower() in (item.lower() for item in items):
                            dm=category
                            
                    domain=dm
                        
                    #print("domain",domain)
                    oem = data['OEM Name']
                    ne_type = data['NE Type']
                    model_name = data['Model']
                    ip_address = data['Ip_Address']
                    current_sw_version = data['Version'].strip()
                    latest_sw_version = lt_version
                    hostname=data['Hostname']
                    created_at_str = data['created_at']
                    
                    insert_query = """
                    INSERT INTO software_version (domain, ne_family, oem, ne_type, model_name, ip_address, current_sw_version, latest_sw_version,hostname, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
                    """
                    query_para = (domain, ne_family, oem, ne_type, model_name, ip_address, current_sw_version, latest_sw_version,hostname, created_at_str)
                    
                    try:
                        response = execute_query_with_para_uso(insert_query, query_para)
                    except Exception as e:
                        print(f"Error inserting data: {e}")
                        continue  # Skip this record and continue with the next one
            select_result = execute_query_uso(select_query)
        
        print(ne_family, oem_names, ne_type_name , current_sw_version_name)
        if ne_family !=None and oem_names !=None  and ne_type_name !=None and current_sw_version_name !=None : 
            print('hit')
            select_result = execute_query_with_para_uso2(select_query2)
            # print(select_result)
        for data in select_result:
            # print("response data",data)
            domain=data[0]    
            ne_family=data[1]
            oem=data[2]
            
            ne_type=data[3]
            model_name=data[4]
            ip_address=data[5]
            current_sw_version=data[6]
            latest_sw_version=data[7]
            hostname=data[8]
            created_at = data[9]
            created_at_str = created_at.isoformat() if isinstance(created_at, datetime) else str(created_at)

            new_json_data = {
                    "domain":domain,
                    "NE Family": ne_family,
                    "OEM Name": oem,
                    "NE Type":  ne_type,
                    "Model": model_name,
                    "Hostname":hostname,
                    "Ip_Address": ip_address,
                    "current_sw_version":current_sw_version,
                    "latest_sw_version":latest_sw_version,
                    "date": created_at_str
                }
            respone_dict.append(new_json_data)
   
        return JSONResponse(
            content={
                "data": respone_dict,
                "status": status,  
                "message": message, 
                },
                status_code=200
            )
    except Exception as e:
        print(f"Data is not available: {e}")
        status_code = 500  
        message = "Internal Server Error"  
        status = False  
        raise HTTPException(status_code=status_code, detail=message)








class DataModel(BaseModel):
    domain: str
    ne_family: str
    ne_type: str
    oem: str


@app.post("/get_version_count")
async def query(data: DataModel):

# async def query(domain: str = Query(None),ne_family: str = Query(None), oem: str = Query(None), ne_type: str = Query(None)):
    message = "An error occurred"
    status = False  
    status_code = 200  
    respone_dict=[]
    uhc_version_dict = []
    uhc_version_dict2 = []
    formatted_data = []
    seen_combinations = set()  
    #ne_family = ne_family.lower() if ne_family else None
    set_uhc = set()
    set_uhc2 = set()
    set_uhc_count={}

    domain = data.domain
    ne_family = data.ne_family
    ne_type = data.ne_type
    oem = data.oem

    domain = None if str(domain) == 'null' else str(domain)
    ne_family = None if str(ne_family) == 'null' else str(ne_family)
    ne_type = None if str(ne_type) == 'null' else str(ne_type)
    oem = None if str(oem) == 'null' else str(oem)

    domains = domain.lower() if domain else None
    ne_familys = ne_family.lower() if ne_family else None
    oem_names = oem.lower() if oem else None
    ne_type_name = ne_type.lower() if ne_type else None
    
    select_query = "SELECT * FROM software_version_one"
    delete_query = "TRUNCATE TABLE software_version_one"
    #print("ne family with query para 1=",ne_family,type(ne_family))
    select_query1=f"""SELECT *  FROM software_version_one  WHERE LOWER(domain)  = '{domains}' """;  
    select_query2=f"""SELECT *  FROM software_version_one  WHERE LOWER(domain)  = '{domains}' and LOWER(ne_family)  = '{ne_familys}' """;  
    select_query3=f"""SELECT *  FROM software_version_one  WHERE LOWER(domain)  = '{domains}' and LOWER(ne_family)  = '{ne_familys}'  and  LOWER(ne_type) = '{ne_type_name}'  """;  
    select_query4=f"""SELECT *  FROM software_version_one  WHERE LOWER(domain)  = '{domains}' and LOWER(ne_family)  = '{ne_familys}'  and  LOWER(oem) = '{oem_names}' and  LOWER(ne_type) = '{ne_type_name}' """;  
   
    # query2=""" SELECT \n \n
    #                 d.domain,o.oem_name,ot.oem_type FROM automation_result a \n \n
    #             JOIN \n \n 
    #                 inventory i ON a.inventory_id = i.s_no \n \n
    #             JOIN \n \n
    #                 domain d ON i.domain_id = d.s_no \n \n
    #             JOIN \n \n
    #                 oem o ON i.oem_id=o.s_no \n \n
    #             JOIN \n \n
    #                 oem_type ot ON i.oem_id=ot.oem_id and i.oem_type_id=ot.s_no""";

    query = """
        SELECT \n \n
                d.domain,o.oem_name,ot.oem_type,a.results FROM automation_result a \n \n
        JOIN   \n \n
            inventory i ON a.inventory_id = i.s_no  \n \n
        JOIN   \n \n
            domain d ON i.domain_id = d.s_no   \n \n
        JOIN  \n \n
            oem o ON i.oem_id = o.s_no  \n \n
        JOIN  \n \n
            oem_type ot ON i.oem_id = ot.oem_id AND i.oem_type_id = ot.s_no  \n \n
        WHERE  \n \n
            a.created_at::DATE = CURRENT_DATE AND a.created_at::TIME BETWEEN '06:00:00' AND '11:00:00'""";
    
    # if ne_family:
    #    # print("inside new query")
    #     query=f"""SELECT \n \n
    #             d.domain,o.oem_name,ot.oem_type,a.results FROM automation_result a \n \n
    #             JOIN \n \n 
    #                 inventory i ON a.inventory_id = i.s_no \n \n
    #             JOIN \n \n
    #                 domain d ON i.domain_id = d.s_no \n \n
    #             JOIN \n \n
    #                 oem o ON i.oem_id=o.s_no \n \n
    #             JOIN \n \n
    #                 oem_type ot ON i.oem_id=ot.oem_id and i.oem_type_id=ot.s_no WHERE a.created_at:: DATE =CURRENT_DATE AND \n\n
                    
    #                 a.created_at::TIME BETWEEN '06:00:00' AND '11:00:00' AND LOWER(d.domain) = {ne_family}""";
    try:
    
        result = execute_query_with_para_uhc(query)
        for data in result:
            try:
                ne_family = data[0]
                oem_type = data[1]
                oem_name = data[2]
                version_dict = data[3]
                set_uhc.add(ne_family)
                dict_list = json.loads(version_dict)
                for item in dict_list:
                    if item.get('name') in ['Version', 'version']:
                        cell_value = item.get('cell_value', 'Null')
                        #print("cell value",cell_value,type(cell_value))
                        if isinstance('cell_value',str):
                            version=str(cell_value).strip()  
                        else:
                            version=str(cell_value).strip()    
                
                json_data = {
                    "NE Family": ne_family,
                    "NE Type": oem_type,
                    "OEM Name": oem_name,
                    "Version": version,
                }
                
                uhc_version_dict.append(json_data)
            
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                continue  
            except Exception as e:
                print(f"Error processing data: {e}")
                continue
        list_uhc = list(set_uhc)
        for value in list_uhc:
            i = value
            # for key, values in data.items():
            for item in uhc_version_dict:

                keys_list = list(item.keys())[0]
                second = list(item.keys())[2]
                # print(second)
                # second_value = data[second_key]
                if i ==item[keys_list]:
                    # print(i ,"+++++++++++++", second)
                    second_value = item[second]
                    # print(second_value)
                    set_uhc2.add(second_value)

            set_uhc_count[i] = len(set_uhc2)  

            set_uhc2=set()
            # print(len(set_uhc2))
        # print('set_uhc_count',set_uhc_count)


        # Dictionary to store aggregated data
        aggregated_data = defaultdict(lambda: {
            "domain": "",
            "NE Family": "",
            "NE Type": "",
            "OEM Name": "",
            "Version": []  # Initialize a list to hold versions
        })

        # Process each entry
        for entry in uhc_version_dict:
            # Create a key based on common fields
            key = (entry["NE Family"],entry["NE Type"], entry["OEM Name"])
            
            # Update the aggregated data with versions
            aggregated_data[key]["NE Family"] = entry["NE Family"]
            aggregated_data[key]["NE Type"] = entry["OEM Name"]
            aggregated_data[key]["OEM Name"] = entry["NE Type"] 
            aggregated_data[key]["Version"].append(entry["Version"])  # Append version to list

        # Convert the aggregated data back into a list of dictionaries
        results = []
        for item in aggregated_data.values():
            # Count total and unique versions
            total_versions = len(item["Version"])
            version_counts = Counter(item["Version"])
            unique_version_count = len(version_counts)
            
            # Prepare the result with counts and unique version counts
            results.append({
                "NE Family": item["NE Family"],
                "NE Type": item["OEM Name"],
                "OEM Name":  item["NE Type"],
                "Total Versions": total_versions,
                "Unique Versions": unique_version_count,
                "Version Counts": dict(version_counts)
            })

        result_list = []
        skip_values = {"NOK", "NA","Credential Issue", "Command failed to execute"}  # Set of values to skip
        select_result = execute_query_uso(select_query)

        if len(select_result) == 0:
            print('if block')
            message = "No records found new records were inserted."
            status = True 
            for data in uhc_version_dict:
                ne_family = data['NE Family']
                domain_dict = {
                    'Core': ['STP/DRA', 'VOLTE','Paco','CLOUD','UDR/HSS/NDS','SIP TRUNKING'],
                    'IN/VAS': ['IN', 'VAS'],
                    'IP': ['IP Core', 'SDN CONTROLLER'],
                    'Optical': ['DWDM', 'OPTICAL'],
                    'Access': ['RAN', 'MW']
                }
                
                for category, items in domain_dict.items():
                    if ne_family.lower() in (item.lower() for item in items):
                        dm=category
            
                if ne_family  in set_uhc_count:
                    value =  set_uhc_count[ne_family]

                domain=dm
                ne_family = data['NE Family']
                ne_family_count =  value
                oem = data['NE Type']
                ne_type = data['OEM Name']
                
                for entry in results:
                    if entry['NE Family'] == ne_family and entry['NE Type'] == oem and entry['OEM Name'] == ne_type:
                        # Filter out unwanted version counts
                        filtered_version_counts = {version: count for version, count in entry['Version Counts'].items() if version not in skip_values}
                        
                        result_list.append({
                            "Total Versions": sum(filtered_version_counts.values()),  # Total versions after filtering
                            "Version Counts": filtered_version_counts
                        })
                        break    
                
                version =   json.dumps(result_list)
                result_list.clear()
                # json_data2 = {
                #         "domain": domain,
                #         "NE Family": ne_family,
                #         "NE Family Count": ne_family_count,
                #         "NE Type": ne_type,
                #         "OEM Name": oem,
                #         "Version": version,

                #     }
                # uhc_version_dict2.append(json_data2)
                
                insert_query = """
                INSERT INTO software_version_one (domain, ne_family, ne_family_count, oem, ne_type, version)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                query_para = (domain, ne_family, ne_family_count, oem, ne_type, version)
                
                try:
                    response = execute_query_with_para_uso(insert_query, query_para)
                except Exception as e:
                    print(f"Error inserting data: {e}")
                    continue  # Skip this record and continue with the next one            

            print(ne_familys, oem_names, ne_type_name)
        
            queries = {
                (False, False, False, False): select_query,
                (True, False, False, False): select_query1,
                (True, True, False, False): select_query2,
                (True, True, True, False): select_query3,
                (True, True, True, True): select_query4
            }

            key = (domains is not None, ne_familys is not None, ne_type_name is not None, oem_names is not None)
            select_result = execute_query_with_para_uso2(queries.get(key)) if key in queries else None

            keys = ['id', 'domain', 'NE Family', 'NE Family Count', 'NE Type', 'OEM Name', 'Version']

            # Convert each tuple to a dictionary
            uhc_version_dict2 = [dict(zip(keys, values)) for values in select_result]

            for item in uhc_version_dict2:
            # Parse the 'Version' field which is a JSON string
                version_info = json.loads(item["Version"])[0]

                # Extract 'Version Counts' details and convert to a list of dictionaries
                for version, count in version_info["Version Counts"].items():
                    # Create a tuple of (NE Family, OEM Name) to check for uniqueness
                    combination = (item["NE Family"], item["OEM Name"], item["NE Type"], version)

                    if combination not in seen_combinations:
                        # Add the combination to the set
                        seen_combinations.add(combination)

                        # Create a new dictionary with the desired structure
                        formatted_item = {
                            "domain": item["domain"],
                            "NE Family": item["NE Family"],
                            "NE Type": item["OEM Name"],
                            "OEM Name": item["NE Type"],
                            "Node count": count,  # Using the version count as node count
                            "Current sw version": version  # Extracting version string
                        }
                        # Add the formatted item to the result list
                        formatted_data.append(formatted_item)  
            select_result = execute_query_uso(select_query)

        else:
            print('else block')

            message = "Records were found; existing records were replaced."
            status = True 
            truncate_result = truncate_query_uso(delete_query) 
            for data in uhc_version_dict:
                ne_family = data['NE Family']
                domain_dict = {
                    'Core': ['STP/DRA', 'VOLTE','Paco','CLOUD','UDR/HSS/NDS','SIP TRUNKING'],
                    'IN/VAS': ['IN', 'VAS'],
                    'IP': ['IP Core', 'SDN CONTROLLER'],
                    'Optical': ['DWDM', 'OPTICAL'],
                    'Access': ['RAN', 'MW']
                }
                
                for category, items in domain_dict.items():
                    if ne_family.lower() in (item.lower() for item in items):
                        dm=category
            
                if ne_family  in set_uhc_count:
                    value =  set_uhc_count[ne_family]

                domain=dm
                ne_family = data['NE Family']
                ne_family_count =  value
                oem = data['NE Type']
                ne_type = data['OEM Name']
                
                for entry in results:
                    if entry['NE Family'] == ne_family and entry['NE Type'] == oem and entry['OEM Name'] == ne_type:
                        # Filter out unwanted version counts
                        filtered_version_counts = {version: count for version, count in entry['Version Counts'].items() if version not in skip_values}
                        
                        result_list.append({
                            "Total Versions": sum(filtered_version_counts.values()),  # Total versions after filtering
                            "Version Counts": filtered_version_counts
                        })
                        break    
                
                version =   json.dumps(result_list)
                result_list.clear()
                # json_data2 = {
                #         "domain": domain,
                #         "NE Family": ne_family,
                #         "NE Family Count": ne_family_count,
                #         "NE Type": ne_type,
                #         "OEM Name": oem,
                #         "Version": version,

                #     }
                # uhc_version_dict2.append(json_data2)
                
                insert_query = """
                INSERT INTO software_version_one (domain, ne_family, ne_family_count, oem, ne_type, version)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                query_para = (domain, ne_family, ne_family_count, oem, ne_type, version)
                
                try:
                    response = execute_query_with_para_uso(insert_query, query_para)
                except Exception as e:
                    print(f"Error inserting data: {e}")
                    continue  # Skip this record and continue with the next one            


            print(ne_familys, oem_names, ne_type_name)
        
            queries = {
                (False, False, False, False): select_query,
                (True, False, False, False): select_query1,
                (True, True, False, False): select_query2,
                (True, True, True, False): select_query3,
                (True, True, True, True): select_query4
            }

            key = (domains is not None, ne_familys is not None, ne_type_name is not None, oem_names is not None)
            select_result = execute_query_with_para_uso2(queries.get(key)) if key in queries else None

            keys = ['id', 'domain', 'NE Family', 'NE Family Count', 'NE Type', 'OEM Name', 'Version']

            # Convert each tuple to a dictionary
            uhc_version_dict2 = [dict(zip(keys, values)) for values in select_result]

                
            for item in uhc_version_dict2:
            # Parse the 'Version' field which is a JSON string
                version_info = json.loads(item["Version"])[0]

                # Extract 'Version Counts' details and convert to a list of dictionaries
                for version, count in version_info["Version Counts"].items():
                    # Create a tuple of (NE Family, OEM Name) to check for uniqueness
                    combination = (item["NE Family"], item["OEM Name"], item["NE Type"], version)

                    if combination not in seen_combinations:
                        # Add the combination to the set
                        seen_combinations.add(combination)

                        # Create a new dictionary with the desired structure
                        formatted_item = {
                            "domain": item["domain"],
                            "NE Family": item["NE Family"],
                            "NE Type": item["OEM Name"],
                            "OEM Name": item["NE Type"],
                            "Node count": count,  # Using the version count as node count
                            "Current sw version": version  # Extracting version string
                        }
                        # Add the formatted item to the result list
                        formatted_data.append(formatted_item)  

        return JSONResponse(formatted_data)

    except Exception as e:
        print(f"Data is not available: {e}")
        status_code = 500  
        message = "Internal Server Error"  
        status = False  
        raise HTTPException(status_code=status_code, detail=message)

@app.get("/table_data_domain_netype")
async def query(domain:str = Query(None),ne_family: str = Query(None), oem: str = Query(None), ne_type: str = Query(None)):

    # Corrected SQL query with JOIN
    if ne_family and oem and ne_type:
        select_query = f"""
            with maxv as (
                select
                    domain,
                    ne_family,
                    ne_type,
                    oem ,
                    current_sw_version,
                    MAX(current_sw_version) over (partition by ne_type  order by ne_type) as maxversion
                from
                    software_version_copy sv
                    where current_sw_version != 'NA')
                select *, COUNT(*) from maxv
                where ne_family = '{ne_family}' and ne_type = '{ne_type}' and oem = '{oem}'
                group by "domain" , ne_family , oem,  ne_type , current_sw_version,  maxversion
        """
    elif ne_family and ne_type:
        select_query = f"""
            with maxv as (
                select
                    domain,
                    ne_family,
                    ne_type,
                    oem ,
                    current_sw_version,
                    MAX(current_sw_version) over (partition by ne_type  order by ne_type) as maxversion
                from
                    software_version_copy sv
                    where current_sw_version != 'NA')
                select *, COUNT(*) from maxv
                where ne_family = '{ne_family}' and ne_type = '{ne_type}'
                group by "domain" , ne_family , oem,  ne_type , current_sw_version,  maxversion
        """
    elif ne_family:
        select_query = f"""
            with maxv as (
                select
                    domain,
                    ne_family,
                    ne_type,
                    oem ,
                    current_sw_version,
                    MAX(current_sw_version) over (partition by ne_type  order by ne_type) as maxversion
                from
                    software_version_copy sv
                    where current_sw_version != 'NA')
                select *, COUNT(*) from maxv
                where ne_family = '{ne_family}'
                group by "domain" , ne_family , oem,  ne_type , current_sw_version,  maxversion
        """

    try:
        result = execute_query_uso(select_query)
        final_structure = {
            "data": result
        }


    except Exception as e:
        print(f"Data is not available: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return JSONResponse(content=final_structure)
