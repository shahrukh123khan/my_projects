
# # site type master data complete columns

from psycopg2.extras import execute_values
import psycopg2
import pandas as pd
import sys
import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import sys

# # Define the table truncate query

# try:
#     connection = psycopg2.connect(
#         host="10.19.71.176",
#         database="alarms",
#         user="psqladm",
#         password="R%e6DgyQ"
#     )
#     cursor = connection.cursor()

#     # Insert query with all columns
#     insert_query = """
#         INSERT INTO site_type_data (
#             circle_code, nssid, site_name, vendor_name, latlong, domain, 
#             node_name, sub_category, sub_category_1, category, scope, 
#             site_type, site_type_vi, site_type_infra, frequency_of_pm_yearly, 
#             proposed_frequency, synergy, kpi, alarm, zone, subzone, 
#             uwfm_circle_codes, uwfm_circle_name, uwfm_circle_subzone_name, 
#             remove_vi_uwfm_csz, remove_id_uwfm_csz, user_id, user_name, 
#             full_name, email_id
#         ) VALUES %s;
#     """

#     # Load the data from Excel
#     df = pd.read_excel('Site_Type_Master_file_data_Nov12.xlsx', sheet_name='Site_Type_Master_file_data_Nov1')
#     df = df.head(10)    
#     print("Excel file read complete")
#     df = df.reset_index(drop=True)

#     # Prepare data for bulk insertion
#     data_to_insert = []
#     for i in range(len(df)):
#         data = (
#             df.loc[i]["CIRCLE_CODE"] if pd.notna(df.loc[i]["CIRCLE_CODE"]) else None,
#             df.loc[i]["NSSID"] if pd.notna(df.loc[i]["NSSID"]) else None,
#             df.loc[i]["SITE_NAME"] if pd.notna(df.loc[i]["SITE_NAME"]) else None,
#             df.loc[i]["VENDOR_NAME"] if pd.notna(df.loc[i]["VENDOR_NAME"]) else None,
#             df.loc[i]["LATLONG"] if pd.notna(df.loc[i]["LATLONG"]) else None,
#             df.loc[i]["DOMAIN"] if pd.notna(df.loc[i]["DOMAIN"]) else None,
#             df.loc[i]["NODE_NAME"] if pd.notna(df.loc[i]["NODE_NAME"]) else None,
#             df.loc[i]["Sub Category"] if pd.notna(df.loc[i]["Sub Category"]) else None,
#             df.loc[i]["Sub Category 1"] if pd.notna(df.loc[i]["Sub Category 1"]) else None,
#             df.loc[i]["category"] if pd.notna(df.loc[i]["category"]) else None,
#             df.loc[i]["scope"] if pd.notna(df.loc[i]["scope"]) else None,
#             df.loc[i]["Site Type"] if pd.notna(df.loc[i]["Site Type"]) else None,
#             df.loc[i]["Site Type (VI)"] if pd.notna(df.loc[i]["Site Type (VI)"]) else None,
#             df.loc[i]["Site Type-Infra"] if pd.notna(df.loc[i]["Site Type-Infra"]) else None,
#             df.loc[i]["Frequency of PM (Yearly)"] if pd.notna(df.loc[i]["Frequency of PM (Yearly)"]) else None,
#             df.loc[i]["Proposed Frequency"] if pd.notna(df.loc[i]["Proposed Frequency"]) else None,
#             df.loc[i]["Synergy"] if pd.notna(df.loc[i]["Synergy"]) else None,
#             df.loc[i]["KPI"] if pd.notna(df.loc[i]["KPI"]) else None,
#             df.loc[i]["Alarm"] if pd.notna(df.loc[i]["Alarm"]) else None,
#             df.loc[i]["Zone"] if pd.notna(df.loc[i]["Zone"]) else None,
#             df.loc[i]["Subzone"] if pd.notna(df.loc[i]["Subzone"]) else None,
#             df.loc[i]["UWFM Circle Codes"] if pd.notna(df.loc[i]["UWFM Circle Codes"]) else None,
#             df.loc[i]["UWFM Circle Name"] if pd.notna(df.loc[i]["UWFM Circle Name"]) else None,
#             df.loc[i]["UWFM Circle Subzone Name"] if pd.notna(df.loc[i]["UWFM Circle Subzone Name"]) else None,
#             df.loc[i]["Remove VI UWFM CSZ"] if pd.notna(df.loc[i]["Remove VI UWFM CSZ"]) else None,
#             df.loc[i]["Remove ID UWFM CSZ"] if pd.notna(df.loc[i]["Remove ID UWFM CSZ"]) else None,
#             df.loc[i]["User ID"] if pd.notna(df.loc[i]["User ID"]) else None,
#             df.loc[i]["User Name"] if pd.notna(df.loc[i]["User Name"]) else None,
#             df.loc[i]["Full Name"] if pd.notna(df.loc[i]["Full Name"]) else None,
#             df.loc[i]["Email ID"] if pd.notna(df.loc[i]["Email ID"]) else None,
#         )
#         data_to_insert.append(data)
#     print("Data prepared for insertion.")

