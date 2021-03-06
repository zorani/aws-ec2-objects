from .ec2common.ec2exceptions import ParamNotFound as ParamNotFound
from .ec2common.ec2exceptions import RequestType as RequestType
from .ec2object.region import RegionManager as RegionManager
from .ec2object.region import Region as Region
from .ec2object.image import ImageManager as ImageManager
from .ec2object.image import Image as Image
from .ec2object.keypair import KeyPairManager as KeyPairManager
from .ec2object.keypair import KeyPair as KeyPair
from .ec2object.instance import InstanceManager as InstanceManager
from .ec2object.instance import Instance as Instance
from .ec2object.networkinterface import (
    NetworkInterfaceManager as NetworkInterfaceManager,
)
from .ec2object.networkinterface import NetworkInterface as NetworkInterface
from .ec2object.vpc import VPCManager as VPCManager
from .ec2object.vpc import VPC as VPC

###API TESTS####DELETE
# from .ec2api.images import Images as Images
################
