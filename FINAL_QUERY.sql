SELECT circle.circle_name,zones.zone_name,subzones.subzone_name,  
sites.site_id,sites.nssid,sites.subzone_id,sites.category_id,site_type.site_type_name,  
site_group.site_group_name,users.user_name,COUNT(equipments.equipment_id) AS equipment_count, 
JSON_AGG(JSON_BUILD_OBJECT
('equipment_name', equipments.equipment_name,
'domain_name', domain.domain_name,     
'vendor_name', vendors.vendor_name)) AS equipment_info 
FROM sites 
JOIN subzones ON subzones.subzone_id = sites.subzone_id 
JOIN zones ON zones.zone_id = subzones.zone_id
JOIN circle ON circle.circle_id = zones.circle_id 
JOIN site_type ON site_type.category_id = sites.category_id
JOIN site_group ON site_group.site_group_id = site_type.site_group_id 
JOIN assigned_subzones ON assigned_subzones.subzone_id = sites.subzone_id 
JOIN users ON users.user_id = assigned_subzones.user_id
LEFT JOIN equipments ON equipments.site_id = sites.site_id 
LEFT JOIN vendors ON vendors.id = equipments.vendor_id
LEFT JOIN domain ON domain.category_id = sites.category_id
GROUP BY circle.circle_name, zones.zone_name, subzones.subzone_name, sites.site_id, sites.nssid,
sites.subzone_id, sites.category_id, site_type.site_type_name, site_group.site_group_name, users.user_name;