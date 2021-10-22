from __future__ import annotations

from dataclasses import dataclass, field

from ..ec2common.ec2exceptions import *


@dataclass
class NetworkInterfaceAttributes:
    Association: object = None
    Attachment: object = None
    Description: str = None
    Groups: object = field(default_factory=list)
    Ipv6Addresses: object = field(default_factory=list)
    MacAddress: str = None
    NetworkInterfaceId: str = None
    OwnerId: str = None
    PrivateDnsName: str = None
    PrivateIpAddress: str = None
    PrivateIpAddresses: object = field(default_factory=list)
    SourceDestCheck: bool = None
    Status: str = None
    SubnetId: str = None
    VpcId: str = None
    InterfaceType: str = None
    Ipv4Prefixes: object = field(default_factory=list)
    Ipv6Prefixes: object = field(default_factory=list)


class NetworkInterfaceManager:
    def __init__(self):
        pass


#    def dict_to_networkinterface(self, dict):
#        new_networkinterface = NetworkInterface()
#        new_networkinterface.attributes = NetworkInterfaceAttributes(**dict)
#        return new_networkinterface

#    def dict_list_to_networkinterface_list(self, dict_list):
#        networkinterface_list = []
#        for dict_item in dict_list:
#            networkinterface_list.append(self.dict_to_networkinterface(dict_item))
#        return networkinterface_list


class NetworkInterface:
    def __init__(self):
        self.attributes = NetworkInterfaceAttributes()
