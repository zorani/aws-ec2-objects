from __future__ import annotations

import json
import re
import threading
import time
from dataclasses import dataclass
from dataclasses import field

from ..ec2api.images import Images
from ..ec2common.ec2exceptions import *


@dataclass
class ImageAttributes:
    Architecture: str = None
    CreationDate: str = None
    ImageId: str = None
    ImageLocation: str = None
    ImageType: str = None
    Public: bool = None
    KernelId: str = None
    OwnerId: str = None
    Platform: str = None
    PlatformDetails: str = None
    UsageOperation: str = None
    RamdiskId: str = None
    State: str = None
    Description: str = None
    EnaSupport: bool = None
    Hypervisor: str = None
    ImageOwnerAlias: str = None
    Name: str = None
    RootDeviceName: str = None
    RootDeviceType: str = None
    SriovNetSupport: str = None
    VirtualizationType: str = None
    BootMode: str = None
    DepricationTime: str = None
    # ProductCodes: object = None
    ##BlockDeviceMappings: object = None
    # StateReason: object = None
    # Tags: object = None


@dataclass
class BlockDeviceMappingEBS:
    # deviceType: str = None
    DeviceName: str = None
    SnapshotId: str = None
    VolumeSize: str = None
    DeleteOnTermination: bool = None
    VolumeType: str = None
    Encrypted: bool = None


@dataclass
class BlockDeviceMappingVirtual:
    # deviceType: str = None
    DeviceName: str = None
    VirtualName: str = None


class ImageManager:
    def __init__(self):
        self.imageapi = Images()

    def retrieve_all_ubuntu_x86_64_machine_images_hvm_ssd(self, name=""):
        # https://wiki.ubuntu.com/Releases
        # uset the first string of the code name e.g. Focal, Bionic, Trusty
        image_objects = []
        json_results = self.imageapi.list_all_ubuntu_x86_64_machine_images_hvm_ssd(
            name=name
        )
        image_datas = json_results["Images"]
        for image_data in image_datas:
            ebsblockdevices = []
            virtualblockdevices = []
            if "BlockDeviceMappings" in image_data:
                BlockDeviceMappings = image_data.pop("BlockDeviceMappings")
                (
                    ebsblockdevices,
                    virtualblockdevices,
                ) = self._extract_block_device_mapping(BlockDeviceMappings)
            newimage = Image()
            newimage.attributes = ImageAttributes(**image_data)
            newimage.ebsblockdevices = ebsblockdevices
            newimage.virtualblockdevices = virtualblockdevices
            image_objects.append(newimage)
        if len(image_objects) > 1:
            image_objects.sort(key=lambda x: x.attributes.Name, reverse=True)
        return image_objects

    def retrieve_all_ubuntu_arm64_machine_images_hvm_ssd(self, name=""):
        # https://wiki.ubuntu.com/Releases
        # uset the first string of the code name e.g. Focal, Bionic, Trusty
        image_objects = []
        json_results = self.imageapi.list_all_ubuntu_arm64_machine_images_hvm_ssd(
            name=name
        )
        image_datas = json_results["Images"]
        for image_data in image_datas:
            ebsblockdevices = []
            virtualblockdevices = []
            if "BlockDeviceMappings" in image_data:
                BlockDeviceMappings = image_data.pop("BlockDeviceMappings")
                (
                    ebsblockdevices,
                    virtualblockdevices,
                ) = self._extract_block_device_mapping(BlockDeviceMappings)
            newimage = Image()
            newimage.attributes = ImageAttributes(**image_data)
            newimage.ebsblockdevices = ebsblockdevices
            newimage.virtualblockdevices = virtualblockdevices
            image_objects.append(newimage)
        if len(image_objects) > 1:
            image_objects.sort(key=lambda x: x.attributes.Name, reverse=True)
        return image_objects

    def retrieve_image(self, imageId):
        json_results = self.imageapi.retrieve_image(imageId)
        image_datas = json_results["Images"]
        image_data = image_datas[0]
        # print(type(image_data))
        # print(image_data)
        ebsblockdevices = []
        virtualblockdevices = []
        if "BlockDeviceMappings" in image_data:
            BlockDeviceMappings = image_data.pop("BlockDeviceMappings")
            ebsblockdevices, virtualblockdevices = self._extract_block_device_mapping(
                BlockDeviceMappings
            )
        # if "ProductCodes" in image_data:
        #    ProductCodes = image_data.pop("ProductCodes")
        #    print(ProductCodes)
        # if "StateReason" in image_data:
        #    StateReason = image_data.pop("StateReason")
        #    print(StateReason)
        # if "Tags" in image_data:
        #    Tags = image_data.pop("Tags")
        #    print(Tags)
        newimage = Image()
        newimage.attributes = ImageAttributes(**image_data)
        newimage.ebsblockdevices = ebsblockdevices
        newimage.virtualblockdevices = virtualblockdevices
        return newimage

    def _extract_block_device_mapping(self, BlockDeviceMappings):
        ebsblockdevices = []
        virtualblockdevices = []
        for BlockDeviceMapping in BlockDeviceMappings:
            if "Ebs" in BlockDeviceMapping:
                newebsbd = BlockDeviceMappingEBS()
                newebsbd.DeviceName = BlockDeviceMapping["DeviceName"]
                if "SnapshotId" in BlockDeviceMapping["Ebs"]:
                    newebsbd.SnapshotId = BlockDeviceMapping["Ebs"]["SnapshotId"]
                if "DeleteOnTermination" in BlockDeviceMapping["Ebs"]:
                    newebsbd.DeleteOnTermination = BlockDeviceMapping["Ebs"][
                        "DeleteOnTermination"
                    ]
                if "VolumeSize" in BlockDeviceMapping["Ebs"]:
                    newebsbd.VolumeSize = BlockDeviceMapping["Ebs"]["VolumeSize"]
                if "VolumeType" in BlockDeviceMapping["Ebs"]:
                    newebsbd.VolumeType = BlockDeviceMapping["Ebs"]["VolumeType"]
                if "Encrypted" in BlockDeviceMapping["Ebs"]:
                    newebsbd.Encrypted = BlockDeviceMapping["Ebs"]["Encrypted"]
                ebsblockdevices.append(newebsbd)
            if "VirtualName" in BlockDeviceMapping:
                newvirtual = BlockDeviceMappingVirtual()
                newvirtual.DeviceName = BlockDeviceMapping["DeviceName"]
                newvirtual.VirtualName = BlockDeviceMapping["VirtualName"]
                virtualblockdevices.append(newvirtual)
        return ebsblockdevices, virtualblockdevices


class Image:
    def __init__(self):
        self.attributes = ImageAttributes()
        self.ebsblockdevices = []
        self.virtualblockdevices = []
