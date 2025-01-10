

# ############################################
# import pandas as pd
# import psycopg2
# from psycopg2.extras import execute_values

# # Database connection details
# db_host = "10.19.71.176"
# db_name = "pms_db"
# db_user = "psqladm"
# db_password = "R%e6DgyQ"

# # File paths
# input_excel_file = "master_file_site_type_cat_updated.xlsx"
# output_excel_file = "output_with_kpi_data.xlsx"

# # Load NSSIDs from the Excel file
# df = pd.read_excel(input_excel_file)
# print("excel file read completed ")
# # Initialize the KPI column
# df['KPI'] = "No"  # Default value is "No"

# # Connect to the database
# try:
#     with psycopg2.connect(
#         host=db_host,
#         database=db_name,
#         user=db_user,
#         password=db_password
#     ) as connection:
#         with connection.cursor() as cursor:
#             print("Connected to database")
            
#             # Get unique circles from the database and sort them
#             cursor.execute("SELECT DISTINCT standard_name_uim FROM final_kpi ORDER BY standard_name_uim;")
#             circles_in_db = [row[0] for row in cursor.fetchall()]
#             print("cirlces in db ",circles_in_db)
#             # Process each circle
#             for circle in circles_in_db:
#                 # Filter the Excel DataFrame for the current circle
#                 nssids_for_circle = df[df['CIRCLE_CODE'] == circle]['NSSID'].dropna()
#                 print("runing circle is ",circle)
#                 if not nssids_for_circle.empty:
#                     # Prepare the query for matching NSSIDs
#                     print("query make up start")
#                     query = f"SELECT nssid FROM final_kpi WHERE standard_name_uim = %s AND ("
#                     query += ' OR '.join(f"nssid LIKE %s" for _ in nssids_for_circle) + ")"
#                     nssid_patterns = [f"%{nssid}%" for nssid in nssids_for_circle]
#                     print("no error in query")
#                     # Execute the query
#                     cursor.execute(query, (circle, *nssid_patterns))
#                     # result=cursor.fetchone()
#                     # print("result",result)
                    
#                     matched_nssids = {row[0].strip().upper() for row in cursor.fetchall()}
#                     print("Matched NSSIDs for circle", circle, ":",matched_nssids, len(matched_nssids))

#                     # Update the KPI column based on matches
#                     for idx, row in df[df['CIRCLE_CODE'] == circle].iterrows():
#                         if row['NSSID'] in matched_nssids:
#                             print("inside the update logic ")
#                             df.at[idx, 'KPI'] = "Yes"

#             # Save the updated DataFrame to a new Excel file
#             df.to_excel(output_excel_file, index=False)
#             print(f"Results saved to {output_excel_file}")

# except Exception as e:
#     print("An error occurred:", e)


# # for idx, row in df[df['CIRCLE_CODE'] == circle].iterrows():
# #     print(f"Checking NSSID: '{row['NSSID']}'")
# #     for nssid in matched_nssids:
# #         print(f"Comparing with matched NSSID: '{nssid}'")
# #     if row['NSSID'].strip().upper() in matched_nssids:
# #         print("inside the update logic ")
# #         df.at[idx, 'KPI'] = "Yes"

# # # After processing each circle, check for missing circles
# # circles_in_excel = df['circle'].unique()
# # missing_circles = set(circles_in_excel) - set(circles_in_db)

# # if missing_circles:
# #     print("Missing circles in database:", missing_circles)
# # SELECT nssid FROM final_kpi WHERE circle = 'A' AND (nssid LIKE '%IDKA101845%' OR nssid LIKE '%IDKA107966%');

# import pandas as pd
# import psycopg2

# # Database connection details
# db_host = "10.19.71.176"
# db_name = "pms_db"
# db_user = "psqladm"
# db_password = "R%e6DgyQ"

# # File paths
# input_excel_file = "master_file_site_type_cat_updated.xlsx"
# output_excel_file = "output_with_kpi_data.xlsx"

# # Load NSSIDs from the Excel file
# df = pd.read_excel(input_excel_file)
# print("Excel file read completed.")
# # Initialize the KPI column
# df['KPI'] = "No"  # Default value is "No"

# # Connect to the database
# try:
#     with psycopg2.connect(
#         host=db_host,
#         database=db_name,
#         user=db_user,
#         password=db_password
#     ) as connection:
#         with connection.cursor() as cursor:
#             print("Connected to database")
            
