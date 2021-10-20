from __future__ import annotations


import os
import time
import queue
import threading
import datetime
import random
import json
import boto3


class Instances:
    def __init__(self):
        self.ec2_client = boto3.client("ec2")
        self.ec2_resource = boto3.resource("ec2")

    def create_instance(
        self,
        image_id,
        instance_type,
        ssh_key_name,
        tag_specification=None,
        arg_region=None,
    ):
        if arg_region:
            # If a region is specified we create the ec2 instance in that region.
            ec2_client = boto3.client("ec2", region_name=arg_region)
        else:
            ec2_client = self.ec2_client

        # Starting an instance...
        # A list of instances will be returned, be we only request one to
        # be created so we will retrive the first item later.
        instances_info_list = ec2_client.run_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName=ssh_key_name,
            TagSpecifications=tag_specification,
        )

        # We are going to need the instance id.
        instance_id = instances_info_list["Instances"][0]["InstanceId"]

        # Wait for the instance to start running
        waiter_running = ec2_client.get_waiter("instance_running")
        waiter_running.wait(InstanceIds=[instance_id])

        # Wait for the instance to have a status:OK
        waiter_status = ec2_client.get_waiter("instance_status_ok")
        waiter_status.wait(InstanceIds=[instance_id])

        # There is going to be NEW information that is available after the instance has fully started.
        # Here we extract that.
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
        updated_instances_info_list = ec2_client.describe_instances(
            InstanceIds=[instance_id]
        )

        return updated_instances_info_list

    def stop_instance(self, instance_id, arg_region=None):

        if arg_region != None:
            # If a region is specified we create the ec2 instance in that region.
            ec2_client = boto3.client("ec2", region_name=arg_region)
        else:
            ec2_client = self.ec2_client

        ec2_client.stop_instances(InstanceIds=[instance_id])

    def list_instance(self):
        pass