#     # Execute the bulk insert in chunks
#     chunk_size = 10000  # Adjust this value based on your system capabilities
#     for i in range(0, len(data_to_insert), chunk_size):
#         chunk = data_to_insert[i:i + chunk_size]
#         #execute_values(cursor, insert_query, chunk)

#     #connection.commit()
#     print("Data inserted successfully.")

# except Exception as e:
#     exc_type, exc_obj, exc_tb = sys.exc_info()
#     line_no = exc_tb.tb_lineno
#     filename = exc_tb.tb_frame.f_code.co_filename
#     err_msg = f"Exception occurred at line {line_no} in file {filename}: {e}"
#     print(err_msg)
# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Connection closed.")


#  master data mobility  

# # Define the table creation query
# create_table_query = """
# CREATE TABLE mobility_data (
#     circle_code VARCHAR(50),
#     nssid VARCHAR(50),
#     site_name VARCHAR(255),
#     vendor_name VARCHAR(255),
#     latlong VARCHAR(100),
#     domain VARCHAR(100),
#     node_name VARCHAR(255),
#     sub_category VARCHAR(100),
#     sub_category_1 VARCHAR(100),
#     category VARCHAR(50),
#     scope VARCHAR(50),
#     site_type VARCHAR(255),
#     site_type_vi VARCHAR(255),
#     site_type_infra VARCHAR(255),
#     frequency_of_pm_yearly VARCHAR(50),
#     proposed_frequency VARCHAR(50),
#     synergy VARCHAR(50)
# );
# """

# # Define the table existence check query
# check_table_query = """
# SELECT EXISTS (
#     SELECT FROM information_schema.tables
#     WHERE table_name = 'mobility_data'
# );
# """

# # Define the table truncate query
# truncate_table_query = "TRUNCATE TABLE mobility_data;"

# try:
#     connection = psycopg2.connect(
#         host="10.19.71.176",
#         database="alarms",
#         user="psqladm",
#         password="R%e6DgyQ"
#     )
#     cursor = connection.cursor()
#     print("Connected to database")

#     # Check if the table exists
#     cursor.execute(check_table_query)
#     table_exists = cursor.fetchone()[0]

#     if not table_exists:
#         # Create the table if it doesn't exist
#         cursor.execute(create_table_query)
#         connection.commit()
#         print("Table 'mobility_data' created.")
#     else:
#         # Truncate the table if it exists
#         cursor.execute(truncate_table_query)
#         connection.commit()
#         print("Table 'mobility_data' truncated.")

