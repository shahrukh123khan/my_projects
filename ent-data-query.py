# --  updating kpi value on the basis of nssid from final kpi table 

# -- # UPDATE site_type_d
# -- # SET kpi = 'Yes'
# -- # FROM final_kpi
# -- # WHERE final_kpi.nssid LIKE '%' || site_type_data.nssid || '%'
# -- #   AND site_type_data.circle_code = final_kpi.standard_name_uim;



# --  udating alarm 

# -- # UPDATE site_type_data
# -- # SET alarm = 'Yes'
# -- # FROM ran_alarms
# -- # WHERE site_type_data.circle_code = ran_alarms.circle_code
# -- #   AND site_type_data.nssid = ran_alarms.nss_id
# -- #   AND site_type_data.domain = 'RAN-BTS'
# -- #   AND ran_alarms.days_between = 'YES';



# -- # UPDATE site_type_data
# -- # SET alarm = 'Yes'
# -- # FROM mw_pm_alarms
# -- # WHERE site_type_data.circle_code = mw_pm_alarms.circle_code
# -- #   AND site_type_data.nssid = mw_pm_alarms.nss_id
# -- #   AND site_type_data.domain = 'MICROWAVE'
# -- #   AND mw_pm_alarms.days_between = 'YES';


# -- # UPDATE site_type_data
# -- # SET alarm = 'Yes'
# -- # FROM mw_fluctuation_alarms
# -- # WHERE site_type_data.circle_code = mw_fluctuation_alarms.circle_code
# -- #   AND site_type_data.nssid = mw_fluctuation_alarms.nss_id
# -- #   AND site_type_data.domain = 'MICROWAVE'
# -- #   AND mw_fluctuation_alarms.days_between = 'YES';






# -- updating the alarm value in site_type_data from alarm table on the basis of circle--nssid 

# -- UPDATE site_type_data
# -- SET alarm = 'Yes'
# -- FROM ran_alarms
# -- WHERE site_type_data.circle_code = ran_alarms.circle_code
# --   AND site_type_data.nssid = ran_alarms.nss_id
# --   AND site_type_data.domain = 'RAN-BTS'
# --   AND ran_alarms.days_between = 'YES';


# -- UPDATE site_type_data
# -- SET alarm = 'Yes'
# -- FROM mw_pm_alarms
# -- WHERE site_type_data.circle_code = mw_pm_alarms.circle_code
# --   AND site_type_data.nssid = mw_pm_alarms.nss_id
# --   AND site_type_data.domain = 'MICROWAVE'
# --   AND mw_pm_alarms.days_between = 'YES';



# -- UPDATE site_type_data
# -- SET alarm = 'Yes'
# -- FROM mw_fluctuation_alarms
# -- WHERE site_type_data.circle_code = mw_fluctuation_alarms.circle_code
# --   AND site_type_data.nssid = mw_fluctuation_alarms.nss_id
# --   AND site_type_data.domain = 'MICROWAVE'
# --   AND mw_fluctuation_alarms.days_between = 'YES';




# -- updating zone and sub zone in site_type_data on the basis of nssid from cxx data table 

# --  UPDATE site_type_data
# --  SET site_type_data.zone = cxx_data.zone
# --      site_type_data.subzone = cxx_data.subzone
# --  FROM cxx_data
# --  WHERE cxx_data.nss_id = site_type_data.nssid;




# -- UPDATE site_type_data
# -- SET codes = CASE circle_code
# --     WHEN 'DEL' THEN 1
# --     WHEN 'RAJ' THEN 2
# --     WHEN 'APR' THEN 3
# --     WHEN 'TNC' THEN 4
# --     WHEN 'HPR' THEN 5
# --     WHEN 'HAR' THEN 6
# --     WHEN 'JNK' THEN 7
# --     WHEN 'KAR' THEN 8
# --     WHEN 'KER' THEN 9
# --     WHEN 'PJB' THEN 10
# --     WHEN 'UPE' THEN 12
# --     WHEN 'UPW' THEN 13
# --     WHEN 'BIH' THEN 14
# --     WHEN 'ODI' THEN 15
# --     WHEN 'ANE' THEN 16
# --     WHEN 'KOL' THEN 18
# --     WHEN 'ROB' THEN 19
# --     WHEN 'MAH' THEN 20
# --     WHEN 'MPC' THEN 21
# --     WHEN 'GUJ' THEN 22
# --     WHEN 'MUM' THEN 43
# --     ELSE NULL  
# -- END;



# -- mapping codes with circle

