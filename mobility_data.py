
# site type master data 
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

# Define the table truncate query

try:
    connection = psycopg2.connect(
        host="10.19.71.176",
        database="alarms",
        user="psqladm",
        password="R%e6DgyQ"
    )
    cursor = connection.cursor()

    # Insert query with all columns
    insert_query = """
        INSERT INTO site_type_data (
            circle_code, nssid, site_name, vendor_name, latlong, domain, 
            node_name, sub_category, sub_category_1, category, scope, 
            site_type, site_type_vi, site_type_infra, frequency_of_pm_yearly, 
            proposed_frequency, synergy, kpi, alarm, zone, subzone, 
            uwfm_circle_codes, uwfm_circle_name, uwfm_circle_subzone_name, 
            remove_vi_uwfm_csz, remove_id_uwfm_csz, user_id, user_name, 
            full_name, email_id
        ) VALUES %s;
    """

    # Load the data from Excel
    df = pd.read_excel('Site_Type_Master_file_data_Nov12.xlsx', sheet_name='Site_Type_Master_file_data_Nov1')
    #df = df.head(10)
    print("Excel file read complete")
    df = df.reset_index(drop=True)

    # Prepare data for bulk insertion
    data_to_insert = []
    for i in range(len(df)):
        data = (
        df.loc[i]["circle_code"] if pd.notna(df.loc[i]["circle_code"]) else None,
        df.loc[i]["nssid"] if pd.notna(df.loc[i]["nssid"]) else None,
        df.loc[i]["site_name"] if pd.notna(df.loc[i]["site_name"]) else None,
        df.loc[i]["vendor_name"] if pd.notna(df.loc[i]["vendor_name"]) else None,
        df.loc[i]["latlong"] if pd.notna(df.loc[i]["latlong"]) else None,
        df.loc[i]["domain"] if pd.notna(df.loc[i]["domain"]) else None,
        df.loc[i]["node_name"] if pd.notna(df.loc[i]["node_name"]) else None,
        df.loc[i]["sub_category"] if pd.notna(df.loc[i]["sub_category"]) else None,
        df.loc[i]["sub_category_1"] if pd.notna(df.loc[i]["sub_category_1"]) else None,
        df.loc[i]["category"] if pd.notna(df.loc[i]["category"]) else None,
        df.loc[i]["scope"] if pd.notna(df.loc[i]["scope"]) else None,
        df.loc[i]["site_type"] if pd.notna(df.loc[i]["site_type"]) else None,
        df.loc[i]["site_type_vi"] if pd.notna(df.loc[i]["site_type_vi"]) else None,
        df.loc[i]["site_type_infra"] if pd.notna(df.loc[i]["site_type_infra"]) else None,
        df.loc[i]["frequency_of_pm_yearly"] if pd.notna(df.loc[i]["frequency_of_pm_yearly"]) else None,
        df.loc[i]["proposed_frequency"] if pd.notna(df.loc[i]["proposed_frequency"]) else None,
        df.loc[i]["synergy"] if pd.notna(df.loc[i]["synergy"]) else None,
        df.loc[i]["kpi"] if pd.notna(df.loc[i]["kpi"]) else None,
        df.loc[i]["alarm"] if pd.notna(df.loc[i]["alarm"]) else None,
        df.loc[i]["zone"] if pd.notna(df.loc[i]["zone"]) else None,
        df.loc[i]["subzone"] if pd.notna(df.loc[i]["subzone"]) else None,
        df.loc[i]["uwfm_circle_codes"] if pd.notna(df.loc[i]["uwfm_circle_codes"]) else None,
        df.loc[i]["uwfm_circle_name"] if pd.notna(df.loc[i]["uwfm_circle_name"]) else None,
        df.loc[i]["uwfm_circle_subzone_name"] if pd.notna(df.loc[i]["uwfm_circle_subzone_name"]) else None,
        df.loc[i]["remove_vi_uwfm_csz"] if pd.notna(df.loc[i]["remove_vi_uwfm_csz"]) else None,
        df.loc[i]["remove_id_uwfm_csz"] if pd.notna(df.loc[i]["remove_id_uwfm_csz"]) else None,
        df.loc[i]["user_id"] if pd.notna(df.loc[i]["user_id"]) else None,
        df.loc[i]["user_name"] if pd.notna(df.loc[i]["user_name"]) else None,
        df.loc[i]["full_name"] if pd.notna(df.loc[i]["full_name"]) else None,
        df.loc[i]["email_id"] if pd.notna(df.loc[i]["email_id"]) else None,
        )
        data_to_insert.append(data)

    print("Data prepared for insertion.")

    # Execute the bulk insert in chunks
    chunk_size = 10000  # Adjust this value based on your system capabilities
    for i in range(0, len(data_to_insert), chunk_size):
        chunk = data_to_insert[i:i + chunk_size]
        execute_values(cursor, insert_query, chunk)

    connection.commit()
    print("Data inserted successfully.")

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    line_no = exc_tb.tb_lineno
    filename = exc_tb.tb_frame.f_code.co_filename
    err_msg = f"Exception occurred at line {line_no} in file {filename}: {e}"
    print(err_msg)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed.")