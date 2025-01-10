import pandas as pd
import psycopg2

# Database connection details
db_host = "10.19.71.176"
db_name = "alarms"
db_user = "psqladm"
db_password = "R%e6DgyQ"

# File paths
input_excel_file = r"C:\Users\hp\OneDrive\Documents\master_file_site_type_cat_updated1.xlsx"
output_excel_file = "output_with_alarm_data.xlsx"

# Load NSSIDs from the Excel file
df = pd.read_excel(input_excel_file)
print("Excel file read completed")

# Initialize the alarm column
df['Alarm'] = "No"  # Default value is "No"

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
            cursor.execute("SELECT DISTINCT circle FROM ran_alarms ORDER BY circle;")
            circles_in_db = [row[0] for row in cursor.fetchall()]
            print("Circles in DB:", circles_in_db)

            # Process each circle
            for circle in circles_in_db:
                # Filter the Excel DataFrame for the current circle and the domain 'RAN-BTS'
                filtered_df = df[(df['CIRCLE_CODE'] == circle) & (df['DOMAIN'] == 'RAN-BTS')]
                nssids_for_circle = filtered_df['NSSID'].dropna().astype(str)  # Ensure all NSSIDs are strings
                print("Running circle is", circle)

                if not nssids_for_circle.empty:
                    # Prepare the query for matching NSSIDs
                    print("Query make up start")
                    query = f"SELECT nss_id, days_between FROM ran_alarms WHERE circle = %s AND ("
                    query += ' OR '.join(f"nss_id LIKE %s" for _ in nssids_for_circle) + ")"
                    nssid_patterns = [f"%{nssid}%" for nssid in nssids_for_circle]
                    print("No error in query")

                    # Execute the query
                    cursor.execute(query, (circle, *nssid_patterns))

                    # Fetch the matched NSSIDs and their days_between values
                    matched_records = cursor.fetchall()
                    print("matched records", len(matched_records))
                    matched_nssids = {str(row[0]).strip().upper() for row in matched_records}
                    #print("matched nssid",circle, matched_nssids,len(matched_nssids))
                    days_between_dict = {str(row[0]).strip().upper(): row[1] for row in matched_records}
                    #print("days between dict ", days_between_dict)


                    # Update the alarm column based on the days_between value
                    for idx, row in filtered_df.iterrows():
                        nssid = str(row['NSSID']).strip().upper()  # Ensure NSSID is a string
                        if nssid in matched_nssids:
                            #print("Inside the update logic")
                            # Check the days_between value and update alarm column
                            if days_between_dict[nssid] == "Yes":  # Adjust condition as needed
                                df.at[idx, 'Alarm'] = "Yes"
                if circle == 'GUJ':
                    break
            # Save the updated DataFrame to a new Excel file
            df.to_excel(output_excel_file, index=False)
            print(f"Results saved to {output_excel_file}")

except Exception as e:
    print("An error occurred:", e)


#['APR', 'ASM', 'BIH', 'CHN', 'DEL', 'GUJ', 'HAR', 'HPR', 'JNK', 'KAR', 'KEL', 'KOL', 'MAG', 'MPCG', 'MUM', 'NES', 'ODI', 'PNB', 'RAJ', 'ROB', 'ROTN', 'UPE', 'UPW']




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
#             print("Circles in DB:", circles_in_db)

#             # Process each circle
#             for circle in circles_in_db:
#                 # Filter the Excel DataFrame for the current circle
#                 nssids_for_circle = df[df['CIRCLE_CODE'] == circle]['NSSID'].dropna().unique()
#                 print("Processing circle:", circle)

#                 if len(nssids_for_circle) > 0:
#                     # Prepare patterns for batch query
#                     nssid_patterns = [f"%{nssid}%" for nssid in nssids_for_circle]
#                     query = """
#                         SELECT EXISTS (
#                             SELECT 1 FROM final_kpi 
#                             WHERE standard_name_uim = %s 
#                             AND nssid LIKE ANY(%s)
#                         );
#                     """
#                     # Execute the batch query
#                     cursor.execute(query, (circle, nssid_patterns))
#                     exists = cursor.fetchone()[0]  # True if any match exists
#                     print("exist value ",exists)
#                     if exists:
#                         # Update the KPI column in the DataFrame
#                         df.loc[(df['CIRCLE_CODE'] == circle) & (df['NSSID'].isin(nssids_for_circle)), 'KPI'] = "Yes"
                
#                 print("Completed processing for circle:", circle)

#             # Save the updated DataFrame to a new Excel file
#             df.to_excel(output_excel_file, index=False)
#             print(f"Results saved to {output_excel_file}")

# except Exception as e:
#     print("An error occurred:", e)
import re

# Sample strings with variable NSSID formats
db_strings = [
    "INAS002336_ARON_H_C_I101-INAS002349_ARON_H_C_I101",
    "East-2-rtn-INNE000344_ARON_I_H_R5A1-3-2",
    "AB1234_XYZ_1-23-45",
    "XYZ98765_ARON_H_RTN"
]

# Pattern to capture a prefix of uppercase letters followed by digits, with variable lengths
nssid_pattern = r"\b([A-Z]+\d+)\b"

# Extract NSSID from each string in the list
for db_string in db_strings:
    nssids = re.findall(nssid_pattern, db_string)
    print(f"Extracted NSSIDs from '{db_string}':", nssids)



# UPDATE site_type_data
# SET kpi = 'Yes'
# FROM kpi_data
# WHERE site_type_data.nssid = kpi_data.nssid
#   AND site_type_data.circle_code = kpi_data.circle_code;


# UPDATE site_type_data
# SET kpi = 'Yes'
# FROM kpi_data
# WHERE kpi_data.nssid LIKE '%' || site_type_data.nssid || '%'
#   AND site_type_data.circle_code = kpi_data.circle_code;


######### categoriesing query  ############
# UPDATE site_data
# SET category = 'cat 9'
# WHERE nssid IN (
#     SELECT DISTINCT nssid
#     FROM site_data
#     WHERE domain = 'ran'
# );

####cat 8  having two domain must 
# UPDATE site_data
# SET category = 'cat 8'
# WHERE nssid IN (
#     SELECT nssid
#     FROM site_data
#     WHERE domain IN ('ipcore', 'microwave')
#     GROUP BY nssid
#     HAVING COUNT(DISTINCT domain) = 2
# );

###############
