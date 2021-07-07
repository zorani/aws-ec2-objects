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
    regionName: str = None
    regionEndpoint: str = None


class RegionManager:
    def __init__(self):
        self.regionapi = Regions()

    def retrieve_regions_enabled_for_my_account(self):
        region_objects = []
        response = self.regionapi.list_all_regions_enabled_for_my_account()
        if response:
            content = json.loads(response.content.decode("utf-8"))
            region_datas = content["regions"]
            for region_data in region_datas:
                newregion = Region()
                newregion.attributes = RegionAttributes(**region_data)
                region_objects.append(newregion)
            return region_objects

    def retrieve_all_regions(self):
        region_objects = []
        response = self.regionapi.list_all_regions()
        if response:
            content = json.loads(response.content.decode("utf-8"))
            region_datas = content["regions"]
            for region_data in region_datas:
                newregion = Region()
                newregion.attributes = RegionAttributes(**region_data)
                region_objects.append(newregion)
            return region_objects


class Region:
    def __init__(self):
        self.attributes = RegionAttributes()
