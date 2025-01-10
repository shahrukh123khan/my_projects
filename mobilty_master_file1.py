import pandas as pd
import time
import os

site_ownership=[
    {
         #[RAN] | [MICROWAVE] | [Access Optical] | [CORE Router] | [BSC | RNC | DWDM]
        "site_type1": ["RAN", "MICROWAVE", "Access Optical", "CORE Router", "BSC", "RNC", "DWDM"],
        "site_type_main1": ["CORE Router"],
        "site_type": ["RAN-BTS", "MICROWAVE", "OPTICS", "IPMPLS-Core", "RAN-BSC", "RNC", "DWDM"],
        "site_type_main": ["IPMPLS-Core",],
        #"site_type_main": [ "MICROWAVE", "OPTICS"],
        #"site_type_main": ["RAN-BTS", "MICROWAVE", "OPTICS", "IPMPLS-Core","RNC",],
        "site_type_vi": "CORE",
        "site_type_infra": "Stategic",
        "frequency": 4,
        "proposed_frequency": 4,
        "synergy": ["RAN FE", "Tx FE", "Infra FE"],
        "priority": 1,
        "category": 9
    },
    {
        "site_type1": ["RAN", "MICROWAVE", "Access Optical", "Aggregation Router", "BSC", "RNC", "DWDM", "DXC", "ROADM"],
        "site_type_main1": ["Aggregation Router", "DWDM", "DXC", "ROADM"],
        "site_type": ["RAN-BTS", "MICROWAVE", "OPTICS", "IPMPLS-Aggregation", "RAN-BSC", "RNC", "DWDM", "DXC", "ROADM"],
        "site_type_main": ["IPMPLS-Aggregation","DWDM-DXC","DWDM-ROADM"],
        #"site_type_main": ["MICROWAVE","OPTICS"],
        #"site_type_main": ["RAN-BTS", "MICROWAVE", "OPTICS", "IPMPLS-Aggregation", "RAN-BSC", "RNC","DWDM-DXC","DWDM-ROADM"],
        "site_type_vi": "Aggregation",
        "site_type_infra": "Stategic",
        "frequency": 4,
        "proposed_frequency": 4,
        "synergy": ["RAN FE", "Tx FE", "Infra FE"],
        "priority": 2,
        "category": 8
    },
    {
        "site_type1": ["RAN", "MICROWAVE", "Access Optical", "Pre-Agg Router", "BSC", "RNC"],
        "site_type_main1": ["BSC", "RNC"],
        "site_type": ["RAN-BTS", "MICROWAVE", "OPTICS", "IPMPLS-Pre-AGG", "RAN-BSC", "RNC"],
        "site_type_main": ["RAN-BSC","RNC"],
        #"site_type_main": ["RAN-BTS", "MICROWAVE", "OPTICS", "IPMPLS-Pre-AGG", "RAN-BSC", "RNC"],
        "site_type_vi": "Aggregation",
        "site_type_infra": "Stategic",
        "frequency": 4,
        "proposed_frequency": 4,
        "synergy": ["RAN FE", "Tx FE", "Infra FE"],
        "priority": 3,
        "category": 7
    },
    {
        "site_type1": ["RAN", "MICROWAVE", "Pre-Agg Router"],
        "site_type_main1": ["Pre-Agg Router"],
        "site_type": ["RAN-BTS", "MICROWAVE", "IPMPLS-Pre-AGG"],
        "site_type_main": ["IPMPLS-Pre-AGG"],
        #"site_type_main": ["MICROWAVE"],
        #"site_type_main": ["RAN-BTS", "MICROWAVE", "IPMPLS-Pre-AGG"],
        "site_type_vi": "PreAgg",
        "site_type_infra": "Tx Hub",
        "frequency": 2,
        "proposed_frequency": 2,
        "synergy": ["RAN FE", "Tx FE", "Infra FE"],
        "priority": 4,
        "category": 6
    },
    # {
    #     "site_type": ["PTN", "Access Router"],
    #     "site_type_main": [],
    #     "site_type_vi": "Access POP",
    #     "site_type_infra": "Tx Hub",
    #     "frequency": 2,
    #     "proposed_frequency": 4,
    #     "synergy": ["Tx FE"],
    #     "priority": 5,
    #     "category": 5
    # },
    {
        "site_type1": ["RAN", "MICROWAVE", "Access Optical", "OLA", "Access Router"],
        "site_type_main1": ["Access Optical", "Access Router"],
        "site_type": ["RAN-BTS", "MICROWAVE", "OPTICS", "OLA", "IPMPLS-Access"],
        "site_type_main": ["OPTICS", "IPMPLS-Access","DWDM-OLA"],
        #"site_type_main": ["RAN-BTS", "MICROWAVE", "OPTICS", "OLA", "IPMPLS-Access"],
        "site_type_vi": "Access POP",
        "site_type_infra": "Tx Hub",
        "frequency": 2,
        "proposed_frequency": 2,
        "synergy": ["RAN FE", "Tx FE"],
        "priority": 6,
        "category": 4
    },
    # {
    #     "site_type1": ["OLA", "Access Optical", "Access Router"],
    #     "site_type_main1": ["OLA"],
    #     "site_type": ["OLA", "OPTICS", "IPMPLS-Access"],
    #     "site_type_main": ["DWDM-OLA"],
    #     #"site_type_main": ["OLA"],
    #     "site_type": ["OLA", "OPTICS", "IPMPLS-Access"],
    #     "site_type_vi": "Access POP",
    #     "site_type_infra": "Tx Hub",
    #     "frequency": 2,
    #     "proposed_frequency": 2,
    #     "synergy": ["Tx FE"],
    #     "priority": 7,
    #     "category": 3
    # },
    {
        "site_type1": ["RAN", "MICROWAVE"],
        "site_type_main1": ["RAN", "MICROWAVE"],
        "site_type": ["RAN-BTS", "MICROWAVE"],
        "site_type_main": ["RAN-BTS","MICROWAVE"],
        "site_type_vi": "Tail/ Repeater Site",
        "site_type_infra": "Access Site",
        "frequency": 2,
        "proposed_frequency": 2,
        "synergy": ["RAN FE"],
        "priority": 8,
        "category": 2
    }
]
output_file = 'master_file_site_type_mylogic6.xlsx'           # Specify the output Excel file name
output_file1 = 'master_file_site_type_cat_updated.xlsx'           # Specify the output Excel file name


