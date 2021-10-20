from __future__ import annotations

from dataclasses import dataclass, field
from ..ec2api.regions import Regions

from ..ec2common.ec2exceptions import *

import json
import threading
import time
import re


@dataclass
class RegionAttributes:
    RegionName: str = None
    Endpoint: str = None
    OptInStatus: str = None


@dataclass
class AvailabilityZones:
    State: str = None
    OptInStatus: str = None
    Messages: list = field(default_factory=list)
    RegionName: str = None
    ZoneName: str = None
    ZoneId: str = None
    GroupName: str = None
    NetworkBorderGroup: str = None
    ZoneType: str = None
    ParentZoneName: str = None
    ParentZoneId: str = None


class RegionManager:
    def __init__(self):
        self.regionapi = Regions()

    def retrieve_regions_enabled_for_my_account(self):
        region_objects = []
        region_json = self.regionapi.list_all_regions_enabled_for_my_account()
        region_datas = region_json["Regions"]
        # print(region_datas[0])
        for region_data in region_datas:
            newregion = Region()
            newregion.attributes = RegionAttributes(**region_data)
            newregion.availabilityzones = self.retrieve_availability_zones(
                newregion.attributes.RegionName
            )
            region_objects.append(newregion)
        return region_objects

    def retrieve_all_regions(self):
        region_objects = []
        region_json = self.regionapi.list_all_regions()
        region_datas = region_json["Regions"]
        # print(region_datas[0])
        for region_data in region_datas:
            newregion = Region()
            newregion.attributes = RegionAttributes(**region_data)
            newregion.availabilityzones = self.retrieve_availability_zones(
                newregion.attributes.RegionName
            )
            region_objects.append(newregion)
        return region_objects

    def retrieve_availability_zones(self, regionname):
        availability_zones = []
        try:
            availabilityzones_json = self.regionapi.list_availabitily_zones_for_region(
                regionname
            )
            availabilityzones_datas = availabilityzones_json["AvailabilityZones"]
            for availabilityzones_data in availabilityzones_datas:
                # print(availabilityzones_data)
                newavailabilityzone = AvailabilityZones(**availabilityzones_data)
                # print(newavailabilityzone)
                availability_zones.append(newavailabilityzone)
        except:
            raise AvailabilityZoneNotFound(
                f"Availability Zone not found for {regionname}"
            )
        # print(availability_zones)
        return availability_zones

    def retrieve_availability_zone_names_for_region(self, regionname):
        my_availability_zones_list = self.retrieve_availability_zones(regionname)
        my_availability_zones: AvailabilityZones
        availability_zone_names = []
        for my_availability_zones in my_availability_zones_list:
            availability_zone_names.append(my_availability_zones.ZoneName)
        return availability_zone_names


class Region:
    def __init__(self):
        self.attributes = RegionAttributes()
        self.availabilityzones = []
