# task schuduler 
# Linux Cron Job
# Edit Crontab:
# Type crontab -e to edit your cron jobs.
# Add a New Cron Job:
# To run your script weekly, add a line in the following format:
# bash
#############################
# def kbps_to_gb(kbps):
#     # Convert kbps to GB
#     gb = (kbps * 0.000125) / 1024
#     return gb

# def mbps_to_gb(mbps):
#     # Convert mbps to GB
#     gb = (mbps * 0.125) / 1024
#     return gb

# # Example values
# kbps_value = 1000000  # Example kbps value
# mbps_value = 1000     # Example mbps value

# gb_from_kbps = kbps_to_gb(kbps_value)
# gb_from_mbps = mbps_to_gb(mbps_value)

# def kbps_to_gb(kbps):
#     # Convert kbps to GB
#     return (kbps * 0.000125) / 1024

# def mbps_to_gb(mbps):
#     # Convert mbps to GB
#     return (mbps * 0.125) / 1024

# # Example values
# kbps_value = 1000000  # Example kbps value
# mbps_value = 12       # Example mbps value

# # Convert kbps regardless of any conditions
# gb_from_kbps = kbps_to_gb(kbps_value)
# print(f"{kbps_value} kbps is approximately {gb_from_kbps:.6f} GB")

# # Apply condition specifically on mbps_value
# if mbps_value > 10:
#     print("Condition met: Mbps value is greater than 10. Converting to GB.")
#     gb_from_mbps = mbps_to_gb(mbps_value)
#     print(f"{mbps_value} mbps is approximately {gb_from_mbps:.6f} GB")
# else:
#     print("Condition not met: Mbps value is 10 or less. No conversion performed for Mbps.")
##################################
# # kbps to mbps 
# def kbps_to_mbps(kbps):
#     return kbps / 1000

# # Example usage
# kbps_value = 10000
# mbps_value = kbps_to_mbps(kbps_value)
# print(f"{kbps_value} kbps is approximately {mbps_value:.2f} Mbps")
# 0 0 * * 0 /usr/bin/python3 /path/to/your/script.py
# This example runs the script at midnight on Sunday (0 for minutes, 0 for hour, * for every day/month, and 0 for Sunday). You can adjust the day and time as needed.
# Save and Exit:
# Save the changes and exit the editor.

# base url --https://10.241.44.184:9501/enterprise-reports/L2MPLS/
# download file 
# import paramiko

# def download_file_sftp(hostname, username, password, remote_file_path, local_file_path):
#     try:
#         # Create a transport object
#         transport = paramiko.Transport((hostname, 22))
#         transport.connect(username=username, password=password)

#         # Create an SFTP session
#         sftp = paramiko.SFTPClient.from_transport(transport)

#         # Download the file
#         sftp.get(remote_file_path, local_file_path)

#         # Close the SFTP session and transport
#         sftp.close()
#         transport.close()

#         print(f"Downloaded {remote_file_path} to {local_file_path}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Usage
# download_file_sftp('hostname', 'username', 'password', '/remote/path/to/file.txt', 'local/path/to/file.txt')







 









# all services  main code 


import pandas as pd
import numpy as np

# # Define file paths for different services
services = {
    'L2MPLS': {
        'file1': 'L2MPLS_LMCKTDetail_XL.xlsx',
        'file2': 'L2MPLS_MasterDetail_XL.xlsx',
        'file3': 'L2MPLS_SVCSiteDetail_XL.xlsx',
    },
    'L3MPLS': {
        'file1': 'L3MPLS_LMCKTDetails_XL.xlsx',
        'file2': 'L3MPLS_MasterDetail_XL.xlsx',
        'file3': 'L3MPLS_SVCSiteDetail_XL.xlsx',
    },
    'GIPT': {
        'file1': 'GIPT_LMCKTDetail_XL.xlsx',
        'file2': 'GIPT_MasterDetail_XL.xlsx',
        'file3': 'GIPT_SVCSiteDetail_XL.xlsx',
    },
    'INTERNET': {
        'file1': 'INTERNET_LMCKTDetail_XL.xlsx',
        'file2': 'INTERNET_MasterDetail_XL.xlsx',
        'file3': 'INTERNET_SVCSiteDetails_XL.xlsx',
    },
    'IPLC': {
        'file1': 'IPLC_LMCKTDetail_XL.xlsx',
        'file2': 'IPLC_MasterDetail_XL.xlsx',
        'file3': 'IPLC_SVCSiteDetail_XL.xlsx',
    },
    'NPLC': {
        'file1': 'NPLC_LMCKTDetail_XL.xlsx',
        'file2': 'NPLC_MasterDetail_XL.xlsx',
        'file3': 'NPLC_SVCSiteDetail_XL.xlsx',
    },
    'SIPT': {
        'file1': 'SIPT_LMCKTDetail_XL.xlsx',
        'file2': 'SIPT_MasterDetail_XL.xlsx',
        'file3': 'SIPT_SVCSiteDetail_XL.xlsx',
    },
    'PRI': {
        'file1': 'PRI_LMCKTDetail_XL.xlsx',
        'file2': 'PRI_MasterDetail_XL.xlsx',
        'file3': 'PRI_SVCSiteDetail_XL.xlsx',
    }
    
}