for item in site_ownership:
    print(item['site_type'])
    # for key, value in item.items():
    #     print(f"Key: {key}, Value: {value}")
#print(site_ownership)
#print(site_ownership[1])


# folder_path = r"C:\Users\Rahul\Downloads"
# folder_path = r"C:\Users\com\Documents\facts\apps\PMS\Files"
folder_path = r"C:\Users\hp\OneDrive\Documents"

# file_name = "PMS_Master_Data_1.xlsx"
#file_name = "my_test_site_type.xlsx"
file_name = "PMS_Master_Data_dwdm.xlsx"

print("folder_path = ", folder_path)
print("file_name = ", file_name)

final_file = os.path.join(folder_path, file_name)
print("final_file = ", final_file)

start_time = time.time()
# master_df1 = pd.read_excel(final_file, sheet_name="PMS_Master_Data_1")
master_df = pd.read_excel(final_file)

#print(master_df1.head())

#print("master_df1 = ", master_df1.shape)
print("Time Taken = ", time.time() - start_time)

#master_df = master_df1
# master_df.loc[master_df['Sub Category'] == 'OLA', 'DOMAIN'] = 'DWDM_OLA'
# master_df.loc[master_df['Sub Category'] == 'WDM-ROADM', 'DOMAIN'] = 'DWDM_ROADM'
# master_df.loc[master_df['Sub Category'].str.contains('DXC', case=False, na=False), 'DOMAIN'] = 'DWDM_DXC'

