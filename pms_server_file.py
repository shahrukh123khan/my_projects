# # working on server 
# # Base URL of the folders
# base_url = 'https://10.241.44.184:9501/enterprise-reports/'

# # Mapping of folders to their respective files
# files_to_download = {
#     'L2MPLS': [
#         'L2MPLS_LMCKTDetail.csv',
#         'L2MPLS_MasterDetail.csv',
#         'L2MPLS_SVCSiteDetail.csv'
#     ],
#     'L3MPLS': [
#         'L3MPLS_LMCKTDetails.csv',
#         'L3MPLS_MasterDetail.csv',
#         'L3MPLS_SVCSiteDetail.csv'
#     ],
#     'NPLC': [
#         'NPLC_LMCKTDetail.csv',
#         'NPLC_MasterDetail.csv',
#         'NPLC_SVCSiteDetail.csv'
#     ],
#     'IPLC': [
#         'IPLC_LMCKTDetail.csv',
#         'IPLC_MasterDetail.csv',
#         'IPLC_SVCSiteDetail.csv'
#     ],
#     'GIPT': [
#         'GIPT_LMCKTDetail.csv',
#         'GIPT_MasterDetail.csv',
#         'GIPT_SVCSiteDetail.csv'
#     ],
#     'INTERNET': [
#         'INTERNET_LMCKTDetail.csv',
#         'INTERNET_MasterDetail.csv',
#         'INTERNET_SVCSiteDetails.csv'
#     ],
#     'SIPT': [
#         'SIPT_LMCKTDetail.csv',
#         'SIPT_MasterDetail.csv',
#         'SIPT_SVCSiteDetail.csv'
#     ],
#     'PRI': [
#         'PRI_LMCKTDetail.csv',
#         'PRI_MasterDetail.csv',
#         'PRI_SVCSiteDetail.csv'
#     ],
# }


# # Check connectivity to the base URL
# try:

#     session = requests.Session()
#     response = session.get(base_url, verify=False)  # Set verify=True if you have a valid SSL certificate
#     if response.status_code != 200:
#         print(f"Failed to connect to the base URL: Status code {response.status_code}")
#         exit()

#     print("Successfully accessed the base URL.")
#  # Create a main directory to save the downloaded files
#     main_save_directory = '/home/FMLVL2/pms/pms_files_downloads'
#     os.makedirs(main_save_directory, exist_ok=True)

#     # Loop through each folder and download the corresponding files
#     for folder, files in files_to_download.items():
#         # Create a directory for each folder
#         folder_path = os.path.join(main_save_directory, folder)
#         os.makedirs(folder_path, exist_ok=True)

#         for file_name in files:
#             # Construct the file URL
#             file_url = f"{base_url}{folder}/{file_name}"

#             # Attempt to download the file
#             file_response = session.get(file_url, verify=False)
#             if file_response.status_code == 200:
#                 with open(os.path.join(folder_path, file_name), 'wb') as f:
#                     f.write(file_response.content)
#                 print(f"Downloaded {file_name} from {file_url}")
#             else:
#                 print(f"Failed to download {file_name} from {file_url} - Status code: {file_response.status_code}")

# except requests.exceptions.RequestException as e:
#     print(f"Error connecting to the base URL: {e}")

                                                                            
                                                                                                     

# import requests
# import os
# import datetime
# import pandas as pd
# # Base URL of the folders
# base_url = 'https://10.241.44.184:9501/enterprise-reports/' 

