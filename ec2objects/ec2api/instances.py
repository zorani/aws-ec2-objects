from __future__ import annotations

import datetime
import json
import os
import queue
import random
import threading
import time

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
        if arg_region != None:
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

    def latest_instance_info(self, instance_id, arg_region):
        ec2_client = boto3.client("ec2", region_name=arg_region)
        latest_instances_info_list = ec2_client.describe_instances(
            InstanceIds=[instance_id]
        )
        latest_instances_info_attributes = latest_instances_info_list["Reservations"][
            0
        ]["Instances"][0]
        return latest_instances_info_attributes

    def stop_instance(self, instance_id, arg_region):
        ec2_resource = boto3.resource("ec2", region_name=arg_region)
        instance = ec2_resource.Instance(instance_id)
        print("sent stop signal")
        instance.stop()
        print("waiting untill stop..")
        instance.wait_until_stopped()
        print("stopped")

    def start_instance(self, instance_id, arg_region):
        ec2_resource = boto3.resource("ec2", region_name=arg_region)
        instance = ec2_resource.Instance(instance_id)
        print("sent start signal")
        info = instance.start()
        print(instance_id)
        print(info["StartingInstances"][0]["InstanceId"])
        print("waiting untill start..")
        instance.wait_until_running()
        print("started")
        # Amazon EC2 docs state that under some circumstances the instance ID changes,
        # well... to catch this, we return the instance id returned by start

        return info["StartingInstances"][0]["InstanceId"]

    def terminate_instance(self, instance_id, arg_region):
        ec2_resource = boto3.resource("ec2", region_name=arg_region)
        instance = ec2_resource.Instance(instance_id)
        print("Sending instance term signal...")
        instance.terminate()
        print("waiting untill terminater..")
        instance.wait_until_terminated()
        print("terminate")

    def reboot_instance(self, instance_id, arg_region):
        ec2_resource = boto3.resource("ec2", region_name=arg_region)
        instance = ec2_resource.Instance(instance_id)
        print("sending reboot signal")
        instance.reboot()
        print("waiting for reboot")
        instance.wait_until_running()
        print("Rebooted")

    def reload_instance(self, instance_id, arg_region):
        # Updates the attributes of the instance resource.
        ec2_resource = boto3.resource("ec2", region_name=arg_region)
        instance = ec2_resource.Instance(instance_id)
        instance.reload()

    def list_instances(self, arg_region):
        ec2_client = boto3.client("ec2", region_name=arg_region)
        response = ec2_client.describe_instances()
        instances_list = []
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instances_list.append(instance["InstanceId"])
        return instances_list