# # FOADM/DXC,OTM/DXC,WDM-ROADM,DXC,OLA

# #master_df.loc[master_df['Sub Category'] == 'DXC', 'DOMAIN'] = 'DWDM_DXC'
# # Update InScope based on DOMAIN values
# master_df.loc[master_df['DOMAIN'] == 'DWDM', 'Scope'] = 'OutScope'
# master_df.loc[master_df['DOMAIN'].isin(['DWDM_DXC', 'DWDM_OLA','DWDM_ROADM']), 'Scope'] = 'InScope'

master_df['category'] = ''
#master_df['Scope'] = 'InScope'
#master_df = master_df[master_df['Scope'] =='In Scope']

master_df['scope'] = ''
out_of_scope_domains = {"DWDM", "RAN", "IPMPLS"}
master_df.loc[master_df['NSSID'].isnull() | master_df['DOMAIN'].isin(out_of_scope_domains), 'scope'] = 'OutOfScope'
master_df.loc[master_df['scope'] == '', 'scope'] = 'InScope'

#print("master_df = ", master_df.shape)
#master_df.to_excel(output_file, sheet_name='master_file_mobility.xlsx', index=False)
unique_circle = master_df['CIRCLE_CODE'].unique().tolist()
print("unique_circle = ", unique_circle)
# unique_circle=["DEL"]

