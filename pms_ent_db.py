
# import psycopg2
# import pandas as pd
# import sys
# from psycopg2.extras import execute_values

from psycopg2.extras import execute_values
import psycopg2
import pandas as pd
import sys
import numpy
from psycopg2.extensions import register_adapter, AsIs

# def addapt_numpy_float64(numpy_float64):
#     return AsIs(numpy_float64)
# def addapt_numpy_int64(numpy_int64):
#     return AsIs(numpy_int64)
# register_adapter(numpy.float64, addapt_numpy_float64)
# register_adapter(numpy.int64, addapt_numpy_int64)


try:
    connection = psycopg2.connect(
        host="10.19.71.176",
        database="pms_db",
        user="psqladm",
        password="R%e6DgyQ"
    )
    cursor = connection.cursor()
    print("Connected to database")

    insert_query = """
         INSERT INTO ent_master_data_new (
         Circle_code, nssid, site_name, vendor_name,
         latitude, longitude, domain, node_name,
         sub_category, sub_category_1, scope, 
         category, bandwidth, bandwidth_unit, fra,top50,bandwidth_check,priority
    )    VALUES %s;
    """
    # Execute queries here
    
    df = pd.read_excel('PMS_Master_File_Ent_11_Nov.xlsx', sheet_name = 'Master_File_Ent')
    #df = pd.read_excel('pms_data_db_check.xlsx', sheet_name = 'Sheet1')

    #df=df.head()
    df =df.reset_index(drop = True)
    data_to_insert=[]
    #print("data frame",df)
    for i in range(len(df)):
        data = (
                df.loc[i]["CIRCLE_CODE"] if pd.notna(df.loc[i]["CIRCLE_CODE"]) else None,
                df.loc[i]["NSSID"] if pd.notna(df.loc[i]["NSSID"]) else None,
                df.loc[i]["SITE NAME"] if pd.notna(df.loc[i]["SITE NAME"]) else None,
                df.loc[i]["VENDOR NAME"] if pd.notna(df.loc[i]["VENDOR NAME"]) else None,
                df.loc[i]["LATITUDE"] if pd.notna(df.loc[i]["LATITUDE"]) else None,
                df.loc[i]["LONGITUDE"] if pd.notna(df.loc[i]["LONGITUDE"]) else None,
                df.loc[i]["DOMAIN"] if pd.notna(df.loc[i]["DOMAIN"]) else None,
                df.loc[i]["NODE NAME"] if pd.notna(df.loc[i]["NODE NAME"]) else None,
                df.loc[i]["SUB CATEGORY"] if pd.notna(df.loc[i]["SUB CATEGORY"]) else None,
                df.loc[i]["SUB CATEGORY 1"] if pd.notna(df.loc[i]["SUB CATEGORY 1"]) else None,
                df.loc[i]["SCOPE"] if pd.notna(df.loc[i]["SCOPE"]) else None,
                df.loc[i]["CATEGORY"] if pd.notna(df.loc[i]["CATEGORY"]) else None,
                df.loc[i]["BANDWIDTH"] if pd.notna(df.loc[i]["BANDWIDTH"]) else None,
                df.loc[i]["BANDWIDTH UNIT"] if pd.notna(df.loc[i]["BANDWIDTH UNIT"]) else None,
                df.loc[i]["FRA"] if pd.notna(df.loc[i]["TOP50"]) else None,
                df.loc[i]["TOP50"] if pd.notna(df.loc[i]["CATEGORY"]) else None,
                df.loc[i]["BANDWIDTH_CHECK"] if pd.notna(df.loc[i]["BANDWIDTH"]) else None,
                df.loc[i]["Priority"] if pd.notna(df.loc[i]["BANDWIDTH UNIT"]) else None,
                )
        data_to_insert.append(data)
        #print(i,data)
        # if df.loc[i]["BANDWIDTH"]>10:
        #     print(df.loc[i]["NODE NAME"])
        #     print("p1")
    execute_values(cursor, insert_query, data_to_insert)

        #cursor.execute(insert_query, data)
    connection.commit()
    
    print("Data inserted successfully")
    
    # connection.close()
    print("Connection closed")
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    line_no = exc_tb.tb_lineno
    filename = exc_tb.tb_frame.f_code.co_filename
    err_msg = f"Exception occurred at Function -> check line no. {line_no} in file {filename}: {e}"
    print(err_msg)


#############################

# CREATE TABLE your_table_name (
#     id SERIAL PRIMARY KEY,
#     CIRCLE_CODE VARCHAR(50),
#     NSSID VARCHAR(50),
#     SITE_NAME VARCHAR(100),
#     VENDOR_NAME VARCHAR(100),
#     LATITUDE FLOAT,
#     LONGITUDE FLOAT,
#     DOMAIN VARCHAR(100),
#     NODE_NAME VARCHAR(100),
#     SUB_CATEGORY VARCHAR(50),
#     SUB_CATEGORY_1 VARCHAR(50),
#     SCOPE VARCHAR(50),
#     CATEGORY VARCHAR(50),
#     BANDWIDTH INTEGER,
#     BANDWIDTH_UNIT VARCHAR(20),
#     FRA VARCHAR(50),
#     TOP50 BOOLEAN,
#     BANDWIDTH_CHECK BOOLEAN,
#     Priority INTEGER
# );

      