# # Mapping of folders to their respective files
# files_to_download = {
#     'L2MPLS': [
#         'L2MPLS_LMCKTDetail.csv',
#         'L2MPLS_MasterDetail.csv',
#         'L2MPLS_SVCSiteDetail.csv'
#     ],
#     'L3MPLS': [
#         'L3MPLS_LMCKTDetails.csv',
#         'L3MPLS_MasterDetail.csv',
#         'L3MPLS_SVCSiteDetail.csv'
#     ],
#     'NPLC': [
#         'NPLC_LMCKTDetail.csv',
#         'NPLC_MasterDetail.csv',
#         'NPLC_SVCSiteDetail.csv'
#     ],
#     'IPLC': [
#         'IPLC_LMCKTDetail.csv',
#         'IPLC_MasterDetail.csv',
#         'IPLC_SVCSiteDetail.csv'
#     ],
#     'GIPT': [
#         'GIPT_LMCKTDetail.csv',
#         'GIPT_MasterDetail.csv',
#         'GIPT_SVCSiteDetail.csv'
#     ],
#     'INTERNET': [
#         'INTERNET_LMCKTDetail.csv',
#         'INTERNET_MasterDetail.csv',
#         'INTERNET_SVCSiteDetails.csv'
#     ],
#     'SIPT': [
#         'SIPT_LMCKTDetail.csv',
#         'SIPT_MasterDetail.csv',
#         'SIPT_SVCSiteDetail.csv'
#     ],
#     'PRI': [
#         'PRI_LMCKTDetail.csv',
#         'PRI_MasterDetail.csv',
#         'PRI_SVCSiteDetail.csv'
#     ],
# }


# # Check connectivity to the base URL
# try:
   
#     session = requests.Session()
#     response = session.get(base_url, verify=False)  # Set verify=True if you have a valid SSL certificate
#     if response.status_code != 200:
#         print(f"Failed to connect to the base URL: Status code {response.status_code}")
#         exit()
    
#     print("Successfully accessed the base URL.")
    
#     # Create a main directory to save the downloaded files
#     main_save_directory = '/home/FMLVL2/pms/pms_files_downloads'
#     os.makedirs(main_save_directory, exist_ok=True)

#     # Loop through each folder and download the corresponding files
#     for folder, files in files_to_download.items():
#         # Create a directory for each folder
#         folder_path = os.path.join(main_save_directory, folder)
#         os.makedirs(folder_path, exist_ok=True)

#         for file_name in files:
#             # Construct the file URL
#             file_url = f"{base_url}{folder}/{file_name}"  
            
#             # Attempt to download the file
#             file_response = session.get(file_url, verify=False)
#             if file_response.status_code == 200:
#                 csv_file_path = os.path.join(folder_path, file_name)
#                 with open(csv_file_path, 'wb') as f:
#                     f.write(file_response.content)
                
#                 # with open(os.path.join(folder_path, file_name), 'wb') as f:
#                 #     f.write(file_response.content)
#                 print(f"Downloaded {file_name} from {file_url}")
#                 # After constructing the excel_file_name
#                 timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#                 excel_file_name = f"{os.path.splitext(file_name)[0]}_{timestamp}.xlsx"  # Add timestamp

#                 excel_file_name = f"{os.path.splitext(file_name)[0]}.xlsx"  # Change extension to .xlsx
#                 excel_file_path = os.path.join(folder_path, excel_file_name)

#                 #Read the CSV file and write to Excel
#                 df = pd.read_csv(csv_file_path)
#                 df.to_excel(excel_file_path, index=False)
                
#                 print(f"Converted {file_name} to {excel_file_name}")

#                 # Optionally, remove the CSV file after conversion
#                 os.remove(csv_file_path)

                
#             else:
#                 print(f"Failed to download {file_name} from {file_url} - Status code: {file_response.status_code}")

# except requests.exceptions.RequestException as e:
#     print(f"Error connecting to the base URL: {e}")

# working on server with conversion of csv to excel
# extra filse path /home/FMLVL2/pms/extra_files/SA Repeat Data_June'24.xlsx 
# /home/FMLVL2/pms/extra_files/Top 50 Inventory 25th April 2024.xlsx
# import requests
# import os
# import datetime
# import pandas as pd

# # Base URL of the folders
# base_url = 'https://10.241.44.184:9501/enterprise-reports/' 