for circle in unique_circle:
    # circle = "DEL"
    filtered_circle_df = master_df[master_df['CIRCLE_CODE']==circle]
    # print("filtered_circle_df = ", circle, filtered_circle_df.shape)
    


    for item in site_ownership:
        #print()
        # print(item['site_type'])
        site_type1 = item['site_type1']
        site_type_main1 = item['site_type_main1']
        site_type = item['site_type']
        site_type_main = item['site_type_main']
        site_type_vi = item['site_type_vi']
        site_type_infra = item['site_type_infra']
        frequency = item['frequency']
        proposed_frequency = item['proposed_frequency']
        synergy = item['synergy']
        priority = item['priority']
        category = item['category']

        if category in [9,8,7,6]:
            #print("9,8,7,6")
            #print("priority = ", category, priority)
    
            filtered_cat_df = filtered_circle_df[filtered_circle_df['category'] == '']

            filtered_cat_df = filtered_cat_df[filtered_cat_df['DOMAIN'].isin(site_type_main)]
           
            nssid_values = filtered_cat_df['NSSID'].unique().tolist()
            #print("NSSID values from filtered_cat_df: ", len(nssid_values))
    
            final_filtered_df = master_df[
                (master_df['CIRCLE_CODE'] == circle) &
                (master_df['NSSID'].isin(nssid_values)) & 
                (master_df['category'] == '') 
                # (master_df['DOMAIN'].isin(site_type))
            ]
    
            master_df.loc[
                (master_df['CIRCLE_CODE'] == circle) &
                (master_df['NSSID'].isin(nssid_values)) & 
                (master_df['category'] == '') 
                # (master_df['DOMAIN'].isin(site_type))
                , 'category'
            ] = category
            filtered_circle_df.loc[
                #(filtered_circle_df['CIRCLE_CODE'] == circle) &
                (master_df['CIRCLE_CODE'] == circle) &
                (filtered_circle_df['NSSID'].isin(nssid_values)) & 
                (filtered_circle_df['category'] == '') 
                # (filtered_circle_df['DOMAIN'].isin(site_type))
                , 'category'
            ] = category
       
        elif category in [4]:
            filtered_cat_df = filtered_circle_df[
                (filtered_circle_df['category'] == '') &
                (filtered_circle_df['DOMAIN'].isin(site_type_main))
            ]
            #print("Filtered Category DataFrame:\n", filtered_cat_df)

            # Get unique NSSID values from filtered data
            nssid_values = filtered_cat_df['NSSID'].unique().tolist()
            #print("Unique NSSIDs from filtered_cat_df:", nssid_values)

            # Group by NSSID and collect all domains for each NSSID
            nssid_all_domains = filtered_circle_df[filtered_circle_df['NSSID'].isin(nssid_values)].groupby('NSSID')['DOMAIN'].apply(set)
            #print("All domains by NSSID:\n", nssid_all_domains)

            # Define the required domain sets
            site_type_main_set = set(site_type_main)
            category_4_domains = site_type_main_set.union({"RAN-BTS", "MICROWAVE"})
            #print("Site Type Main Set:", site_type_main_set)
            #print("Category 4 Domains Set:", category_4_domains)

            # Check each NSSID and their domains for categorization
            nssid_for_cat_3 = []
            nssid_for_cat_4 = []

            for nssid, domains in nssid_all_domains.items():
                #print(f"NSSID: {nssid}, Domains: {domains}")

                # Check for Category 3: must contain any of site_type_main without RAN or Microwave
                if any(domain in domains for domain in site_type_main) and not any(d in domains for d in {"RAN-BTS", "MICROWAVE"}):
                    nssid_for_cat_3.append(nssid)
                    #print(f"{nssid} matches Category 3")

                # Check for Category 4: must contain any from site_type_main and at least one of RAN or Microwave
                if any(domain in domains for domain in site_type_main) and (any(d in domains for d in {"RAN-BTS", "MICROWAVE"})):
                    nssid_for_cat_4.append(nssid)
                    #print(f"{nssid} matches Category 4")

           
            if nssid_for_cat_3:
                master_df.loc[
                    (master_df['CIRCLE_CODE'] == circle) &
                    (master_df['NSSID'].isin(nssid_for_cat_3)) &
                    (master_df['category'] == '')
                    , 'category'
                ] = 3
                
                filtered_circle_df.loc[
                    #(filtered_circle_df['CIRCLE_CODE'] == circle) &
                    (master_df['CIRCLE_CODE'] == circle) &
                    (filtered_circle_df['NSSID'].isin(nssid_for_cat_3)) &
                    (filtered_circle_df['category'] == '')
                    , 'category'
                ] = 3

            if nssid_for_cat_4:
                master_df.loc[
                    (master_df['CIRCLE_CODE'] == circle) &
                    (master_df['NSSID'].isin(nssid_for_cat_4)) &
                    (master_df['category'] == '')
                    , 'category'
                ] = 4  # Assign Category 4
                        
                filtered_circle_df.loc[
                    (master_df['CIRCLE_CODE'] == circle) &
                    #(filtered_circle_df['CIRCLE_CODE'] == circle) &
                    (filtered_circle_df['NSSID'].isin(nssid_for_cat_4)) &
                    (filtered_circle_df['category'] == '')
                    , 'category'
                ] = 4
        elif category in [2]:
            filtered_cat_df = filtered_circle_df[filtered_circle_df['category'] == '']
            print("filtered_cat_df 111= ", len(filtered_cat_df))
            filtered_cat_df = filtered_cat_df[filtered_cat_df['DOMAIN'].isin(site_type_main)]

           
            final_filtered_df = master_df[
                (master_df['CIRCLE_CODE'] == circle) &
                (master_df['category'] == '') 
            ]
    
            master_df.loc[
                (master_df['CIRCLE_CODE'] == circle) &
                (master_df['category'] == '') 
                , 'category'
            ] = category
            filtered_circle_df.loc[
                (master_df['CIRCLE_CODE'] == circle) &
                (filtered_circle_df['category'] == '') 
                , 'category'
            ] = category
    
    
master_df.to_excel(output_file, sheet_name='master_file_mobility', index=False)
excel1 = pd.read_excel('master_file_site_type_mylogic6.xlsx')
excel2 = pd.read_excel('site_type.xlsx')    
merged_df = pd.merge(excel1, excel2, on='category', how='left')
merged_df.to_excel(output_file1, sheet_name='master_file_mobility', index=False)
            
         
   

            
        
#master_df.to_excel(output_file, sheet_name='master_file_mobility', index=False)



#IDKA102080 IDKA103580

