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
        region = newinstance.attributes.Placement["AvailabilityZone"][0:-1]
        # ["Placement"]["AvailabilityZone"][0:-1]
        newinstance.region = region

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

    # Might want to check status of machines... e.g. if a machine is terminated you can't restart it.

    def __init__(self):
        self.instanceapi = Instances()
        self.attributes = InstanceAttributes()
        self.region = None

    def start(self):
        self.instance_checks()
        if (self.instance_state() == "pending") or (self.instance_state() == "running"):
            return
        newInstanceId = self.instanceapi.start_instance(
            self.attributes.InstanceId, self.region
        )
        self.attributes.InstanceId = newInstanceId
        self.update_instance_state()

    def stop(self):
        self.instance_checks()
        if (self.instance_state() == "stopping") or (
            self.instance_state() == "stopped"
        ):
            return
        self.instanceapi.stop_instance(self.attributes.InstanceId, self.region)
        self.update_instance_state()

    def delete(self):
        self.instance_checks()
        if self.instance_state() == "terminated":
            return
        # According to https://github.com/boto/boto3/issues/176 sometimes you need to stop the instance first
        # to avoid issues.
        self.stop()
        self.instanceapi.terminate_instance(self.attributes.InstanceId, self.region)
        # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html
        # By default, Amazon EBS root device volumes are automatically deleted when the instance terminates.
        # However, by default, any additional EBS volumes that you attach at launch, or any EBS volumes that
        # you attach to an existing instance persist even after the instance terminates. This behavior is
        # controlled by the volume's DeleteOnTermination attribute, which you can modify.

    def reboot(self):
        self.instance_checks()
        self.instanceapi.reboot_instance(self.attributes.InstanceId, self.region)
        pass

    def instance_checks(self):
        self.does_instance_exist()
        self.update_instance_state()

    def update_instance_state(self):
        # First we ask boto3 to update the attributes of the instance
        self.instanceapi.reload_instance(self.attributes.InstanceId, self.region)
        # Then we get the latest info and update the attributes.
        updated_attributes = self.instanceapi.latest_instance_info(
            self.attributes.InstanceId, self.region
        )
        self.attributes = InstanceAttributes(**updated_attributes)

    def instance_state(self):
        # Will return one of these values.
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.state
        # 0 : pending
        # 16 : running
        # 32 : shutting-down
        # 48 : terminated
        # 64 : stopping
        # 80 : stopped
        self.update_instance_state()
        state: dict
        state = self.attributes.State
        return state["Name"]

    def does_instance_exist(self):
        if self.attributes.InstanceId in self.instanceapi.list_instances(self.region):
            if self.instance_state() == "terminated":
                raise EC2InstanceNolongerExists(
                    f"{self.attributes.InstanceId} no longer exists."
                )
            return True
        else:
            return False
