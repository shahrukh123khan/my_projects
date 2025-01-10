import csv
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
    'Internet': [
        'Internet_LMCktDetail.csv',
        'Internet_MasterDetail.csv',
        'Internet_SVCSiteDetails.csv'
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
                
                # Generate a timestamp and create the Excel file name
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_file_name_with_timestamp = f"{os.path.splitext(file_name)[0]}_{timestamp}.csv"
                csv_file_path_with_timestamp = os.path.join(folder_path, csv_file_name_with_timestamp)

                with open(csv_file_path_with_timestamp, 'wb') as f:
                    f.write(file_response.content)
                print(f"Downloaded and saved {csv_file_name_with_timestamp} from {file_url}")     
                
            else:
                print(f"Failed to download {file_name} from {file_url} - Status code: {file_response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error connecting to the base URL: {e}")

# Processing the downloaded Excel files to create a master file
all_results = []
output_file = '/home/FMLVL2/pms/PMS_Master_Data_ENT_server_pms_nov12.xlsx'           # Specify the output Excel file name
top_50_inventory = '/home/FMLVL2/pms/extra_files/Top 50 Inventory 25th April 2024.xlsx'
df4 = pd.read_excel(top_50_inventory)
df4 = df4[df4['TOP50'] == 'Gold Cat-1 UBR']
FRA_File='/home/FMLVL2/pms/extra_files/Vodafone_Idea_FRA Last Three Month.xlsx'
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
    elif folder == 'Internet':
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
    print("folder path ",folder_path)
    # Check that we have at least three files to process
    if len(files) < 3:
        print(f"Not enough files in {folder_path} to process for {folder}.")
        continue

    df1 = pd.read_csv(os.path.join(folder_path, files[-3]),engine='python',quoting=csv.QUOTE_NONE)  # Latest file for file1
    df2 = pd.read_csv(os.path.join(folder_path, files[-2]),engine='python',quoting=csv.QUOTE_NONE)  # Second latest for file2
    df3 = pd.read_csv(os.path.join(folder_path, files[-1]),engine='python',quoting=csv.QUOTE_NONE)  # Most recent for file3
    
    unique_circuit_ids = pd.concat([df1, df2, df3, df4])['CIRCUITID'].unique()

    for circuit_id in unique_circuit_ids:
        filtered_df1 = df1[df1['CIRCUITID'] == circuit_id]
        filtered_df2 = df2[df2['CIRCUITID'] == circuit_id]
        filtered_df3 = df3[df3['CIRCUITID'] == circuit_id]
        filtered_df4 = df4[df4['CIRCUITID'] == circuit_id]

        sub_category = filtered_df2['PROPERTIES_LMSERVICEPROVIDER'].values[0] if not filtered_df2.empty else np.nan
       
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
        'CATEGORY':folder,
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

final_df['Priority'] = final_df.apply(
    lambda row: 'critical_1' if row['FRA'] == 'Yes' and row['TOP50'] == 'No' and row['BANDWIDTH_CHECK'] == 'No' else
                 'critical_2' if row['FRA'] == 'No' and row['TOP50'] == 'Yes' and row['BANDWIDTH_CHECK'] == 'No' else
                 'critical_3' if row['FRA'] == 'No' and row['TOP50'] == 'No' and row['BANDWIDTH_CHECK'] == 'Yes' else
                 'Regular',
    axis=1
)

final_df.to_excel(output_file, sheet_name='Master_File_ENT', index=False)

print(f"Data has been written to {output_file}.")

