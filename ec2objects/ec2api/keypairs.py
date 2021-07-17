from __future__ import annotations


import os
import time
import queue
import threading
import datetime
import random
import json
import boto3


class KeyPairs:
    def __init__(self):
        self.ec2_client = boto3.client("ec2")

    def list_keypairs(
        self,
    ):
        json_results = self.ec2_client.describe_key_pairs()
        return json_results

    def get_keypair_by_name(self, name):
        json_results = self.ec2_client.describe_key_pairs(
            Filters=[
                {"Name": "key-name", "Values": [name]},
            ]
        )
        return json_results

    def get_keypair_by_id(self, keypairid):
        json_results = self.ec2_client.describe_key_pairs(
            Filters=[
                {"Name": "key-pair-id", "Values": [keypairid]},
            ]
        )
        return json_results

    def get_keypair_by_fingerprint(self, fingerprint):
        json_results = self.ec2_client.describe_key_pairs(
            Filters=[
                {"Name": "fingerprint", "Values": [fingerprint]},
            ]
        )
        return json_results

    def get_keypair_by_tag_keyname(self, tagkeyname):
        json_results = self.ec2_client.describe_key_pairs(
            Filters=[
                {"Name": "tag-key", "Values": [tagkeyname]},
            ]
        )
        return json_results

    def get_keypair_by_tag(self, key, value):
        NameValue = f"tag:{key}"
        json_results = self.ec2_client.describe_key_pairs(
            Filters=[
                {"Name": NameValue, "Values": [value]},
            ]
        )
        return json_results

    def import_keypair(self, name, publickey_string, tag_specification):
        publickeymaterial = publickey_string.encode("utf-8")
        json_results = self.ec2_client.import_key_pair(
            KeyName=name,
            PublicKeyMaterial=publickeymaterial,
            TagSpecifications=tag_specification,
        )
        return json_results

    def delete_keypair(self, KeyName):
        response = self.ec2_client.delete_key_pair(KeyName=KeyName)
        return response
