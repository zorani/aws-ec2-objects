from __future__ import annotations

from dataclasses import dataclass, field
from ..ec2api.keypairs import KeyPairs

from ..ec2common.ec2exceptions import *

import json
import threading
import time
import re


@dataclass
class KeyPairAttributes:
    KeyPairId: str = None
    KeyFingerprint: str = None
    KeyName: str = None
    # Tags: list = field(default_factory=list)


@dataclass
class Tags:
    Key: str = None
    Value: str = None


class KeyPairManager:
    def __init__(self):
        self.keypairapi = KeyPairs()

    def retrieve_keypairs(self):
        response = self.keypairapi.list_keypairs()
        keypair_objects = self._build_keypair_objects_from_response(response)
        return keypair_objects

    def retrieve_keypair_by_name(self, name):
        response = self.keypairapi.get_keypair_by_name(name)
        keypair_objects = self._build_keypair_objects_from_response(response)
        return keypair_objects

    def retrieve_keypair_by_id(self, keypairid):
        response = self.keypairapi.get_keypair_by_id(keypairid)
        keypair_objects = self._build_keypair_objects_from_response(response)
        return keypair_objects

    def retrieve_keypair_by_fingerprint(self, fingerprint):
        response = self.keypairapi.get_keypair_by_fingerprint(fingerprint)
        keypair_objects = self._build_keypair_objects_from_response(response)
        return keypair_objects

    def retrieve_keypair_by_tag_keyname(self, tagkeyname):
        response = self.keypairapi.get_keypair_by_tag_keyname(tagkeyname)
        keypair_objects = self._build_keypair_objects_from_response(response)
        return keypair_objects

    def retrieve_keypair_by_tag(self, key, value):
        response = self.keypairapi.get_keypair_by_tag(key, value)
        keypair_objects = self._build_keypair_objects_from_response(response)
        return keypair_objects

    def upload_keypair_rsa(self, name, publickey, tag_dict):
        if self._does_keypair_name_exist(name) == True:
            raise KeyPairNameAlreadyExists(f"Key pair name {name} already exists  ")
        tag_specification = self._build_tag_specification_list(tag_dict)
        print(tag_specification)
        self.keypairapi.import_keypair(name, publickey, tag_specification)
        response = self.retrieve_keypair_by_name(name)
        # print("RESPONSE", response)
        # print(response)
        # keypair_objects = self._build_keypair_objects_from_response(response)
        return response[0]

    def _build_keypair_objects_from_response(self, response):
        keypair_objects = []
        keypairs = response["KeyPairs"]
        for keypair in keypairs:
            tag_objects = []
            if "Tags" in keypair:
                tags = keypair.pop("Tags")
                # print(tags)
                for tag in tags:
                    # print(tag)
                    newtag = Tags(**tag)
                    tag_objects.append(newtag)
            newkeypair = KeyPair()
            newkeypair.attributes = KeyPairAttributes(**keypair)
            newkeypair.tags = tag_objects
            keypair_objects.append(newkeypair)
        return keypair_objects

    def _build_tag_specification_list(self, tag_dict):
        tag_specifications = []
        tag_specification = {}
        tag_specification["ResourceType"] = "key-pair"
        tag_list = []
        for key, value in tag_dict.items():
            tag = {}
            tag["Key"] = key
            tag["Value"] = value

            tag_list.append(tag)
        tag_specification["Tags"] = tag_list
        tag_specifications.append(tag_specification)
        return tag_specifications

    def _does_keypair_name_exist(self, KeyName):
        if len(self.retrieve_keypair_by_name(KeyName)) > 0:
            return True
        else:
            return False


class KeyPair:
    def __init__(self):
        self.keypairapi = KeyPairs()
        self.attributes = KeyPairAttributes()
        self.tags = []

    def delete(self):
        response = self.keypairapi.delete_keypair(self.attributes.KeyName)
        # return response
