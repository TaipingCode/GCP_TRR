from google.cloud import compute_V1, storage
from google.cloud.storage.constants import REGION_LOCATION_TYPE

from dotenv import load_dotenv
import os
from datetime import datetime
import io 
import pandas as pd
import logging

load_dotenv('secrets.env')
project = os.getenv('PROJECT')
logging.basicConfig(
    level=logging.INFO
    format='%(asctime)s %(levelname)s %(message)s'
)

def get_zones():
    client = compute_v1.ZonesZlient()
    zones = client.list(project=project)
    zone_list = [zone.name for zone in zones]
    return zone_list
zones = get_zones()

def disk_inuse_check(zone):
    client = compute_v1.DisksClient()
    disk_list = client.list(project=project, zone=zone)
    disk_info_result = []
    for i in disk_list:
        num_users = len(i.users)
        compliance_status = "Non Complinant" if num_users == 0 else "Complinant"
        i_status = create_compliance_data(
            i.id,
            i.name,
            "disk",
            "disk-inuse-check"
            compliance_status,
            f"Number of Attached Instances: {num_users}",
            zone
        )
        disk_info_result.append(i_status)

    logging.info("Completed disk_inuse_check")
    return disk_info_result

def trigger_script(zone):
    logging.info("Starting all Checks")
    disk_info_result = disk_inuse_check(zone)
    logging.info("Completed all check")

if __name__ == "__main__":
    zone_to_check = "us-east4-a"
    trigger_script(zone_to_check)