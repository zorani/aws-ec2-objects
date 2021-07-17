from __future__ import annotations


import os
import time
import queue
import threading
import datetime
import random
import json
import boto3


class Images:
    def __init__(self):
        self.ec2_client = boto3.client("ec2")

    def retrieve_image(self, imageId):
        json_results = self.ec2_client.describe_images(ImageIds=[imageId])
        return json_results

    def list_all_ubuntu_x86_64_machine_images_hvm_ssd(self, name=""):
        json_results = self.ec2_client.describe_images(
            Owners=["099720109477"],
            Filters=[
                {"Name": "architecture", "Values": ["x86_64"]},
                {
                    "Name": "name",
                    "Values": [f"ubuntu/images/hvm-ssd/ubuntu-{name.lower()}*"],
                },
                # {"Name": "image-type", "Values": ["machine"]},
                {"Name": "virtualization-type", "Values": ["hvm"]},
            ],
        )
        return json_results

    def list_all_ubuntu_arm64_machine_images_hvm_ssd(self, name=""):
        json_results = self.ec2_client.describe_images(
            Owners=["099720109477"],
            Filters=[
                {"Name": "architecture", "Values": ["arm64"]},
                {
                    "Name": "name",
                    "Values": [f"ubuntu/images/hvm-ssd/ubuntu-{name.lower()}*"],
                },
                # {"Name": "image-type", "Values": ["machine"]},
                {"Name": "virtualization-type", "Values": ["hvm"]},
            ],
        )
        return json_results