# # Mapping of folders to their respective files
# files_to_download = {
#     # 'L2MPLS': [
#     #     'L2MPLS_LMCKTDetail.csv',
#     #     'L2MPLS_MasterDetail.csv',
#     #     'L2MPLS_SVCSiteDetail.csv'
#     # ],
#     # 'L3MPLS': [
#     #     'L3MPLS_LMCKTDetails.csv',
#     #     'L3MPLS_MasterDetail.csv',
#     #     'L3MPLS_SVCSiteDetail.csv'
#     # ],
#     # 'NPLC': [
#     #     'NPLC_LMCKTDetail.csv',
#     #     'NPLC_MasterDetail.csv',
#     #     'NPLC_SVCSiteDetail.csv'
#     # ],
#     # 'IPLC': [
#     #     'IPLC_LMCKTDetail.csv',
#     #     'IPLC_MasterDetail.csv',
#     #     'IPLC_SVCSiteDetail.csv'
#     # ],
#     # 'GIPT': [
#     #     'GIPT_LMCKTDetail.csv',
#     #     'GIPT_MasterDetail.csv',
#     #     'GIPT_SVCSiteDetail.csv'
#     # ],
#     # 'INTERNET': [
#     #     'INTERNET_LMCKTDetail.csv',
#     #     'INTERNET_MasterDetail.csv',
#     #     'INTERNET_SVCSiteDetails.csv'
#     # ],
#     'SIPT': [
#         'SIPT_LMCKTDetail.csv',
#         'SIPT_MasterDetail.csv',
#         'SIPT_SVCSiteDetail.csv'
#     ],
#     'PRI': [
#         'PRI_LMCKTDetail.csv',
#         'PRI_MasterDetail.csv',
#         'PRI_SVCSiteDetail.csv'
#     ],
# }

# # Check connectivity to the base URL
# try:
#     session = requests.Session()
#     response = session.get(base_url, verify=False)  
#     if response.status_code != 200:
#         print(f"Failed to connect to the base URL: Status code {response.status_code}")
#         exit()
    
#     print("Successfully accessed the base URL.")
    
#     # Create a main directory to save the downloaded files
#     main_save_directory = '/home/FMLVL2/pms/pms_files_downloads'
#     os.makedirs(main_save_directory, exist_ok=True)

#     # Loop through each folder and download the corresponding files
#     for folder, files in files_to_download.items():
#         # Create a directory for each folder
#         folder_path = os.path.join(main_save_directory, folder)
#         os.makedirs(folder_path, exist_ok=True)

#         for file_name in files:
#             # Construct the file URL
#             file_url = f"{base_url}{folder}/{file_name}"  
            
#             # Attempt to download the file
#             file_response = session.get(file_url, verify=False)
#             if file_response.status_code == 200:
#                 csv_file_path = os.path.join(folder_path, file_name)
#                 with open(csv_file_path, 'wb') as f:
#                     f.write(file_response.content)
                
#                 print(f"Downloaded {file_name} from {file_url}")
                
#                 # Generate a timestamp and create the Excel file name
#                 timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#                 excel_file_name = f"{os.path.splitext(file_name)[0]}_{timestamp}.xlsx"  # Add timestamp
#                 excel_file_path = os.path.join(folder_path, excel_file_name)

#                 # Read the CSV file and write to Excel
#                 df = pd.read_csv(csv_file_path)
#                 df.to_excel(excel_file_path, index=False)
                
#                 print(f"Converted {file_name} to {excel_file_name}")

#                 # Optionally, remove the CSV file after conversion
#                 os.remove(csv_file_path)

#             else:
#                 print(f"Failed to download {file_name} from {file_url} - Status code: {file_response.status_code}")

# except requests.exceptions.RequestException as e:
#     print(f"Error connecting to the base URL: {e}")

import requests
import os
import datetime
import pandas as pd
import numpy as np

# Base URL of the folders
base_url = 'https://10.241.44.184:9501/enterprise-reports/'

