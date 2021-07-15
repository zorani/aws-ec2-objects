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

    def list_all_amazon_public_images(self):
        json_results = self.ec2_client.describe_images(Owners=["amazon"])
        return json_results

    def retrieve_image(self, imageId):
        json_results = self.ec2_client.describe_images(ImageIds=[imageId])
        return json_results
