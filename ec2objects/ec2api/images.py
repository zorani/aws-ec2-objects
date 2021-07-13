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

import xml.etree.ElementTree as ET
from io import BytesIO

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


class Images(EC2ApiConnection):
    def __init__(self):
        EC2ApiConnection.__init__(self)

    def list_all_public_images(self):
        # "us-east-1"
        params = {}
        # This gets a lot of data, need to wait a while... setting timeout to 120sec
        params["Action"] = "DescribeImages"
        params["Region"] = self.default_region
        params["Owner.1"] = "amazon"
        # params["ImageId.1"] = "ami-058b1b7fe545997ae"
        params["Filter.1.Name"] = "is-public"
        params["Filter.1.Value.1"] = "true"
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

    def retrieve_image(self, imageId):
        params = {}
        # This gets a lot of data, need to wait a while... setting timeout to 120sec
        params["Action"] = "DescribeImages"
        params["Region"] = self.default_region
        params["ImageId.1"] = imageId
        response = self.get_request(params=params)
        if response:
            old_content = response.content
            # print(old_content)
            old_content_byte_encoded = BytesIO(old_content)
            tree = ET.parse(old_content_byte_encoded)
            root = tree.getroot()
            imageSet = ET.tostring(root[1][0])
            response._content = self.xml_to_json_response(imageSet)
        # print(response.content)
        return response

    def xml_to_json_response(self, imageSet):
        # old_content = response.content
        # print(old_content)
        # old_content_byte_encoded = BytesIO(old_content)
        # tree = ET.parse(old_content_byte_encoded)
        # root = tree.getroot()
        # imageSet = ET.tostring(root[1])
        # print(imageSet)
        context = ET.iterparse(BytesIO(imageSet), events=("end",))
        image_info_list = []
        n = 0
        for event, elem in context:
            # print(elem)
            if elem.tag == "{http://ec2.amazonaws.com/doc/2016-11-15/}item":
                # print(elem.tag)
                if n % 1000 == 0:
                    print(n)
                n = n + 1
                xml_content = BeautifulSoup(ET.tostring(elem), "xml")
                imageId = xml_content.findAll("imageId")
                imageLocation = xml_content.findAll("imageLocation")
                imageState = xml_content.findAll("imageState")
                imageOwnerId = xml_content.findAll("imageOwnerId")
                creationDate = xml_content.findAll("creationDate")
                isPublic = xml_content.findAll("isPublic")
                architecture = xml_content.findAll("architecture")
                imageType = xml_content.findAll("imageType")
                imageOwnerAlias = xml_content.findAll("imageOwnerAlias")
                rootDeviceType = xml_content.findAll("rootDeviceType")
                blockDeviceMapping = xml_content.findAll("blockDeviceMapping")
                virtualizationType = xml_content.findAll("virtualizationType")
                hypervisor = xml_content.findAll("hypervisor")
                platformDetails = xml_content.findAll("platformDetails")
                usageOperation = xml_content.findAll("usageOperation")
                image_info = {}
                if len(imageId) > 0:
                    if len(imageId) > 0:
                        # print(imageId[0].get_text())
                        image_info["imageId"] = imageId[0].get_text()
                    else:
                        image_info["imageId"] = None

                    if len(imageLocation) > 0:
                        image_info["imageLocation"] = imageLocation[0].get_text()
                    else:
                        image_info["imageLocation"] = None

                    if len(imageState) > 0:
                        image_info["imageState"] = imageState[0].get_text()
                    else:
                        image_info["imageState"] = None

                    if len(imageOwnerId) > 0:
                        image_info["imageOwnerId"] = imageOwnerId[0].get_text()
                    else:
                        image_info["imageOwnerId"] = None

                    if len(creationDate) > 0:
                        image_info["creationDate"] = creationDate[0].get_text()
                    else:
                        image_info["creationDate"] = None

                    if len(isPublic) > 0:
                        image_info["isPublic"] = isPublic[0].get_text()
                    else:
                        image_info["isPublic"] = None

                    if len(architecture) > 0:
                        image_info["architecture"] = architecture[0].get_text()
                    else:
                        image_info["architecture"] = None

                    if len(imageType) > 0:
                        image_info["imageType"] = imageType[0].get_text()
                    else:
                        image_info["imageType"] = None

                    if len(imageOwnerAlias) > 0:
                        image_info["imageOwnerAlias"] = imageOwnerAlias[0].get_text()
                    else:
                        image_info["imageOwnerAlias"] = None

                    if len(rootDeviceType) > 0:
                        image_info["rootDeviceType"] = rootDeviceType[0].get_text()
                    else:
                        image_info["rootDeviceType"] = None

                    if len(blockDeviceMapping) > 0:
                        gt_blockDeviceMapping = blockDeviceMapping[0]
                        image_info["blockDeviceMapping"] = self.block_device_mapping(
                            gt_blockDeviceMapping
                        )
                    else:
                        block_device_mapping = {}
                        block_device_mapping["ebs"] = []
                        block_device_mapping["virtual"] = []

                        image_info["blockDeviceMapping"] = block_device_mapping

                    if len(virtualizationType) > 0:
                        image_info["virtualizationType"] = virtualizationType[
                            0
                        ].get_text()
                    else:
                        image_info["virtualizationType"] = None

                    if len(hypervisor) > 0:
                        image_info["hypervisor"] = hypervisor[0].get_text()
                    else:
                        image_info["hypervisor"] = None

                    if len(platformDetails) > 0:
                        image_info["platformDetails"] = platformDetails[0].get_text()
                    else:
                        image_info["platformDetails"] = None

                    if len(usageOperation) > 0:
                        image_info["usageOperation"] = usageOperation[0].get_text()
                    else:
                        image_info["usageOperation"] = None

                    image_info_list.append(image_info)
        return_dict = {}
        return_dict["images"] = image_info_list
        new_content = json.dumps(return_dict).encode("utf-8")
        return new_content

    # def xml_to_json_response(self, response):
    #    old_contect = response.content
    #    xml_content = BeautifulSoup(old_contect, "xml")
    #    imageId = xml_content.findAll("imageId")
    #    imageLocation = xml_content.findAll("imageLocation")
    #    imageState = xml_content.findAll("imageState")
    #    imageOwnerId = xml_content.findAll("imageOwnerId")
    #    creationDate = xml_content.findAll("creationDate")
    #    isPublic = xml_content.findAll("isPublic")
    #    architecture = xml_content.findAll("architecture")
    #    imageType = xml_content.findAll("imageType")
    #    imageOwnerAlias = xml_content.findAll("imageOwnerAlias")
    #    rootDeviceType = xml_content.findAll("rootDeviceType")
    #    blockDeviceMapping = xml_content.findAll("blockDeviceMapping")
    #    virtualizationType = xml_content.findAll("virtualizationType")
    #    hypervisor = xml_content.findAll("hypervisor")
    #    platformDetails = xml_content.findAll("platformDetails")
    #    usageOperation = xml_content.findAll("usageOperation")
    #    ##add the rest
    #    image_info_list = []
    #    for i in range(0, len(imageId)):
    #        image_info = {}
    #        image_info["imageId"] = imageId[i].get_text()
    #        image_info["imageLocation"] = imageLocation[i].get_text()
    #        image_info["imageState"] = imageState[i].get_text()
    #        image_info["imageOwnerId"] = imageOwnerId[i].get_text()
    #        image_info["creationDate"] = creationDate[i].get_text()
    #        image_info["isPublic"] = isPublic[i].get_text()
    #        image_info["architecture"] = architecture[i].get_text()
    #        image_info["imageType"] = imageType[i].get_text()
    #        image_info["imageOwnerAlias"] = imageOwnerAlias[i].get_text()
    #        image_info["rootDeviceType"] = rootDeviceType[i].get_text()
    #        gt_blockDeviceMapping = blockDeviceMapping[i]
    #        image_info["blockDeviceMapping"] = self.block_device_mapping(
    #            gt_blockDeviceMapping
    #        )
    #        image_info["virtualizationType"] = virtualizationType[i].get_text()
    #        image_info["hypervisor"] = hypervisor[i].get_text()
    #        image_info["platformDetails"] = platformDetails[i].get_text()
    #        image_info["usageOperation"] = usageOperation[i].get_text()
    #        image_info_list.append(image_info)
    #    return_dict = {}
    #    return_dict["images"] = image_info_list
    #    response._content = json.dumps(return_dict).encode("utf-8")
    #    return response

    def block_device_mapping(self, blockdevice_xml):
        block_device_mapping = {}
        blockdevice_xml_str = str(blockdevice_xml)
        ebs_blockmappings_json = []
        virtual_blockmappings_json = []
        ebs_blockmappings_to_process = set()
        virtual_blockmappings_to_process = set()
        xml_content_soup = BeautifulSoup(str(blockdevice_xml_str), "xml")
        # BUILD EBS BLOCK MAPPINGS
        xml_content_soup_ebs = xml_content_soup.findAll("ebs")
        for item in xml_content_soup_ebs:
            ebs_blockmappings_to_process.add(item.parent)
        # print(ebs_blockmappings_to_process)
        if len(ebs_blockmappings_to_process) > 0:
            for item in ebs_blockmappings_to_process:
                new_ebs_blockmapping = {}
                deviceName = item.deviceName.get_text()
                new_ebs_blockmapping["deviceName"] = deviceName
                ebs_volumes_list = []
                for ebs_item in item.findAll("ebs"):
                    # print(ebs_item)
                    # ebs_item_json = {}
                    try:
                        new_ebs_blockmapping[
                            "snapshotId"
                        ] = ebs_item.snapshotId.get_text()
                    except:
                        new_ebs_blockmapping["snapshotId"] = "NOT FOUND"
                    new_ebs_blockmapping["volumeSize"] = ebs_item.volumeSize.get_text()
                    new_ebs_blockmapping[
                        "deleteOnTermination"
                    ] = ebs_item.deleteOnTermination.get_text()
                    new_ebs_blockmapping["volumeType"] = ebs_item.volumeType.get_text()
                    new_ebs_blockmapping["encrypted"] = ebs_item.encrypted.get_text()
                #    ebs_volumes_list.append(ebs_item_json)
                # new_ebs_blockmapping["ebslist"] = ebs_volumes_list
                ebs_blockmappings_json.append(new_ebs_blockmapping)
        # print(ebs_blockmappings_json)
        # BUILD EBS VIRTUAL MAPPINGS
        xml_content_soup_virtual = xml_content_soup.findAll("virtualName")
        for item in xml_content_soup_virtual:
            virtual_blockmappings_to_process.add(item.parent)
        # print(virtual_blockmappings_to_process)
        for item in virtual_blockmappings_to_process:
            new_virtual_blockmapping = {}
            new_virtual_blockmapping["deviceName"] = item.deviceName.get_text()
            new_virtual_blockmapping["virtualName"] = item.virtualName.get_text()
            virtual_blockmappings_json.append(new_virtual_blockmapping)
        # print(virtual_blockmappings_json)
        block_device_mapping["ebs"] = ebs_blockmappings_json
        block_device_mapping["virtual"] = virtual_blockmappings_json
        return block_device_mapping
