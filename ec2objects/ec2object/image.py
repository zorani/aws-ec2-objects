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
    imageId: str = None
    imageLocation: str = None
    imageState: str = None
    imageOwnerId: str = None
    creationDate: str = None
    isPublic: str = None
    architecture: str = None
    imageType: str = None
    imageOwnerAlias: str = None
    rootDeviceType: str = None
    # blockDeviceMapping: str = None
    virtualizationType: str = None
    hypervisor: str = None
    platformDetails: str = None
    usageOperation: str = None


@dataclass
class BlockDeviceMappingEBS:
    # deviceType: str = None
    deviceName: str = None
    snapshotId: str = None
    volumeSize: str = None
    deleteOnTermination: bool = None
    volumeType: str = None
    encrypted: bool = None


@dataclass
class BlockDeviceMappingVirtual:
    # deviceType: str = None
    deviceName: str = None
    virtualName: str = None


class ImageManager:
    def __init__(self):
        self.imageapi = Images()

    def retrieve_all_images(self):
        image_objects = []
        response = self.imageapi.list_all_public_images()
        if response:
            content = json.loads(response.content.decode("utf-8"))
            image_datas = content["images"]
            for image_data in image_datas:
                blockDeviceMapping = image_data.pop("blockDeviceMapping")
                ebs_devices = []
                virtual_devices = []
                for ebs_device in blockDeviceMapping["ebs"]:
                    new_ebs_device = BlockDeviceMappingEBS(**ebs_device)
                    ebs_devices.append(new_ebs_device)
                for virtual_device in blockDeviceMapping["virtual"]:
                    new_virtual_device = BlockDeviceMappingVirtual(**virtual_device)
                    virtual_devices.append(new_virtual_device)
                newimage = Image()
                newimage.attributes = ImageAttributes(**image_data)
                if len(ebs_devices) > 0:
                    newimage.ebsblockdevices = ebs_devices
                else:
                    newimage.ebsblockdevices = []
                if len(virtual_devices) > 0:
                    newimage.virtualblockdevices = virtual_devices
                else:
                    newimage.virtualblockdevices = []

                image_objects.append(newimage)
            return image_objects

    def retrieve_image(self, imageId):
        response = self.imageapi.retrieve_image(imageId)
        if response:
            content = json.loads(response.content.decode("utf-8"))
            image_datas = content["images"]
            image_data = image_datas[0]
            blockDeviceMapping = image_data.pop("blockDeviceMapping")
            ebs_devices = []
            virtual_devices = []
            for ebs_device in blockDeviceMapping["ebs"]:
                new_ebs_device = BlockDeviceMappingEBS(**ebs_device)
                ebs_devices.append(new_ebs_device)
            for virtual_device in blockDeviceMapping["virtual"]:
                new_virtual_device = BlockDeviceMappingVirtual(**virtual_device)
                virtual_devices.append(new_virtual_device)
            # print(type(image_data))
            newimage = Image()
            newimage.attributes = ImageAttributes(**image_data)
            if len(ebs_devices) > 0:
                newimage.ebsblockdevices = ebs_devices
            if len(virtual_devices) > 0:
                newimage.virtualblockdevices = virtual_devices
            return newimage


class Image:
    def __init__(self):
        self.attributes = ImageAttributes()
        self.ebsblockdevices = None
        self.virtualblockdevices = None
