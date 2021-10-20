from __future__ import annotations

from dataclasses import dataclass, field
from ..ec2api.instances import Instances

from ..ec2common.ec2exceptions import *

import json
import threading
import time
import re


@dataclass
class InstanceAttributes:
    AmiLaunchIndex: int = None
    ImageId: str = None
    InstanceId: str = None
    InstanceType: str = None
    KeyName: str = None
    LaunchTime: str = None
    Monitoring: object = field(default_factory=list)
    Placement: object = field(default_factory=list)
    PrivateDnsName: str = None
    PrivateIpAddress: str = None
    ProductCodes: list = field(default_factory=list)
    PublicDnsName: str = None
    State: object = field(default_factory=list)
    StateTransitionReason: str = None
    SubnetId: str = None
    VpcId: str = None
    Architecture: str = None
    BlockDeviceMappings: object = field(default_factory=list)
    ClientToken: str = None
    EbsOptimized: bool = None
    EnaSupport: bool = None
    Hypervisor: str = None
    NetworkInterfaces: object = field(default_factory=list)
    RootDeviceName: str = None
    RootDeviceType: str = None
    SecurityGroups: object = field(default_factory=list)
    SourceDestCheck: bool = None
    StateReason: object = None
    VirtualizationType: str = None
    CpuOptions: object = None
    CapacityReservationSpecification: object = None
    MetadataOptions: object = None
    EnclaveOptions: object = None
    BootMode: str = None
    ElasticGpuAssociations: object = field(default_factory=list)
    ElasticInferenceAcceleratorAssociations: object = field(default_factory=list)
    HybernationOptions: object = None
    IamInstanceProfile: object = None
    InstanceLifecycle: str = None
    KernelId: str = None
    Licenses: object = field(default_factory=list)
    NetworkInterfacesAttribute: object = field(default_factory=list)
    OutpostArn: str = None
    Platform: str = None
    PlatformDetails: str = None
    PublicIpAddress: str = None
    RamdiskId: str = None
    SpotInstanceRequestId: str = None
    SriovNetSupport: str = None
    Tags: object = field(default_factory=list)
    UsageOperation: str = None
    UsageOperationUpdateTime: str = None
    HibernationOptions: object = None


class InstanceManager:
    def __init__(self):
        self.instanceapi = Instances()

    def create_instance(
        self, image_id, instance_type, ssh_key_name, tag_dict=None, arg_region=None
    ):
        if tag_dict != None:
            tag_specification = self._build_tag_specification_list(tag_dict)
        else:
            tag_specification = []
            # print(tag_specification)
        instanceinfo = self.instanceapi.create_instance(
            image_id,
            instance_type,
            ssh_key_name,
            tag_specification=tag_specification,
            arg_region=arg_region,
        )

        instanceinfo_instance = instanceinfo["Reservations"][0]["Instances"][0]

        newinstance = Instance()
        newinstance.attributes = InstanceAttributes(**instanceinfo_instance)

        return newinstance

    def _build_tag_specification_list(self, tag_dict):
        tag_specifications = []
        tag_specification = {}
        tag_specification["ResourceType"] = "instance"
        tag_list = []
        for key, value in tag_dict.items():
            tag = {}
            tag["Key"] = key
            tag["Value"] = value

            tag_list.append(tag)
        tag_specification["Tags"] = tag_list
        tag_specifications.append(tag_specification)

        return tag_specifications


class Instance:
    def __init__(self):
        self.instanceapi = Instances()
        self.attributes = InstanceAttributes()