all_results = []
top_50_inventory = 'top_50_inventory.xlsx'
FRA_File='Vodafone_Idea_FRALastThreeMonth.xlsx'
output_file = 'Master_File_Ent_11Nov.xlsx'           


df4 = pd.read_excel(top_50_inventory)
df4 = df4[df4['TOP50'] == 'Gold Cat-1 UBR']
df5 = pd.read_excel(FRA_File)
df5 = df5[df5['Platform'] == 'UBR']

#correct
# circle_code = {
#     'andhra pradesh': 'APR',
#     'assam': 'ASM',
#     'bihar': 'BIH',
#     'chennai': 'CHN',
#     'delhi': 'DEL',
#     'gujrat': 'GUJ',
#     'haryana': 'HAR',
#     'himanchal pradesh': 'HPR',
#     'jammu and kashmir': 'JNK',
#     'karnataka': 'KAR',
#     'kerala': 'KEL',
#     'kolkata': 'KOL',
#     'maharashtra and goa': 'MAG',
#     'madhya pradesh and chattisgarh': 'MPC',
#     'mumbai': 'MUM',
#     'north east': 'NES',
#     'orissa': 'ODI',
#     'punjab': 'PJB',
#     'rajasthan': 'RAJ',
#     'rest of bengal': 'ROB',
#     'tamil nadu': 'TNC',
#     'uttar pradesh (east)': 'UPE',
#     'uttar pradesh (west)': 'UPW'
# }
circle_code = {
    'andhra pradesh': 'APR',
    'assam': 'ASM',
    'bihar and jharkhand': 'BIH',
    'chennai': 'CHN',
    'delhi': 'DEL',
    'gujarat': 'GUJ',  
    'haryana': 'HAR',
    'himachal pradesh': 'HPR',  
    'jammu and kashmir': 'JNK',
    'karnataka': 'KAR',
    'kerala': 'KEL',
    'kolkata': 'KOL',
    'madhya pradesh': 'MPC',
    'maharashtra and goa': 'MAG',
    'mumbai': 'MUM',
    'orissa': 'ODI',  
    'punjab': 'PJB',
    'rajasthan': 'RAJ',
    'rest of bengal': 'ROB',
    'tamil nadu': 'TNC',  
    'uttar pradesh (east)': 'UPE',  
    'uttar pradesh (west)': 'UPW'   
}


