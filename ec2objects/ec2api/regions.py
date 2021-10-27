from __future__ import annotations

import datetime
import json
import os
import queue
import random
import threading
import time

import boto3


class Regions:
    def __init__(self):
        self.ec2_client = boto3.client("ec2")

    def list_all_regions_enabled_for_my_account(self):
        regions_json = self.ec2_client.describe_regions(AllRegions=False)
        return regions_json

    def list_all_regions(self):
        regions_json = self.ec2_client.describe_regions(AllRegions=True)
        return regions_json

    def list_availabitily_zones_for_region(self, regionname):
        local_client = boto3.client("ec2", region_name=regionname)
        # print(regionname)
        try:
            availabilityzones_json = local_client.describe_availability_zones(
                Filters=[
                    {"Name": "region-name", "Values": [regionname]},
                ],
                # AllAvailabilityZones=True,
            )
        except:
            availabilityzones_json = {}

        return availabilityzones_json
        # return self.availabilityzoens[regionname]
