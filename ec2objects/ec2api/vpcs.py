from __future__ import annotations


import os
import time
import queue
import threading
import datetime
import random
import json
import boto3


class VPCs:
    def __init__(self):
        self.ec2_client = boto3.client("ec2")
        self.ec2_resource = boto3.resource("ec2")

    def create_vpc_IPV4(self, CidrBlock: str, arg_region=None):
        if arg_region != None:
            # If a region is specified we create the ec2 instance in that region.
            ec2_client = boto3.client("ec2", region_name=arg_region)
        else:
            ec2_client = self.ec2_client

        response = ec2_client.create_vpc(CidrBlock=CidrBlock)
        return response["Vpc"]