for service_name, files in services.items():
    # Read the relevant files for the current service
    df1 = pd.read_excel(files['file1'])
    df2 = pd.read_excel(files['file2'])
    df3 = pd.read_excel(files['file3'])

    # df4 = pd.read_excel(top_50_inventory).head(10)
    # df4 = df4[df4['TOP50'] == 'Gold Cat-1 UBR']
    # Perform your filtering and processing similar to the original code
    # Example of filtering and combining logic:
    unique_circuit_ids = pd.concat([df1, df2, df3, df4,df5])['CIRCUITID'].unique()
    print("excel files read completed")
    for circuit_id in unique_circuit_ids:
        # Filter each DataFrame for the current circuit_id
        filtered_df1 = df1[df1['CIRCUITID'] == circuit_id]
        filtered_df2 = df2[df2['CIRCUITID'] == circuit_id]
        filtered_df3 = df3[df3['CIRCUITID'] == circuit_id]
        filtered_df4 = df4[df4['CIRCUITID'] == circuit_id]

        sub_category = filtered_df2['PROPERTIES_LMSERVICEPROVIDER'].values[0] if not filtered_df2.empty else np.nan
        if service_name in ['IPLC', 'NPLC']:
            bandwidth = 'SERVICE_PROP_BANDWIDTH'
            bandwidth_unit = 'SERVICE_PROP_BANDWIDTHUOM'
        elif service_name == 'PRI':
            bandwidth = 'SERVICE_PROP_ACCESSBANDWIDTH'
            bandwidth_unit = 'SERVICE_PROP_ACCESSBANDWIDTHUOM'
        elif service_name == 'INTERNET':
            bandwidth = 'SERVICE_PROP_PORTBANDWIDTH'
            bandwidth_unit = 'SERVICE_PROP_PORTBANDWIDTHUOM'
    # elif folder in ['P2MPLS', 'P3MPLS', 'SIPT', 'GIPT']:
    #     bandwidth = 'PE_BANDWIDTH'
    #     bandwidth_unit = 'PE_BANDWIDTHUOM'
        else:
            bandwidth = 'PE_BANDWIDTH' 
            bandwidth_unit = 'PE_BANDWIDTHUOM'  
            # Determine Domain based on Sub Category
        if isinstance(sub_category, str) and 'ubr' in sub_category.lower():
            domain_value = 'ENT_UBR'
        else:
            domain_value = 'ENT'
        
        scope_value = 'Inscope' if domain_value == 'ENT_UBR' else 'Outscope'
        if not filtered_df2.empty:
                raw_bandwidth = pd.to_numeric(filtered_df2[bandwidth].iloc[0], errors='coerce')
                #raw_bandwidth = filtered_df2[bandwidth].iloc[0]
                raw_bandwidth_unit = filtered_df2[bandwidth_unit].iloc[0]
        
        else:
            raw_bandwidth = np.nan
            raw_bandwidth_unit = np.nan 
        # Convert to Mbps based on the unit
        if str(raw_bandwidth_unit).lower() == 'kbps' and pd.notna(raw_bandwidth):
            bandwidth_value = raw_bandwidth / 1000  # Convert kbps to Mbps
            bandwidth_unit_value = 'mbps'
        elif str(raw_bandwidth_unit).lower() == 'gbps' and pd.notna(raw_bandwidth):
            bandwidth_value = raw_bandwidth * 1000  # Convert Gbps to Mbps
            bandwidth_unit_value = 'mbps'
        else:
            bandwidth_value = raw_bandwidth
            bandwidth_unit_value = raw_bandwidth_unit
        if pd.notna(bandwidth_value) and isinstance(bandwidth_value, (int, float)):
            bandwidth_check = 'Yes' if bandwidth_value > 10 else 'No'
        else:
            bandwidth_check = 'No'  # Handle NaN or non-numeric values
        
        
        service_address_circle_name = filtered_df3['SERVICE_ADDRESS_CIRCLENAME'].values[0] if not filtered_df3.empty else np.nan
        
        # Normalize circle name for mapping
        if isinstance(service_address_circle_name, str):
            service_address_circle_name = service_address_circle_name.strip().lower()
            #print(f"Processing circle name: {service_address_circle_name}")  # Debug print
        else:
            service_address_circle_name = np.nan

        # Map using the normalized circle name
        circle_code_mapped = circle_code.get(service_address_circle_name, np.nan)
        #print(f"Mapped circle code: {circle_code_mapped}")  # Debug print
        top50_value_check = 'Yes' if not filtered_df4.empty and filtered_df4['TOP50'].notna().any() else 'No'
        #circle_code_mapped,
        combined_data = {
        'CIRCLE_CODE':circle_code_mapped,     #filtered_df3['SERVICE_ADDRESS_CIRCLENAME'].values[0] if not filtered_df3.empty else np.nan,
        'NSSID': filtered_df1['NSSID'].values[0] if not filtered_df1.empty else np.nan,
        'SITE NAME':'NA',
        'VENDOR NAME':'NA',
        'LATITUDE': filtered_df3['SERVICE_ADDRESS_LATITUDE'].values[0] if not filtered_df3.empty else np.nan,
        'LONGITUDE': filtered_df3['SERVICE_ADDRESS_LONGITUDE'].values[0] if not filtered_df3.empty else np.nan,
        'DOMAIN': domain_value,
        'NODE NAME': circuit_id,
        'SUB CATEGORY': filtered_df2['PROPERTIES_LMSERVICEPROVIDER'].values[0] if not filtered_df2.empty else np.nan,
        'SUB CATEGORY 1':'NA',
        'SCOPE': scope_value,  
        'CATEGORY':service_name,
        # 'BANDWIDTH': filtered_df2['SERVICE_PROP_PORTBANDWIDTH'].values[0] if not filtered_df2.empty else np.nan,
        # 'BANDWIDTH UNIT': filtered_df2['SERVICE_PROP_PORTBANDWIDTHUOM'].values[0] if not filtered_df2.empty else np.nan, 
        'BANDWIDTH': bandwidth_value,
        'BANDWIDTH UNIT': bandwidth_unit_value,
        'TOP50':top50_value_check,        #'Yes' if not filtered_df4.empty else 'No' ,
        # 'TOP50': 'Yes' if not filtered_df4.empty and filtered_df4['TOP50'].iloc[0] == 'Yes' else 'No',  # Correct check                                   #filtered_df4['TOP50'].values[0] if not filtered_df4.empty else np.nan,
        'BANDWIDTH_CHECK': bandwidth_check
        #'TOP50': filtered_df4['TOP50'].values[0] if not filtered_df4.empty else np.nan,
        #'Priority':df5[df5['CIRCUITID']].values[0] if not filtered_df5.empty else np.nan,

    }
        all_results.append(combined_data)
