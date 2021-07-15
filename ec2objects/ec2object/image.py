from __future__ import annotations

from dataclasses import dataclass, field
from ..ec2api.images import Images

from ..ec2common.ec2exceptions import *

import json
import threading
import time
import re

# <item>\n
# <imageId>ari-e6bc478f</imageId>\n
# <imageLocation>ec2-paid-ibm-was-us-east-1/initrd-2.6.16.60-0.30-xen.x86_64.manifest.xml</imageLocation>\n
# <imageState>available</imageState>\n
# <imageOwnerId>470254534024</imageOwnerId>\n
# <creationDate>2011-06-24T20:34:25.000Z</creationDate>\n
# <isPublic>true</isPublic>\n
# <architecture>x86_64</architecture>\n
# <imageType>ramdisk</imageType>\n
# <imageOwnerAlias>amazon</imageOwnerAlias>\n
# <rootDeviceType>instance-store</rootDeviceType>\n
# <blockDeviceMapping/>\n
# <virtualizationType>paravirtual</virtualizationType>\n
# <hypervisor>xen</hypervisor>\n
# <platformDetails>Linux/UNIX</platformDetails>\n
# <usageOperation>RunInstances</usageOperation>\n
# </item>\n


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

    def retrieve_all_amazon_public_images(self):
        image_objects = []
        json_results = self.imageapi.list_all_amazon_public_images()
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
            # if "ProductCodes" in image_data:
            #    ProductCodes = image_data.pop("ProductCodes")
            # if "StateReason" in image_data:
            #    StateReason = image_data.pop("StateReason")
            # if "Tags" in image_data:
            #    Tags = image_data.pop("Tags")
            newimage = Image()
            newimage.attributes = ImageAttributes(**image_data)
            newimage.ebsblockdevices = ebsblockdevices
            newimage.virtualblockdevices = virtualblockdevices
            image_objects.append(newimage)
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