# Mapping of folders to their respective files
files_to_download = {
    'L2MPLS': [
        'L2MPLS_LMCKTDetail.csv',
        'L2MPLS_MasterDetail.csv',
        'L2MPLS_SVCSiteDetail.csv'
    ],
    'L3MPLS': [
        'L3MPLS_LMCKTDetails.csv',
        'L3MPLS_MasterDetail.csv',
        'L3MPLS_SVCSiteDetail.csv'
    ],
    'NPLC': [
        'NPLC_LMCKTDetail.csv',
        'NPLC_MasterDetail.csv',
        'NPLC_SVCSiteDetail.csv'
    ],
    'IPLC': [
        'IPLC_LMCKTDetail.csv',
        'IPLC_MasterDetail.csv',
        'IPLC_SVCSiteDetail.csv'
    ],
    'GIPT': [
        'GIPT_LMCKTDetail.csv',
        'GIPT_MasterDetail.csv',
        'GIPT_SVCSiteDetail.csv'
    ],
    'INTERNET': [
        'INTERNET_LMCKTDetail.csv',
        'INTERNET_MasterDetail.csv',
        'INTERNET_SVCSiteDetails.csv'
    ],
    'SIPT': [
        'SIPT_LMCKTDetail.csv',
        'SIPT_MasterDetail.csv',
        'SIPT_SVCSiteDetail.csv'
    ],
    'PRI': [
        'PRI_LMCKTDetail.csv',
        'PRI_MasterDetail.csv',
        'PRI_SVCSiteDetail.csv'
    ],
}

# Check connectivity to the base URL
try:
    session = requests.Session()
    response = session.get(base_url, verify=False)
    if response.status_code != 200:
        print(f"Failed to connect to the base URL: Status code {response.status_code}")
        exit()
    
    print("Successfully accessed the base URL.")
    
    # Create a main directory to save the downloaded files
    main_save_directory = '/home/FMLVL2/pms/pms_files_downloads'
    os.makedirs(main_save_directory, exist_ok=True)

    # Loop through each folder and download the corresponding files
    for folder, files in files_to_download.items():
        folder_path = os.path.join(main_save_directory, folder)
        os.makedirs(folder_path, exist_ok=True)

        for file_name in files:
            file_url = f"{base_url}{folder}/{file_name}"  
            file_response = session.get(file_url, verify=False)
            if file_response.status_code == 200:
                csv_file_path = os.path.join(folder_path, file_name)
                with open(csv_file_path, 'wb') as f:
                    f.write(file_response.content)
                
                print(f"Downloaded {file_name} from {file_url}")
                
                # Generate a timestamp and create the Excel file name
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                excel_file_name = f"{os.path.splitext(file_name)[0]}_{timestamp}.xlsx"
                excel_file_path = os.path.join(folder_path, excel_file_name)

                # Read the CSV file and write to Excel, skipping bad lines
                df = pd.read_csv(csv_file_path, on_bad_lines='skip')
                df.to_excel(excel_file_path, index=False)
                
                print(f"Converted {file_name} to {excel_file_name}")

                # Optionally, remove the CSV file after conversion
                os.remove(csv_file_path)

            else:
                print(f"Failed to download {file_name} from {file_url} - Status code: {file_response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error connecting to the base URL: {e}")

# Processing the downloaded Excel files to create a master file
all_results = []
output_file = '/home/FMLVL2/pms/PMS_Master_Data_ENT.xlsx'           # Specify the output Excel file name
top_50_inventory = '/home/FMLVL2/pms/extra_files/Top 50 Inventory 25th April 2024.xlsx'
df4 = pd.read_excel(top_50_inventory)
df4 = df4[df4['TOP50'] == 'Gold Cat-1 UBR']
FRA_File='Vodafone_Idea_FRA-July_Aug24.xlsx'
df5 = pd.read_excel(FRA_File)
df5 = df5[df5['Platform'] == 'UBR']