# -- UPDATE site_type_data
# -- SET uwfm_circle_code_name = CASE codes
# --     WHEN 1 THEN 'DEL'
# --     WHEN 2 THEN 'RAJ'
# --     WHEN 3 THEN 'APR'
# --     WHEN 4 THEN 'CHN'
# --     WHEN 5 THEN 'HPR'
# --     WHEN 6 THEN 'HAR'
# --     WHEN 7 THEN 'JNK'
# --     WHEN 8 THEN 'KAR'
# --     WHEN 9 THEN 'KEL'
# --     WHEN 10 THEN 'PNB'
# --     WHEN 11 THEN 'ROTN'
# --     WHEN 12 THEN 'UPE'
# --     WHEN 13 THEN 'UPW'
# --     WHEN 14 THEN 'BIH'
# --     WHEN 15 THEN 'ODI'
# --     WHEN 16 THEN 'NES'
# --     WHEN 17 THEN 'ASM'
# --     WHEN 18 THEN 'KOL'
# --     WHEN 19 THEN 'ROB'
# --     WHEN 20 THEN 'MAG'
# --     WHEN 21 THEN 'MPCG'
# --     WHEN 22 THEN 'GUJ'
# --     WHEN 43 THEN 'MUM'
# --     ELSE NULL  -- Set to NULL or another default value if not matched
# -- END;



# -- uwfm data mapping concating the subzone with circle name 

# -- UPDATE site_type_data
# -- SET uwfm_circle_subzone_name = CONCAT(subzone, '-', uwfm_circle_name);


# -- remove specific part from the subzone text 
# it will remove the zone text . any text we can remove .

# -- UPDATE site_type_data
# -- SET uwfm_circle_subzone_name = CONCAT(REPLACE(subzone, 'Zone', ''), '-', uwfm_circle_name);

# removing vi from the uwfm_circle_subzone_name 


# UPDATE site_type_data
# SET remove_vi_uwfm_csz = CASE
#     WHEN uwfm_circle_subzone_name LIKE 'VI_%' THEN REPLACE(uwfm_circle_subzone_name, 'VI_', '')
#     ELSE uwfm_circle_subzone_name
# END;

# updating the site_type_data username full name and email column on the basis of matching the uwfm_circle_subzone_name and 
#zone_name in uwfm table 

# UPDATE site_type_data
# SET
#     username = uwfm_data.username,
#     fullname = uwfm_data.fullname,
#     email = uwfm_data.email
# FROM uwfm_data
# WHERE uwfm_data.zones LIKE '%' || site_type_data.remove_vi_uwfm_csz || '%';

# handeling case insensitive 
# WHERE uwfm_data.zones ILIKE '%' || site_type_data.remove_vi_uwfm_csz || '%';

# handeling null values in the columns 

# WHERE uwfm_data.zones IS NOT NULL
#   AND site_type_data.remove_vi_uwfm_csz IS NOT NULL
#   AND uwfm_data.zones LIKE '%' || site_type_data.remove_vi_uwfm_csz || '%';

# complet query handeling the case sensitivity and null values 

# UPDATE site_type_data
# SET
#     username = uwfm_data.username,
#     fullname = uwfm_data.fullname,
#     email = uwfm_data.email
# FROM uwfm_data
# WHERE uwfm_data.zones IS NOT NULL
#   AND site_type_data.remove_vi_uwfm_csz IS NOT NULL
#   AND uwfm_data.zones ILIKE '%' || site_type_data.remove_vi_uwfm_csz || '%';


##################################
# select * from site_type_data
# select * from uwfm_data 
# UPDATE site_type_data
# SET
#     user_id = uwfm_data.user_id,
# 	user_name = uwfm_data.user_name,
#     full_name = uwfm_data.full_name,
#     email_id = uwfm_data.email_id
# FROM uwfm_data
# WHERE uwfm_data.zones IS NOT NULL
#   AND site_type_data.remove_vi_uwfm_csz IS NOT NULL
#   AND uwfm_data.zones ILIKE '%' || site_type_data.remove_vi_uwfm_csz || '%';



UPDATE site_type_data
SET
    user_id = uwfm_data_new.user_id,
	user_name = uwfm_data_new.user_name,
    full_name = uwfm_data_new.full_name,
    email_id = uwfm_data_new.email_id
FROM uwfm_data_new
WHERE uwfm_data_new.zone_names IS NOT NULL
  AND site_type_data.remove_vi_uwfm_csz IS NOT NULL
  AND uwfm_data_new.zone_names ILIKE '%' || site_type_data.remove_vi_uwfm_csz || '%';





UPDATE site_type_data
SET
    user_id = uwfm_data_new.user_id,
	user_name = uwfm_data_new.user_name,
    full_name = uwfm_data_new.full_name,
    email_id = uwfm_data_new.email_id
FROM uwfm_data_new
WHERE uwfm_data_new.zone_names IS NOT NULL
  AND site_type_data.remove_id_uwfm_csz IS NOT NULL
  AND uwfm_data_new.zone_names ILIKE '%' || site_type_data.remove_id_uwfm_csz || '%';


INSERT INTO zones (zone_name)
SELECT new_zones.zone_name
FROM new_zones
WHERE NOT EXISTS (
    SELECT 1
    FROM zones
    WHERE zones.zone_name = new_zones.zone_name
);


#select nssid,domain,user_name from site_type_data where uwfm_circle_name='DEL' and zone='VI_GHAZIABAD' and subzone='VI_INDRAPURAM'and category=2