#             # Get unique circles from the database and sort them
#             cursor.execute("SELECT DISTINCT standard_name_uim FROM final_kpi ORDER BY standard_name_uim;")
#             circles_in_db = [row[0] for row in cursor.fetchall()]
#             print("Circles in db:", circles_in_db)
            
#             # Process each circle
#             for circle in circles_in_db:
#                 # Filter the Excel DataFrame for the current circle
#                 nssids_for_circle = df[df['CIRCLE_CODE'] == circle]['NSSID'].dropna()
#                 print("Running circle is", circle)

#                 if not nssids_for_circle.empty:
#                     # Check each NSSID individually
#                     for nssid in nssids_for_circle:
#                         # Prepare the query for checking existence of the NSSID
#                         query = f"""
#                             SELECT EXISTS (
#                                 SELECT 1 FROM final_kpi 
#                                 WHERE standard_name_uim = %s AND nssid LIKE %s
#                             );
#                         """
#                         nssid_pattern = f"%{nssid}%"
#                         #print(f"Checking NSSID: {nssid}")

#                         # Execute the query
#                         cursor.execute(query, (circle, nssid_pattern))
#                         exists = cursor.fetchone()[0]  # Fetch the boolean result

#                         # Update the KPI column based on existence
#                         if exists:
#                             #print(f"Updating KPI column to 'Yes' for NSSID: {nssid}")
#                             # Update only the specific record
#                             df.loc[(df['CIRCLE_CODE'] == circle) & (df['NSSID'] == nssid), 'KPI'] = "Yes"
#                 print("completed circle is", circle)

#             print("query in db completed")
#             # Save the updated DataFrame to a new Excel file
#             df.to_excel(output_excel_file, index=False)
#             print(f"Results saved to {output_excel_file}")

# except Exception as e:
#     print("An error occurred:", e)



import pandas as pd
import psycopg2
import re
from psycopg2.extras import execute_values

# Database connection details
db_host = "10.19.71.176"
db_name = "pms_db"
db_user = "psqladm"
db_password = "R%e6DgyQ"

# File paths
input_excel_file = "master_file_site_type_cat_updated.xlsx"
output_excel_file = "output_with_kpi_data.xlsx"

# Load NSSIDs from the Excel file
df = pd.read_excel(input_excel_file)
print("Excel file read completed.")

# Initialize the KPI column
df['KPI'] = "No"  # Default value is "No"

# Define the regex pattern for extracting NSSIDs
nssid_pattern = r"\b([A-Z]+\d+)\b"

# Connect to the database
try:
    with psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    ) as connection:
        with connection.cursor() as cursor:
            print("Connected to database")
            
            # Get unique circles from the database and sort them
            cursor.execute("SELECT DISTINCT standard_name_uim FROM final_kpi ORDER BY standard_name_uim;")
            circles_in_db = [row[0] for row in cursor.fetchall()]
            print("Circles in DB:", circles_in_db)
            
            # Process each circle
            for circle in circles_in_db:
                # Filter the Excel DataFrame for the current circle
                nssids_for_circle = df[df['CIRCLE_CODE'] == circle]['NSSID'].dropna()
                print("Running for circle:", circle)
                
                if not nssids_for_circle.empty:
                    # Prepare the query for matching NSSIDs
                    print("Preparing query...")
                    query = f"SELECT nssid FROM final_kpi WHERE standard_name_uim = %s AND ("
                    query += ' OR '.join(f"nssid LIKE %s" for _ in nssids_for_circle) + ")"
                    nssid_patterns = [f"%{re.search(nssid_pattern, nssid).group(0)}%" for nssid in nssids_for_circle if re.search(nssid_pattern, nssid)]

                    # Execute the query
                    print("Executing query...")
                    cursor.execute(query, (circle, *nssid_patterns))
                    
                    matched_nssids = {row[0].strip().upper() for row in cursor.fetchall()}
                    print("Matched NSSIDs for circle", circle, ":", matched_nssids, len(matched_nssids))

                    # Update the KPI column based on matches
                    for idx, row in df[df['CIRCLE_CODE'] == circle].iterrows():
                        extracted_nssid = re.search(nssid_pattern, row['NSSID'])
                        if extracted_nssid and extracted_nssid.group(0) in matched_nssids:
                            print("Updating KPI for NSSID:", row['NSSID'])
                            df.at[idx, 'KPI'] = "Yes"

            # Save the updated DataFrame to a new Excel file
            df.to_excel(output_excel_file, index=False)
            print(f"Results saved to {output_excel_file}")

except Exception as e:
    print("An error occurred:", e)

