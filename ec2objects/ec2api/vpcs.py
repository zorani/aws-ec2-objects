from __future__ import annotations

import datetime
import json
import os
import queue
import random
import threading
import time

import boto3


class VPCs:
    def __init__(self):
        self.ec2_client = boto3.client("ec2")
        self.ec2_resource = boto3.resource("ec2")

    def create_vpc_IPV4(self, CidrBlock: str, arg_region=None):
        ec2_client = self._build_ec2_client(arg_region)
        # if arg_region != None:
        # If a region is specified we create the ec2 instance in that region.
        #    ec2_client = boto3.client("ec2", region_name=arg_region)
        # else:
        #    ec2_client = self.ec2_client

        response_create = ec2_client.create_vpc(CidrBlock=CidrBlock)
        VPCId = response_create["Vpc"]["VpcId"]
        waiter_vpc = ec2_client.get_waiter("vpc_available")
        waiter_vpc.wait(VpcIds=[VPCId])

        vpc_attributes = self.describe_vpc(VPCId, arg_region)
        # print(vpc_attributes)
        return vpc_attributes

    def describe_vpc(self, VPCId, arg_region):
        ec2_client = self._build_ec2_client(arg_region)
        response_desc = ec2_client.describe_vpcs(VpcIds=[VPCId])
        return response_desc["Vpcs"][0]

    def describe_vpcs_in_region(self, arg_region):
        ec2_client = self._build_ec2_client(arg_region)
        vpcs = ec2_client.describe_vpcs()
        return vpcs

    def get_all_region_names(self):
        # Returns region names that you have opted in.
        region_names = []
        response = self.ec2_client.describe_regions(AllRegions=True)
        region_records = response["Regions"]
        for region_record in region_records:
            if region_record["OptInStatus"] != "not-opted-in":
                region_names.append(region_record["RegionName"])
        return region_names

    def _build_ec2_client(self, arg_region):
        if arg_region != None:
            ec2_client = boto3.client("ec2", region_name=arg_region)
        else:
            ec2_client = self.ec2_client
        return ec2_client

    def update_vpc_IPV4(self, VpcId, arg_region):
        pass


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#vpc