#     insert_query = """
#         INSERT INTO mobility_data (
#             circle_code, nssid, site_name, vendor_name,
#             latlong, domain, node_name,
#             sub_category, sub_category_1, category, 
#             scope, site_type, site_type_vi, site_type_infra,
#             frequency_of_pm_yearly, proposed_frequency, synergy
#         ) VALUES %s;
#     """
#     # Load the data from Excel
#     df = pd.read_excel('master_file_site_type_cat_updated.xlsx', sheet_name='master_file_mobility')
#     df=df.head(200)
#     print("execl file read complete")
#     df = df.reset_index(drop=True)
#     # Prepare data for bulk insertion
#     data_to_insert = []
#     for i in range(len(df)):
#         data = (
#             df.loc[i]["CIRCLE_CODE"] if pd.notna(df.loc[i]["CIRCLE_CODE"]) else None,
#             df.loc[i]["NSSID"] if pd.notna(df.loc[i]["NSSID"]) else None,
#             df.loc[i]["SITE_NAME"] if pd.notna(df.loc[i]["SITE_NAME"]) else None,
#             df.loc[i]["VENDOR_NAME"] if pd.notna(df.loc[i]["VENDOR_NAME"]) else None,
#             df.loc[i]["LATLONG"] if pd.notna(df.loc[i]["LATLONG"]) else None,
#             df.loc[i]["DOMAIN"] if pd.notna(df.loc[i]["DOMAIN"]) else None,
#             df.loc[i]["NODE_NAME"] if pd.notna(df.loc[i]["NODE_NAME"]) else None,
#             df.loc[i]["Sub Category"] if pd.notna(df.loc[i]["Sub Category"]) else None,
#             df.loc[i]["Sub Category 1"] if pd.notna(df.loc[i]["Sub Category 1"]) else None,
#             df.loc[i]["category"] if pd.notna(df.loc[i]["category"]) else None,
#             df.loc[i]["scope"] if pd.notna(df.loc[i]["scope"]) else None,
#             df.loc[i]["Site Type"] if pd.notna(df.loc[i]["Site Type"]) else None,
#             df.loc[i]["Site Type (VI)"] if pd.notna(df.loc[i]["Site Type (VI)"]) else None,
#             df.loc[i]["Site Type-Infra"] if pd.notna(df.loc[i]["Site Type-Infra"]) else None,
#             df.loc[i]["Frequency of PM (Yearly)"] if pd.notna(df.loc[i]["Frequency of PM (Yearly)"]) else None,
#             df.loc[i]["Proposed Frequency"] if pd.notna(df.loc[i]["Proposed Frequency"]) else None,
#             df.loc[i]["Synergy"] if pd.notna(df.loc[i]["Synergy"]) else None,
#             #df.loc[i]["Alarm"] if pd.notna(df.loc[i]["Alarm"]) else None,
#         )   
#         #print("first iteration completed",data)
#         data_to_insert.append(data)
#     print("for loop completed ",data_to_insert)
#     # Execute the bulk insert in chunks
#     chunk_size = 10000  # Adjust this value based on your system capabilities
#     for i in range(0, len(data_to_insert), chunk_size):
#         chunk = data_to_insert[i:i + chunk_size]
#         execute_values(cursor, insert_query, chunk)

#     connection.commit()
#     print("Data inserted successfully in site type data")

# except Exception as e:
#     exc_type, exc_obj, exc_tb = sys.exc_info()
#     line_no = exc_tb.tb_lineno
#     filename = exc_tb.tb_frame.f_code.co_filename
#     err_msg = f"Exception occurred at Function -> check line no. {line_no} in file {filename}: {e}"
#     print(err_msg)
# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Connection closed")

# #########################################################
# #  cxx data 

# create_table_query ="""
# CREATE TABLE cxx_data_new (
#     circle VARCHAR(100),
#     vendor VARCHAR(100),
#     technology VARCHAR(100),
#     node_name VARCHAR(255),
#     nss_id VARCHAR(100),
#     rsite_name VARCHAR(255),
#     node_id VARCHAR(100),
#     ip_id VARCHAR(100),
#     site_type VARCHAR(100),
#     boo_vendor VARCHAR(100),
#     zone VARCHAR(100),
#     sub_zone VARCHAR(100)
# );
# """

# # Define the table existence check query
# check_table_query = """
# SELECT EXISTS (
#     SELECT FROM information_schema.tables
#     WHERE table_name = 'cxx_data_new'
# );
# """

# # Define the table truncate query
# truncate_table_query = "TRUNCATE TABLE cxx_data_new;"

# try:
#     connection = psycopg2.connect(
#         host="10.19.71.176",
#         database="alarms",
#         user="psqladm",
#         password="R%e6DgyQ"
#     )
#     cursor = connection.cursor()
#     print("Connected to database")

    
#     # Check if the table exists
#     cursor.execute(check_table_query)
#     table_exists = cursor.fetchone()[0]

#     if not table_exists:
#         # Create the table if it doesn't exist
#         cursor.execute(create_table_query)
#         connection.commit()
#         print("Table 'cxx_data_new' created.")
#     else:
#         # Truncate the table if it exists
#         cursor.execute(truncate_table_query)
#         connection.commit()
#         print("Table 'cxx_data_new' truncated.")

#     insert_query = """
#         INSERT INTO cxx_data_new (
#             circle, vendor, technology, node_name, nss_id, 
#             rsite_name, node_id, ip_id, site_type, 
#             boo_vendor, zone, sub_zone
#         ) VALUES %s;
#     """
    
#     # Load the data from Excel
#     df = pd.read_excel('cxx_data_file.xlsx')
#     #df = pd.read_excel('site_type_db_check.xlsx')
#     df=df.head(200)
#     print("Excel file read complete")
    
#     df = df.reset_index(drop=True)

