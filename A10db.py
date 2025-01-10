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
try:
    connection = psycopg2.connect(
        host="10.19.71.167",
        database="uhc_dev",
        user="postgres",
        password="mM3IRLNUX[JU-E,"
    )
    cursor = connection.cursor()
    print("Connected to database")

    insert_query = """
        INSERT INTO inventory (oem_id, oem_type_id, 
                            circle, location, service, 
                            cvp, host, ip, domain_id,
                            checkpoint_ids,username,password,
                            model_no,nss_id,login_server
                            )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    # Execute queries here
    
    df = pd.read_excel('hp_volte.xlsx', sheet_name = 'Sheet1')
    # df = df[df['NE Type'] == 'Database Server']
    df = df[(df['SUBDOMAIN'] == 'IPCPE') & (df['NETWORK'] == 'VOLTE') & (df['VENDOR'] == 'HP')]
    df =df.reset_index(drop = True)
    #print("data frame",df)
    for i in range(len(df)):
        data = (23,220,
                df.loc[i]["CIRCLE"],df.loc[i]["LOCATION"],"IP_Core",
                df.loc[i]["UpdatedHostname"],df.loc[i]["UpdatedHostname"],df.loc[i]["IPADDRESS"],11,
                "{187}",df.loc[i]["NODEUSER"].strip(),df.loc[i]["NODEPWD"].strip(),
                df.loc[i]["MODELNO"],df.loc[i]["NSSID"],df.loc[i]["LOGINSERVER"]
                )
        print(i,data)
        #cursor.execute(insert_query, data)
        #connection.commit()

    print("Data inserted successfully")
    
    # connection.close()
    print("Connection closed")
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    line_no = exc_tb.tb_lineno
    filename = exc_tb.tb_frame.f_code.co_filename
    err_msg = f"Exception occurred at Function -> check line no. {line_no} in file {filename}: {e}"
    print(err_msg)












