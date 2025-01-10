from sqlalchemy import Column, String, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import INET  # For IPv4 addresses
from pydantic import BaseModel, validator
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

class SiteDetails(Base):
    __tablename__ = 'circuit_inventory_master'

    circle = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    site_name = Column(String(255), nullable=True)
    site_id = Column(String(255), nullable=False)
    nss_id = Column(String(255), nullable=True)
    technology = Column(String(255), nullable=True)
    order_id = Column(String(255), nullable=True)
    circuit_id = Column(String(255), nullable=True)
    service_type = Column(String(255), nullable=True)
    new_vlan = Column(String(255), nullable=True)
    enodeb_ip = Column(INET, nullable=False)
    e_nodeb_service_ip = Column(INET, nullable=True)
    mw_id_connected_to_site = Column(String(255), nullable=True)
    mw_port_connected_to_site = Column(String(255), nullable=True)
    mw_id_connected_to_mux = Column(String(255), nullable=True)
    mw_port_connected_to_mux = Column(String(255), nullable=True)
    mux_id_connected_to_mw = Column(String(255), nullable=True)
    mux_port_connected_to_mw = Column(String(255), nullable=True)
    mux_id_connected_to_router = Column(String(255), nullable=True)
    mux_port_connected_to_router = Column(String(255), nullable=True)
    site_router_location = Column(String(255), nullable=True)
    site_parented_router_host_name = Column(String(255), nullable=True)
    site_parented_router_port = Column(String(255), nullable=True)
    site_parented_router_interface_ip = Column(INET, nullable=True)
    site_parented_vrf_name = Column(String(255), nullable=True)
    mme1_parented_pe_primary_router_hostname = Column(String(255), nullable=True)
    mme1_parented_pe_primary_router_port = Column(String(255), nullable=True)
    mme1_parented_pe_primary_router_interface_ip = Column(INET, nullable=True)
    mme1_parented_pe_primary_router_vlan = Column(String(255), nullable=True)
    mme1_parented_pe_router_vrf = Column(String(255), nullable=True)
    mme1_parented_dcgw_primary_router_hostname = Column(String(255), nullable=True)
    mme1_parented_dcgw_primary_router_port = Column(String(255), nullable=True)
    mme2_parented_pe_primary_router_hostname = Column(String(255), nullable=True)
    mme2_parented_pe_primary_router_port = Column(String(255), nullable=True)
    mme2_parented_pe_primary_router_interface_ip = Column(INET, nullable=True)
    mme2_parented_pe_primary_router_vlan = Column(String(255), nullable=True)
    mme2_parented_pe_router_vrf = Column(String(255), nullable=True)
    mme2_parented_dcgw_primary_router_hostname = Column(String(255), nullable=True)
    mme2_parented_dcgw_primary_router_port = Column(String(255), nullable=True)
    vgw1_parented_pe_primary_router_hostname = Column(String(255), nullable=True)
    vgw1_parented_pe_primary_router_port = Column(String(255), nullable=True)
    vgw1_parented_pe_primary_interface_ip = Column(INET, nullable=True)
    vgw1_parented_pe_primary_router_vlan = Column(String(255), nullable=True)
    vgw1_parented_pe_primary_router_vrf = Column(String(255), nullable=True)
    vgw1_parented_dcgw_primary_router_hostname = Column(String(255), nullable=True)
    vgw1_parented_dcgw_primary_router_port = Column(String(255), nullable=True)
    vgw2_parented_pe_primary_router_hostname = Column(String(255), nullable=True)
    vgw2_parented_pe_primary_router_port = Column(String(255), nullable=True)
    vgw2_parented_pe_primary_router_interface_ip = Column(INET, nullable=True)
    vgw2_parented_pe_primary_router_vlan = Column(String(255), nullable=True)
    vgw2_parented_pe_primary_router_vrf = Column(String(255), nullable=True)
    vgw2_parented_dcgw_primary_router_hostname = Column(String(255), nullable=True)
    vgw2_parented_dcgw_primary_router_port = Column(String(255), nullable=True)
    oss_parented_pe_primary_router_hostname = Column(String(255), nullable=True)
    oss_parented_pe_router_port = Column(String(255), nullable=True)
    oss_parented_pe_primary_interface_ip = Column(INET, nullable=True)
    oss_parented_pe_primary_router_vlan = Column(String(255), nullable=True)
    oss_parented_pe_primary_router_vrf = Column(String(255), nullable=True)
    s1c_vrf_rd_value = Column(String(255), nullable=True)
    s1c_vrf_rt_value = Column(String(255), nullable=True)
    s1u_vrf_rd_value = Column(String(255), nullable=True)
    s1u_vrf_rt_value = Column(String(255), nullable=True)
    om_vrf_rd_value = Column(String(255), nullable=True)
    om_vrf_rt_value = Column(String(255), nullable=True)
    mme1_service_ip = Column(INET, nullable=True)
    mme2_service_ip = Column(INET, nullable=True)
    vgw1_service_ip = Column(INET, nullable=True)
    vgw2_service_ip = Column(INET, nullable=True)
    oss_service_ip = Column(INET, nullable=True)
    __table_args__ = (
        PrimaryKeyConstraint('site_id', 'enodeb_ip'),
    )

class software_version(Base):
    __tablename__ = 'software_version_copy'

    domain = Column(String(255), nullable=True)
    ne_family = Column(String(255), nullable=True)
    oem = Column(String(255), nullable=True)
    ne_type = Column(String(255), nullable=False)
    circle = Column(String(255), nullable=True)
    model_name = Column(String(255), nullable=True)
    ip_address = Column(String(255), nullable=True)
    current_sw_version = Column(String(100), nullable=True)
    hostname = Column(String(255), nullable=True)
    created_at = Column(String(255), nullable=True)
    standard_ne_type = Column(String(255), nullable=False)
    last_upgrade_date = Column(DateTime, server_default=func.now(), nullable=True)

class upgrade_software_version(Base):
    __tablename__ = 'upgrade_software_version'

    domain = Column(String(255), nullable=True)
    ne_family = Column(String(255), nullable=True)
    oem = Column(String(255), nullable=True)
    ne_type = Column(String(255), nullable=False)
    current_version = Column(String(100), nullable=True)
    model_hw_type = Column(String(255), nullable=True)
    latest_version = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=True)  


class software_version_data(Base):
    __tablename__ = 'software_version_data'

    domain = Column(String(255), nullable=True)
    ne_family = Column(String(255), nullable=True)
    oem = Column(String(255), nullable=True)
    ne_type = Column(String(255), nullable=False)
    circle = Column(String(255), nullable=True)
    model_name = Column(String(255), nullable=True)
    ip_address = Column(String(255), nullable=True)
    current_sw_version = Column(String(100), nullable=True)
    hostname = Column(String(255), nullable=True)
    created_at = Column(String(255), nullable=True)    
    standard_ne_type = Column(String(255), nullable=False)
    last_upgrade_date = Column(DateTime, server_default=func.now(), nullable=True)