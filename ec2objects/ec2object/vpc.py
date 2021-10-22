from __future__ import annotations

from dataclasses import dataclass, field
from ..ec2api.vpcs import VPCs

from ..ec2common.ec2exceptions import *

# See vpc notes at the end of this file.


@dataclass
class VPCAttributes:
    CidrBlock: str = None
    DhcpOptionsId: str = None
    State: str = None
    VpcId: str = None
    OwnerId: str = None
    InstanceTenancy: str = None
    # Tenancy defines how EC2 instances are distributed across physical hardware
    # and affects pricing. There are three tenancy options available:
    # - Shared (default) — Multiple AWS accounts may share the same physical hardware.
    # - Dedicated Instance (dedicated) — Your instance runs on single-tenant hardware.
    # - Dedicated Host (host) — Your instance runs on a physical server with EC2 instance capacity fully dedicated to your use, an isolated server with configurations that you can control.
    Ipv6CidrBlockAssociationSet: object = field(default_factory=list)
    CidrBlockAssociationSet: object = field(default_factory=list)
    IsDefault: bool = None
    Tags: object = field(default_factory=list)


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_vpc
class VPCManager:
    def __init__(self):
        self.vpcapi = VPCs()

    def create_vpc(self, CidrBlock: str, arg_region):
        vpcattributes = self.vpcapi.create_vpc_IPV4(
            CidrBlock=CidrBlock, arg_region=arg_region
        )
        newvpc = VPC()
        newvpc.attributes = VPCAttributes(**vpcattributes)

        return newvpc


class VPC:
    def __init__(self):
        self.attributes = VPCAttributes()
        self.region = None


# VPC quick notes.
# https://www.youtube.com/watch?v=z07HTSzzp3o
# https://www.youtube.com/watch?v=bGDMeD6kOz0
#
# Available Private IPv4 IP addresses
# According to rfc1918  with CIDR notation.
#
# class C) 192.168.0.0/16
# class B) 172.16.0.0/12
# class A) 10.0.0.0/8
#
# https://www.freecodecamp.org/news/subnet-cheat-sheet-24-subnet-mask-30-26-27-29-and-other-ip-address-cidr-network-references/
#
#
#
# So according to the rfc1918 you should only stick to the above 3 blocks of IPs
# for your private networks.
#
# Amazon guide: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-subnet-basics
#
# Class A VPC must be /16 or smaller.
# Class B VPC must be /16 or smaller.
# Class C VPC must be /16 or smaller.

# /28 is the smalles netmask allowed by amazon.
# from the cheat sheet, /28 is 16 IP addresses.
#                       /16 is 65536 IP addresses.

# SUBNETTING

# OK.... lets say we create an amazon class A VPC with 65,536 IP addresses
# 10.0.0.0/16
#
# We have 65,536 IP addresses that we can subnet.
#
# First of all   /16 blocks the first 16 bytes of an IP address
# Decimal Version: 255.255.0.0
# Binary  Version: 11111111.11111111.00000000.00000000
#
# Which leaves:
#   Decimal:
# 0.0.255.255 to play with, thats...
# 256*256 = 65,536 (including the 0) available IP addresses for your VPC
# and to be slices up in subnets.
#
#   Binary:
# 0.0.11111111.11111111

# SUBNET MASK

# So viewed in binary it's easier to understand what a subnet mask is.
# 11111111.11111111.00000000.00000000  is a mask for our example.
# the first 11111111.11111111 just block out the area, not allowed to use.
# It's our network.
# Remember our network is class A so the first 16 bits under the mask is
# 00001010.00000000 = 10.0.

# the last 00000000.00000000 is called the 'wildcard mask', we can create
# as many combination of these binary numbers to create a complete IP on the
# network.

# e.g.  00000010.00000001 = 2.1
# which is 11111111.11111111.00000010.00000001 = 255.255.2.1

# but our example is a class A network, the first 16 bytes are actually
# 00001010.00000000 = 10.0.
# so our internal IP address is actually 10.0.2.1 for our example.

# Our range of available IPs for our private devices is.
# Start:
# 00001010.00000000.00000000.00000000 = 10.0.0.0
# End:
# 00001010.00000000.11111111.11111111 = 10.0.255.255

# So, whats a subnet?
# You can slice up the above private IP addresses in the PVC in to
# subnetworks.  The slice sizes depend upon, and are contrained, by BINARY maths
# and also the imposed limit by amazon which is VPCs 16 or smaller as noted above.
#
# Okay, let do some subnetting.
#
# Our VPC: 10.0.0.0/16    with 65,534 IP Addresses
# Start: 00001010.00000000.00000000.00000000 = 10.0.0.0
# End: 00001010.00000000.11111111.11111111 = 10.0.255.255
#
# let make subnet of the smallest allowed size = 16 IP addresses, which is CIDR=/28
# 00001010.00000000.00000000.0000*0000    < 32-28 = 4
# The last 4 bits of the subnet must be kept zero, these represent the ip addresses
# that will be assigned to the computers in your subnet.
# How many IP addresses? 2^4= 16.  Easy.
# So each subnet will have 16 IP addresses.
#
# And our binary restrictions are as follows, we can only define our subnet slices
# using the 0 below.
#
# XXXXXXXX.XXXXXXXX.00000000.0000XXXX
#
# So,
# XXXXXXXX.XXXXXXXX.00000001.0000XXXX is a valid subnet mask
# XXXXXXXX.XXXXXXXX.00000010.0000XXXX is a valid subnet mask
# XXXXXXXX.XXXXXXXX.11111111.0000XXXX is a valid subnet mask
#
# So we have the following valid subnets in CIDR format.
# 10.0.0.0/28
# 10.0.1.0/28
#     ...
# 10.0.255.0/28
#
# Wait there is more. We can also use those other zeros too.
#
# XXXXXXXX.XXXXXXXX.00000000.0001XXXX is a valid subnet mask
# XXXXXXXX.XXXXXXXX.00000000.0010XXXX is a valid subnet mask
# XXXXXXXX.XXXXXXXX.00000000.0010XXXX is a valid subnet mask
#
# So we also have the following subnets available,
#
# 10.0.0.0/28
# 10.0.0.16/28
# 10.0.0.32/28
# 10.0.0.48/28
# 10.0.0.240/28
#
# and you can mix n match these digits so the following are valid subnets too....
#
# 10.0.1.16/28
# 10.0.1.32/28
# 10.0.1.48/28
# 10.0.2.16/28
#
# Each of these has space for 16 IP addresses.
#
#  So subnetting... easy but tricky.


# INTERNET GATEWAY  private to public(outside world)
# SECURITY GROUPS applied on per instance level, assined to vpc.
# Network Access Control List  (NACL), subnet level - which traffic can enter subnet.
# ROUTING TABLE... route traffic differently, and assign public IP addresses.
# NAT GATEWAY ... Translates internal ips to public ones.
