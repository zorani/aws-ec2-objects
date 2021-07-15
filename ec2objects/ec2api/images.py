from __future__ import annotations

from .ec2apiconnection import EC2ApiConnection
from bs4 import BeautifulSoup
import os
import time
import queue
import threading
import datetime
import random
import json
import boto3

import xml.etree.ElementTree as ET
from io import BytesIO


class Images(EC2ApiConnection):
    def __init__(self):
        EC2ApiConnection.__init__(self)
        self.ec2_client = boto3.client("ec2")

    def list_all_public_images(self):
        # "us-east-1"
        params = {}
        # This gets a lot of data, need to wait a while... setting timeout to 120sec
        params["Action"] = "DescribeImages"
        params["Region"] = self.default_region
        params["Owner.1"] = "amazon"
        # params["ImageId.1"] = "ami-058b1b7fe545997ae"
        # params["Filter.1.Name"] = "is-public"
        # params["Filter.1.Value.1"] = "true"
        # params["Filter.2.Name"] = "architecture"
        # params["Filter.2.Value.1"] = "x86_64"
        # params["Filter.3.Name"] = "platform"
        # params["Filter.3.Value.1"] = "windows"
        response = self.get_request(params=params)
        if response:
            old_content = response.content
            # print(old_content)
            old_content_byte_encoded = BytesIO(old_content)
            tree = ET.parse(old_content_byte_encoded)
            root = tree.getroot()
            imageSet = ET.tostring(root[1])
            response._content = self.xml_to_json_response(imageSet)
        return response

    def list_all_amazon_public_images(self):
        json_results = self.ec2_client.describe_images(Owners=["amazon"])
        return json_results

    def retrieve_image(self, imageId):
        json_results = self.ec2_client.describe_images(ImageIds=[imageId])
        return json_results