print("data creation completed")
final_df = pd.DataFrame(all_results)

circuit_id_counts = df5['CircuitID'].value_counts()

# Step 2: Identify CircuitIDs that occur more than 2 times
circuit_ids_with_high_count = circuit_id_counts[circuit_id_counts > 2].index

#Step 3: Create a new column in final_df to check if CircuitID is in the above list
final_df['FRA'] = final_df['NODE NAME'].apply(lambda x: 'Yes' if x in circuit_ids_with_high_count else 'No')
# final_df['Priority'] = final_df.apply(
#      lambda row: 'critical_1' if row['FRA'] == 'Yes' else                 #and row['BANDWIDTH_CHECK'] != 'Yes' and row['TOP50'] != 'Yes' else
#                 #'critical_2' if row['TOP50'] == 'Yes' else
#                 'critical_2' if row['TOP50'] == 'Yes' else                #and row['FRA'] != 'Yes' and row['BANDWIDTH_CHECK'] != 'Yes' else
#                 #'critical_3' if row['BANDWIDTH_CHECK'] == 'Yes' else
#                 'critical_3' if row['BANDWIDTH_CHECK'] == 'Yes' else          #and row['FRA'] != 'Yes' and row['TOP50'] != 'Yes' else
#                 'Regular', 
#     axis=1
# )
final_df['Priority'] = final_df.apply(
    lambda row: 'critical_1' if row['FRA'] == 'Yes' and row['TOP50'] == 'No' and row['BANDWIDTH_CHECK'] == 'No' else
                 'critical_2' if row['FRA'] == 'No' and row['TOP50'] == 'Yes' and row['BANDWIDTH_CHECK'] == 'No' else
                 'critical_3' if row['FRA'] == 'No' and row['TOP50'] == 'No' and row['BANDWIDTH_CHECK'] == 'Yes' else
                 'Regular',
    axis=1
)
# Optionally, display the result
#print(final_df)

#final_df = final_df.drop_duplicates(subset=['Node_Name'])
# Define the desired order of columns
desired_column_order = [
    
    'CIRCLE_CODE', 
    'NSSID', 
    'SITE NAME', 
    'VENDOR NAME', 
    'LATITUDE', 
    'LONGITUDE', 
    'DOMAIN', 
    'NODE NAME', 
    'SUB CATEGORY', 
    'SUB CATEGORY 1', 
    'SCOPE', 
    'CATEGORY', 
    'BANDWIDTH', 
    'BANDWIDTH UNIT', 
    'FRA',
    'TOP50', 
    'BANDWIDTH_CHECK', 
    'Priority'
]

# Reorder the DataFrame
final_df = final_df[desired_column_order]
final_df.to_excel(output_file, sheet_name='Master_File_Ent', index=False)

print(f"Data has been written to {output_file}.")

#  lambda row: 'critical_1' if row['FRA'] == 'Yes' else
#                 'critical_2' if row['TOP50'] == 'Yes' and row['FRA'] != 'Yes' else
#                 'critical_3' if row['BANDWIDTH_CHECK'] == 'Yes' and row['FRA'] != 'Yes' and row['TOP50'] != 'Yes' else
#                 'Regular', 
#     axis=1
# )

# final_df['REPEAT_OUTAGE'] = np.nan

# final_df['PRIORITY'] = 'No'
# df = pd.read_excel('SARepeatData_June24.xlsx', sheet_name = 'Summary')
# filtered_df = df[(df["Platform"] == "UBR") & (df["Grand Total"] > 2)]
# #print("circuit id of summary data",df["CIRCUITID"])