#     # Prepare data for bulk insertion
#     data_to_insert = []
#     for i in range(len(df)):
#         data = (
#             df.loc[i]["CIRCLE"] if pd.notna(df.loc[i]["CIRCLE"]) else None,
#             df.loc[i]["VENDOR"] if pd.notna(df.loc[i]["VENDOR"]) else None,
#             df.loc[i]["TECHNOLOGY"] if pd.notna(df.loc[i]["TECHNOLOGY"]) else None,
#             df.loc[i]["NODE_NAME"] if pd.notna(df.loc[i]["NODE_NAME"]) else None,
#             df.loc[i]["NSS_ID"] if pd.notna(df.loc[i]["NSS_ID"]) else None,
#             df.loc[i]["RSITE_NAME"] if pd.notna(df.loc[i]["RSITE_NAME"]) else None,
#             df.loc[i]["NODE_ID"] if pd.notna(df.loc[i]["NODE_ID"]) else None,
#             df.loc[i]["IP_ID"] if pd.notna(df.loc[i]["IP_ID"]) else None,
#             df.loc[i]["SITE_TYPE"] if pd.notna(df.loc[i]["SITE_TYPE"]) else None,
#             df.loc[i]["BOO_VENDOR"] if pd.notna(df.loc[i]["BOO_VENDOR"]) else None,
#             df.loc[i]["ZONE"] if pd.notna(df.loc[i]["ZONE"]) else None,
#             df.loc[i]["SUB_ZONE"] if pd.notna(df.loc[i]["SUB_ZONE"]) else None,
#         )
#         data_to_insert.append(data)
    
#     print("Data preparation completed")
    
#     # Execute the bulk insert in chunks
#     chunk_size = 10000  # Adjust this value based on your system capabilities
#     for i in range(0, len(data_to_insert), chunk_size):
#         chunk = data_to_insert[i:i + chunk_size]
#         execute_values(cursor, insert_query, chunk)

#     connection.commit()
#     print("Data inserted successfully cxx data")

# except Exception as e:
#     exc_type, exc_obj, exc_tb = sys.exc_info()
#     line_no = exc_tb.tb_lineno
#     filename = exc_tb.tb_frame.f_code.co_filename
#     err_msg = f"Exception occurred at Function -> check line no. {line_no} in file {filename}: {e}"
#     print(err_msg)
# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Connection closed")



######## uwfm data ################

create_table_query ="""
CREATE TABLE uwfm (
    USER_ID VARCHAR(50),
    USER_NAME VARCHAR(100),
    FULL_NAME VARCHAR(255),
    EMAIL_ID VARCHAR(255),
    ROLE_NAME VARCHAR(100),
    DOMAIN_NAMES VARCHAR(255),
    CIRCLE_CODE VARCHAR(50),
    ZONE_NAMES VARCHAR(255)
);
"""
check_table_query = """
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_name = 'uwfm'
);
"""

# Define the table truncate query
truncate_table_query = "TRUNCATE TABLE uwfm;"


try:
    #Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host="10.19.71.176",
        database="alarms",
        user="psqladm",
        password="R%e6DgyQ"
    )
    cursor = connection.cursor()
    print("Connected to database")

    # Check if the table exists
    cursor.execute(check_table_query)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        # Create the table if it doesn't exist
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'uwfm data' created.")
    else:
        # Truncate the table if it exists
        cursor.execute(truncate_table_query)
        connection.commit()
        print("Table 'uwfm data' truncated.")

    # SQL Insert Query using the column names from the uwfm_data table
    insert_query = """
        INSERT INTO uwfm (
            USER_ID, USER_NAME, FULL_NAME, EMAIL_ID,
            ROLE_NAME, DOMAIN_NAMES, CIRCLE_CODE, ZONE_NAMES
        ) VALUES %s;
    """
    
    # Load the data from Excel
    df = pd.read_excel(r"c:\Users\hp\Downloads\uwfm_zone_data_12Nov.xlsx", sheet_name='uwfm_zone_data_12nov')
    print("Excel file read complete")
    filtered_df = df[(df['DOMAIN_NAMES'].str.contains('mobility', case=False, na=False)) & (df['ROLE_NAME'].str.lower() == 'manager'.lower())]
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df=filtered_df.head(200)
    
    #Prepare data for bulk insertion
    data_to_insert = []
    for i in range(len(filtered_df)):
        data = (
            filtered_df.loc[i]["USER_ID"] if pd.notna(filtered_df.loc[i]["USER_ID"]) else None,         # USER_ID
            filtered_df.loc[i]["USER_NAME"] if pd.notna(filtered_df.loc[i]["USER_NAME"]) else None,     # USER_NAME
            filtered_df.loc[i]["FULL_NAME"] if pd.notna(filtered_df.loc[i]["FULL_NAME"]) else None,     # FULL_NAME
            filtered_df.loc[i]["EMAIL_ID"] if pd.notna(filtered_df.loc[i]["EMAIL_ID"]) else None,      # EMAIL_ID
            filtered_df.loc[i]["ROLE_NAME"] if pd.notna(filtered_df.loc[i]["ROLE_NAME"]) else None,     # ROLE_NAME
            filtered_df.loc[i]["DOMAIN_NAMES"] if pd.notna(filtered_df.loc[i]["DOMAIN_NAMES"]) else None, # DOMAIN_NAMES
            filtered_df.loc[i]["CIRCLE_CODE"] if pd.notna(filtered_df.loc[i]["CIRCLE_CODE"]) else None,  # CIRCLE_CODE
            filtered_df.loc[i]["ZONE_NAMES"] if pd.notna(filtered_df.loc[i]["ZONE_NAMES"]) else None    # ZONE_NAMES
        )
        data_to_insert.append(data)
        
    print("For loop completed")
    # Execute the bulk insert in chunks
    chunk_size = 10000  
    for i in range(0, len(data_to_insert), chunk_size):
        chunk = data_to_insert[i:i + chunk_size]
        execute_values(cursor, insert_query, chunk)

    connection.commit()
    print("Data inserted successfully wdfm")

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    line_no = exc_tb.tb_lineno
    filename = exc_tb.tb_frame.f_code.co_filename
    err_msg = f"Exception occurred at Function -> check line no. {line_no} in file {filename}: {e}"
    print(err_msg)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed")




