#service_list=['IPLC','PRI','INTERNET','NPLC','P2MPLS','P3MPLS','SIPT','GIPT']
# Loop through services and read the latest Excel files
for folder in files_to_download.keys():
    folder_path = os.path.join(main_save_directory, folder)
    if folder in ['IPLC', 'NPLC']:
        bandwidth = 'SERVICE_PROP_BANDWIDTH'
        bandwidth_unit = 'SERVICE_PROP_BANDWIDTHUOM'
    elif folder == 'PRI':
        bandwidth = 'SERVICE_PROP_ACCESSBANDWIDTH'
        bandwidth_unit = 'SERVICE_PROP_ACCESSBANDWIDTHUOM'
    elif folder == 'INTERNET':
        bandwidth = 'SERVICE_PROP_PORTBANDWIDTH'
        bandwidth_unit = 'SERVICE_PROP_PORTBANDWIDTHUOM'
    # elif folder in ['P2MPLS', 'P3MPLS', 'SIPT', 'GIPT']:
    #     bandwidth = 'PE_BANDWIDTH'
    #     bandwidth_unit = 'PE_BANDWIDTHUOM'
    else:
        bandwidth = 'PE_BANDWIDTH' 
        bandwidth_unit = 'PE_BANDWIDTHUOM'  
    # Get the latest files in the folder
    files = sorted(os.listdir(folder_path), key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    print("files values =",files)
    # Check that we have at least three files to process
    if len(files) < 3:
        print(f"Not enough files in {folder_path} to process for {folder}.")
        continue

    df1 = pd.read_excel(os.path.join(folder_path, files[-3]))  # Latest file for file1
    df2 = pd.read_excel(os.path.join(folder_path, files[-2]))  # Second latest for file2
    df3 = pd.read_excel(os.path.join(folder_path, files[-1]))  # Most recent for file3
    
    unique_circuit_ids = pd.concat([df1, df2, df3, df4])['CIRCUITID'].unique()

    for circuit_id in unique_circuit_ids:
        filtered_df1 = df1[df1['CIRCUITID'] == circuit_id]
        filtered_df2 = df2[df2['CIRCUITID'] == circuit_id]
        filtered_df3 = df3[df3['CIRCUITID'] == circuit_id]
        filtered_df4 = df4[df4['CIRCUITID'] == circuit_id]

        sub_category = filtered_df2['PROPERTIES_LMSERVICEPROVIDER'].values[0] if not filtered_df2.empty else np.nan

        if isinstance(sub_category, str) and 'ubr' in sub_category.lower():
            domain_value = 'ENT_UBR'
        else:
            domain_value = 'ENT'
        
        scope_value = 'Inscope' if domain_value == 'ENT_UBR' else 'Outscope'

        # raw_bandwidth = filtered_df2[bandwidth].values[0] if not filtered_df2.empty else np.nan
        # raw_bandwidth_unit = filtered_df2[bandwidth_unit].values[0] if not filtered_df2.empty else np.nan
        if not filtered_df2.empty:
                raw_bandwidth = filtered_df2[bandwidth].iloc[0]
                raw_bandwidth_unit = filtered_df2[bandwidth_unit].iloc[0]
        else:
            raw_bandwidth = np.nan
            raw_bandwidth_unit = np.nan 

        if raw_bandwidth_unit == 'kbps' and pd.notna(raw_bandwidth):
            bandwidth_value = raw_bandwidth / 1000  # Convert kbps to Mbps
            bandwidth_unit_value = 'Mbps'
        elif raw_bandwidth_unit == 'Gbps' and pd.notna(raw_bandwidth):
            bandwidth_value = raw_bandwidth * 1000  # Convert Gbps to Mbps
            bandwidth_unit_value = 'Mbps'
        else:
            bandwidth_value = raw_bandwidth
            bandwidth_unit_value = raw_bandwidth_unit
        if pd.notna(bandwidth_value) and isinstance(bandwidth_value, (int, float)):
            bandwidth_check = 'Yes' if bandwidth_value > 10 else 'No'
        else:
            bandwidth_check = 'No'  # Handle NaN or non-numeric values  


        combined_data = {
            'CIRCLE_CODE': filtered_df3['SERVICE_ADDRESS_CIRCLENAME'].values[0] if not filtered_df3.empty else np.nan,
            'NSSID': filtered_df1['NSSID'].values[0] if not filtered_df1.empty else np.nan,
            'SITE NAME': 'NA',
            'VENDOR NAME': 'NA',
            'LATITUDE': filtered_df3['SERVICE_ADDRESS_LATITUDE'].values[0] if not filtered_df3.empty else np.nan,
            'LONGITUDE': filtered_df3['SERVICE_ADDRESS_LONGITUDE'].values[0] if not filtered_df3.empty else np.nan,
            'DOMAIN': domain_value,
            'NODE NAME': circuit_id,
            'SUB CATEGORY': filtered_df2['PROPERTIES_LMSERVICEPROVIDER'].values[0] if not filtered_df2.empty else np.nan,
            'SUB CATEGORY 1': 'NA',
            'SCOPE': scope_value,  
            'CATEGORY': folder,
            'BANDWIDTH': bandwidth_value,
            'BANDWIDTH UNIT': bandwidth_unit_value,
            'TOP50':'Yes' if not filtered_df4.empty else 'No' ,   
            'BANDWIDTH_CHECK': bandwidth_check                                                                                                                              #filtered_df4['TOP50'].values[0] if not filtered_df4.empty else np.nan,
        }
        all_results.append(combined_data)

final_df = pd.DataFrame(all_results)

circuit_id_counts = df5['CircuitID'].value_counts()

# Step 2: Identify CircuitIDs that occur more than 2 times
circuit_ids_with_high_count = circuit_id_counts[circuit_id_counts > 2].index

# Step 3: Create a new column in final_df to check if CircuitID is in the above list
final_df['FRA'] = final_df['NODE NAME'].apply(lambda x: 'Yes' if x in circuit_ids_with_high_count else 'No')
final_df['Priority'] = final_df.apply(
    lambda row: 'Critical' if (row['TOP50'] == 'Yes' or 
                                row['BANDWIDTH_CHECK'] == 'Yes' or 
                                row['FRA'] == 'Yes') 
                else 'Regular', axis=1
)
# Optionally, display the result
#print(final_df)

#final_df = final_df.drop_duplicates(subset=['Node_Name'])

final_df.to_excel(output_file, sheet_name='Master_File_ENT', index=False)

print(f"Data has been written to {output_file}.")

# # Add repeat outage and priority
# final_df['REPEAT_OUTAGE'] = np.nan
# final_df['PRIORITY'] = 'No'
# df = pd.read_excel('/home/FMLVL2/pms/extra_files/SA Repeat Data_June24.xlsx', sheet_name='Summary')
# filtered_df = df[(df["Platform"] == "UBR") & (df["Grand Total"] > 2)]

# if 'CIRCUITID' in filtered_df.columns:
#     for circuit_id in filtered_df['CIRCUITID']:
#         if circuit_id in final_df['NODE NAME'].values:
#             final_df.loc[final_df['NODE NAME'] == circuit_id, 'REPEAT_OUTAGE'] = circuit_id
#             final_df.loc[final_df['NODE NAME'] == circuit_id, 'PRIORITY'] = 'Yes'

# if 'CIRCUITID' in df4.columns:
#     for circuit_id in df4['CIRCUITID']:
#         if circuit_id in final_df['NODE NAME'].values:
#             final_df.loc[final_df['NODE NAME'] == circuit_id, 'PRIORITY'] = 'Yes'

# # Save the final master file
# final_df.to_excel('updated_master_file.xlsx', sheet_name='Updated_Master_File', index=False)

# if 'CIRCUITID' in filtered_df.columns:
#     print("Updated master file created successfully with matched Circuit IDs.")
# else:
#     print("The specified column 'CIRCUITID' does not exist in the filtered DataFrame.")
