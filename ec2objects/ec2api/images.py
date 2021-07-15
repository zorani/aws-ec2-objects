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

    def list_all_amazon_public_images(self):
        json_results = self.ec2_client.describe_images(Owners=["amazon"])
        return json_results

    def retrieve_image(self, imageId):
        json_results = self.ec2_client.describe_images(ImageIds=[imageId])
        return json_results