# if 'CIRCUITID' in filtered_df.columns:
#     for circuit_id in filtered_df['CIRCUITID']:
#         if circuit_id in final_df['NODE NAME'].values:
#             final_df.loc[final_df['NODE NAME'] == circuit_id, 'REPEAT_OUTAGE'] = circuit_id
#             final_df.loc[final_df['NODE NAME'] == circuit_id, 'PRIORITY'] = 'Yes'

# # # Check for matching Circuit IDs in df4
# # for service_name, files in services.items():
# #     df4 = pd.read_excel(top_50_inventory)
# #     df4 = df4[df4['TOP50'] == 'Gold Cat-1 UBR']  # Adjust based on your filtering logic

# #     if 'CIRCUITID' in df4.columns:
# #         for circuit_id in df4['CIRCUITID']:
# #             if circuit_id in final_df['NODE NAME'].values:
# #                 final_df.loc[final_df['NODE NAME'] == circuit_id, 'PRIORITY'] = 'Yes'

# if 'CIRCUITID' in df4.columns:
#         for circuit_id in df4['CIRCUITID']:
#             if circuit_id in final_df['NODE NAME'].values:
#                 final_df.loc[final_df['NODE NAME'] == circuit_id, 'PRIORITY'] = 'Yes'



# final_df.to_excel('updated_master_file.xlsx', sheet_name='Updated_Master_File', index=False)

# if 'CIRCUITID' in filtered_df.columns:
#     print("Updated master file created successfully with matched Circuit IDs.")
# else:
#     print("The specified column 'CIRCUITID' does not exist in the filtered DataFrame.")   

# import requests
# import os

# # Base URL of the folders
# base_url = 'https://10.241.44.184:9501/enterprise-reports/'

# # Function to list files in a specified folder
# def list_files(folder):
#     folder_url = f"{base_url}{folder}/"
#     response = requests.get(folder_url, verify=False)
#     if response.status_code == 200:
#         # Assuming the response is a list of file names in plain text or HTML
#         # This might need to be adjusted based on the actual response format
#         files = response.text.splitlines()  # Split by line
#         files = [file.lower() for file in files]  # Convert to lowercase
#         print(f"Files in {folder}:")
#         for file in files:
#             print(file)
#         return files
#     else:
#         print(f"Failed to list files in {folder} - Status code: {response.status_code}")
#         return []

# # Function to download a specific file
# def download_file(folder, file_name):
#     file_url = f"{base_url}{folder}/{file_name}"
#     response = requests.get(file_url, verify=False)
#     if response.status_code == 200:
#         save_directory = '/home/FMLVL2/pms/pms_files_downloads'
#         os.makedirs(save_directory, exist_ok=True)
#         file_path = os.path.join(save_directory, file_name)

#         # Save the file
#         with open(file_path, 'wb') as f:
#             f.write(response.content)
        
#         print(f"Downloaded {file_name} from {file_url}")
#     else:
#         print(f"Failed to download {file_name} from {file_url} - Status code: {response.status_code}")

# # Main function to execute the script
# def main():
#     # Specify the folder you want to list files from
#     folder_name = 'L2MPLS'  # Change this to the folder you want to list files from
#     files = list_files(folder_name)

#     # Specify the file you want to download (in lowercase)
#     file_to_download = 'l2mpls_lmcktdetail.csv'  # Change this to the desired file name in lowercase
#     if file_to_download in files:
#         download_file(folder_name, file_to_download)
#     else:
#         print(f"{file_to_download} not found in {folder_name}.")

# if __name__ == "__main__":
#     main()


# import requests
# import os
# import re

# # Base URL of the folders
# base_url = 'https://10.241.44.184:9501/enterprise-reports/'

# # Function to list folders
# def list_folder(base_url):
#     folder_url = f"{base_url}"
#     response = requests.get(folder_url, verify=False)
#     if response.status_code == 200:
#         # Use regex to find all file links in the response text
#         folders = re.findall(r'href="([^"]+)"', response.text)
#         folders = [folder.lower() for folder in folders if folder.endswith('.csv')]  # Filter only .csv files
#         print("Files in the folder:")
#         for name in folders:
#             print(name)
#         return folders
#     else:
#         print(f"Failed to list files in the folder - Status code: {response.status_code}")
#         return []


# def main():
#     folders = list_folder(base_url)
#     # folder_name = 'L2MPLS'  
#     # files = list_files(folder_name)
#     # file_to_download = 'l2mpls_lmcktdetail.csv' 
#     # if file_to_download in files:
#     #     download_file(folder_name, file_to_download)
#     # else:
#     #     print(f"{file_to_download} not found in {folder_name}.")
#     print("folder listed successfully")

# if __name__ == "__main__":
#     main()