#  kpi data 

# from psycopg2.extras import execute_values
# import psycopg2
# import pandas as pd
# import sys
# import numpy
# from psycopg2.extensions import register_adapter, AsIs

# def addapt_numpy_float64(numpy_float64):
#     return AsIs(numpy_float64)

# def addapt_numpy_int64(numpy_int64):
#     return AsIs(numpy_int64)

# register_adapter(numpy.float64, addapt_numpy_float64)
# register_adapter(numpy.int64, addapt_numpy_int64)

# try:
#     connection = psycopg2.connect(
#         host="10.19.71.176",
#         database="alarms",
#         user="psqladm",
#         password="R%e6DgyQ"
#     )
#     cursor = connection.cursor()
#     print("Connected to database")

#     insert_query = """
#         INSERT INTO final_kpi (
#             type, kpi_type, report_name, subsheet_name,
#             condition, circle, standard_name_uim, oem, nssid, remark
#         ) VALUES %s;
#     """
    
#     # Load the data from Excel
#     df = pd.read_excel('final_kpi_data.xlsx', sheet_name='final_kpi_data')
#     print("Excel file read complete")

#     df = df.reset_index(drop=True)

#     # Prepare data for bulk insertion
#     data_to_insert = []
#     for i in range(len(df)):
#         data = (
#             df.loc[i]["type"] if pd.notna(df.loc[i]["type"]) else None,
#             df.loc[i]["kpi_type"] if pd.notna(df.loc[i]["kpi_type"]) else None,
#             df.loc[i]["report_name"] if pd.notna(df.loc[i]["report_name"]) else None,
#             df.loc[i]["subsheet_name"] if pd.notna(df.loc[i]["subsheet_name"]) else None,
#             df.loc[i]["condition"] if pd.notna(df.loc[i]["condition"]) else None,
#             df.loc[i]["circle"] if pd.notna(df.loc[i]["circle"]) else None,
#             df.loc[i]["standard_name_uim"] if pd.notna(df.loc[i]["standard_name_uim"]) else None,
#             df.loc[i]["oem"] if pd.notna(df.loc[i]["oem"]) else None,
#             df.loc[i]["nssid"] if pd.notna(df.loc[i]["nssid"]) else None,
#             df.loc[i]["remark"] if pd.notna(df.loc[i]["remark"]) else None,
#         )
#         data_to_insert.append(data)

    
#     print("Data preparation for insertion completed")

#     # Execute the bulk insert in chunks
#     chunk_size = 10000  # Adjust this value based on your system capabilities
#     for i in range(0, len(data_to_insert), chunk_size):
#         chunk = data_to_insert[i:i + chunk_size]
#         execute_values(cursor, insert_query, chunk)

#     connection.commit()
#     print("Data inserted successfully")

# except Exception as e:
#     exc_type, exc_obj, exc_tb = sys.exc_info()
#     line_no = exc_tb.tb_lineno
#     filename = exc_tb.tb_frame.f_code.co_filename
#     err_msg = f"Exception occurred at Function -> check line no. {line_no} in file {filename}: {e}"
#     print(err_msg)
# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Connection closed")


