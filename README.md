<h1 align="center">ec2 objects (pip3 install ec2objects)</h1>
<p align="left"><b>everyone:</b> I wish, for once, to just have a simple object oriented experience with the api.</p>
<p align="left"><b>ec2objects:</b> </p>

<p align="center">
<a href="https://github.com/zorani/aws-ec2-objects"><img src="https://img.shields.io/github/forks/zorani/aws-ec2-objects.svg?style=social&label=Fork"></a>
<a href="https://github.com/zorani/aws-ec2-objects"><img src="https://img.shields.io/github/stars/zorani/aws-ec2-objects.svg?style=social&label=Star"></a>
<a href="https://github.com/zorani/aws-ec2-objects"><img src="https://img.shields.io/github/watchers/zorani/aws-ec2-objects.svg?style=social&label=Watch"></a>
</p>

Please visit <a href="https://github.com/zorani/aws-ec2-objects">GitHub</a> page for documentation that has navigation that works.

# Table of Contents

- [How to install](#how-to-install)
- [Configurations](#configurations)
- [Regions](#regions)
	- [Region Manager](#region-manager)
		- [Retrieve All Regions](#retrieve-all-regions)
		- [Retrieve Regions Enabled For Your Account](#retrieve-regions-enabled-for-your-account)
	- [Region Object](#region-object)
- [Images](#images)
	- [Image Manager](#image-manager)
		- [Retrieve Image By ImageId](#retrieve-image-by-imageid)
		- [Retrieve Ubuntu Images](#retrieve-ubuntu-images)
	- [Image Object](#image-object)
- [SSH Key Pairs](#ssh-key-pairs)
   - [KeyPair Manager](#keypair-manager)
	   - [Retrieve Keypairs](#retrieve-keypairs)
	   - [Retrieve Keypair By Name](#retrieve-keypair-by-name)
	   - [Retrieve Keypair By ID](#retrieve-keypair-by-id)
	   - [Retrieve Keypair By Fingerprint](#retrieve-keypair-by-fingerpring)
	   - [Retrieve Keypairs By Tag Keyname](#retrieve-keypairs-by-tag-keyname)
	   - [Retrieve Keypairs By Tag](#retrieve-keypairs-by-tag)
	   - [Upload Keypair RSA](#upload-keypair-rsa)
	- [KeyPair Object](#keypair-object)
	  - [Delete Keypair](#delete-keypair)
# How to install

Here are your options.

## Install from pypi repository

The most popular way is to install the latest package available on pypi.

You can install ec2objects using **pip3**

    pip3 install -U ec2objects

You can uninstall if you like using,

    pip3 uninstall ec2objects

## Install from the cloned git hub repo

There are a few ways to install this python package from a clone of its github repo.
Check out a copy and try the following...

### Build a .tar.gz install package

From the root of the repo build a repo, and check the repo.

    python3 setup.py sdist
    twine check dist/*

Check the newly created dist directory for newly created .tar.gz files.
This is your .tar.gz package and you can install using...

    pip3 install ./dist/ec2objects-0.0.17.tar.gz

You can still uninstall using the same commands,

    pip3 uninstall ec2objects

### Install using the setup.py file

!WARNING! Install does not track which files, and where they are placed.
So, you need to keep a record of there python3 does this.

This is how... from the github repo root directory.

    sudo python3 setup.py install --record files.txt

You can uninstall using by playing back that files.txt file,

    sudo xargs rm -rf < files.txt

### Local interactive install

Using this method you can modify this packages code and have changes immediately available.
Perfect for if you want to tinker with the library, poke around and contribute to the project.

From the cloned repository root directory.

    pip3 install -e ./

You can uninstall using the usual command,

    pip3 uninstall ec2objects

**[⬆ back to top](#table-of-contents)**

# Configurations
## BOTO 3
ec2objects uses [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) to interact with the amazon api.
Decided to go with boto3 as it gives nice json responses instead of the xml mess direct interaction with the api gives.

You can find further token requirements and details at the above link.

Here is are the quick start requirements for ec2objects.

## Token: Required

Set the AWS_ACCESS_KEY_ID, and the AWS_SECRET_ACCESS_KEY environment variables with your amazon aws access credentials.

    export AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    export AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

## Default Region: Required


Please set the AWS_DEFAULT_REGION environment variable to a region you know you  have enabled for your credentials.

For example:

    export AWS_DEFAULT_REGION='us-east-1'

For relevant commands you can specify a completely different region if you need to act on a different region.

**[⬆ back to top](#table-of-contents)**


# Regions


An [AWS Region](https://docs.aws.amazon.com/general/latest/gr/rande.html#region-names-codes) is a collection of AWS resources in a geographic area. 

Each AWS Region is isolated and independent of the other Regions. 

Regions provide fault tolerance, stability, and resilience, and can also reduce latency. They enable you to create redundant resources that remain available and unaffected by a Regional outage.

Import the ec2object Region and RegionManger to interact with Regions.

```python
from ec2objects import Region, RegionManager
```
## Region Manager

Create a region manager.
```python
region_manager = RegionManager()
```
### Retrieve All Regions
Retrieve a list of region objects.
```python
list_of_all_region_objects = region_manager.retrieve_all_regions()
```

### Retrieve Regions Enabled For Your Account
Retrieve a list of region objects enabled for your account.
```python
list_of_enabled_region_objects = region_manager.retrieve_regions_enabled_for_my_account()
```

## Region Object

Region objects contains an attributes data class with the standard ec2 [region attributes](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_Region.html).

Region objects also contain a list of availability zones data classes for that region.

```python
class Region:
    def __init__(self):
        self.attributes = RegionAttributes()
        self.availabilityzones = []
        ...
```
```python
@dataclass
class RegionAttributes:
    RegionName: str = None
    Endpoint: str = None
    OptInStatus: str = None
```

```python
@dataclass
class AvailabilityZones:
    State: str = None
    OptInStatus: str = None
    Messages: list = field(default_factory=list)
    RegionName: str = None
    ZoneName: str = None
    ZoneId: str = None
    GroupName: str = None
    NetworkBorderGroup: str = None
    ZoneType: str = None
    ParentZoneName: str = None
    ParentZoneId: str = None
```
**[⬆ back to top](#table-of-contents)**

# Images
An Amazon Machine Image ([AMI User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)) provides the information required to launch an instance. 

[AMI BOTO3 API GUIDE](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#image) details at this link.

An AMI includes the following:

-   One or more Amazon Elastic Block Store (Amazon EBS) snapshots, or, for instance-store-backed AMIs, a template for the root volume of the instance (for example, an operating system, an application server, and applications).
    
-   Launch permissions that control which AWS accounts can use the AMI to launch instances.
    
-   A block device mapping that specifies the volumes to attach to the instance when it's launched.

Import the ec2object Image and ImageManger to interact with Regions.
```python
from ec2objects import Image, ImageManager
```
## Image Manager
Create an image manager.
```python
image_manager = ImageManager()
```
### Retrieve Image By ImageId
Retrieve an image object by ImageId.
```python
image_object = image_manager.retrieve_image("ami-fd534b97")
```


### Retrieve Ubuntu Images

Okay, so the AWS documentation is a bit difficult.
Going to break it down and try to extract and common sense.. thanks aws.

The following methods retrieve Ubuntu images that have...

Architechture:'x86_64' or 'arm64'
ImageType:'machine'

hvm-ssd: **Important** What does this mean?
The instance created from this image(an hvm-ssd) will have small root storage,
/dev/sda1, to hold the OS.
/dev/sda1 is ephemeral storage is the **volatile temporary storage attached to your instances** which is only present during the running lifetime of the instance. Data will be available on restart but will be destroyed on instance termination.

For longer term data storage you do need to attach an existing Elastic Block Storage (EBS) device for or create and attach new EBS and attach that.

...and HVM?

HVM (known as **Hardware Virtual Machine**) is the type of instance that mimics bare-metal server setup which provides better hardware isolation. With this instance type, the OS can run directly on top of the Virtual Machine without additional configuration making it to look like it is running on a real physical server.

#### Retrieve All x86_64 Ubuntu hvm-ssd machine images

Retrieve a list of image objects.

Argument 'name' is optional and can be excluded entirely. 
You can request individual Ubuntu releases using the first string of the release code names found at https://wiki.ubuntu.com/Releases 
e.g. name="focal", name="bionic", name="trusty"
        
```python
list_of_image_objects =retrieve_all_ubuntu_x86_64_machine_images_hvm_ssd(self, name="")
```

#### Retrieve All arm64 Ubuntu hvm-ssd machine images

Retrieve a list of image objects.

Argument 'name' is optional and can be excluded entirely. 
You can request individual Ubuntu releases using the first string of the release code names found at https://wiki.ubuntu.com/Releases 
e.g. name="focal", name="bionic", name="trusty"

```python
list_of_image_objects =retrieve_all_ubuntu_arm64_machine_images_hvm_ssd(self, name="")
```

**[⬆ back to top](#table-of-contents)**
## Image Object

Image objects contains an attributes data class with the standard ec2 [image attributes](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images), descriptions available at this link.

Each object also contains a list of ebsblockdevices, and a list of virtuablockdevices - empty if none exists.

ebsblockdevices  holds a list of BlockDeviceMappingEBS if they exist.

virtualblockdevices holds a list of BlockDeviceMappingVirtual if they exist.

```python
class Image:
    def __init__(self):
        self.attributes = ImageAttributes()
        self.ebsblockdevices = []
        self.virtualblockdevices = []
```
```python
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
```

```python
@dataclass
class BlockDeviceMappingEBS:
    DeviceName: str = None
    SnapshotId: str = None
    VolumeSize: str = None
    DeleteOnTermination: bool = None
    VolumeType: str = None
    Encrypted: bool = None
```
```python
@dataclass
class BlockDeviceMappingVirtual:
    DeviceName: str = None
    VirtualName: str = None
```
**[⬆ back to top](#table-of-contents)**

# SSH Key Pairs
A [key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html), consisting of a public key and a private key, is a set of security credentials that you use to prove your identity when connecting to an EC2 instance.
Import the ec2object KeyPair and KeyPairManger to interact with SSH Key Pairs.
```python
from ec2objects import KeyPair, KeyPairManager
```
## KeyPair Manager
Create a keypair manager.
```python
keypair_manager = KeyPairManager()
```
### Retrieve Keypairs
Retrieve all of your keypairs.
```python
list_of_keypair_objects=keypair_manager.retrieve_keypairs()
```

### Retrieve Keypair By Name
Retrieve all of your keypairs by keypair name.
AWS keypair names are unique.

```python
list_of_keypair_objects=keypair_manager.retrieve_keypair_by_name(str:name)
```
### Retrieve Keypair By ID
Retrieve all of your keypairs by keypair ID.

```python
list_of_keypair_objects=keypair_manager.retrieve_keypair_by_id(str:keypairid)
```
### Retrieve Keypair By Fingerprint
Retrieve all of your keypairs by key fingerprint.

```python
list_of_keypair_objects=keypair_manager.retrieve_keypair_by_fingerprint(str:fingerprint)
```
### Retrieve Keypairs By Tag Keyname
Retrieve all of your keypairs by the name of a tag key, not it's actual tag content.

```python
list_of_keypair_objects=keypair_manager.retrieve_keypair_by_tag_keyname(str:tagkeyname)
```
### Retrieve Keypairs By Tag

Retrieve all of your keypairs by supplying the name of a tag, and the tag value.

```python
list_of_keypair_objects=keypair_manager.retrieve_keypair_by_tag(str:key,str:value)
```
### Upload Keypair RSA

AWS will only accept RSA keys for upload.
This method will return ONE keypair object with the details of the new key uploaded to AWS.

```python
uploadedkey = keypair_manager.upload_keypair_rsa(str:keyname, str:ssh_public_key, dict:tags)
```
where you provide tags for your keypair in the form of a dict, e.g.
```python
tags = {}
tags["tag1"] = "value1"
tags["apple"] = "banana"
```

**[⬆ back to top](#table-of-contents)**
## KeyPair Object

A keypair object contains the attributes, and tags for an AWS keypair.

```python
class KeyPair:
    def __init__(self):
        self.attributes = KeyPairAttributes()
        self.tags = []
        ...
```

```python
@dataclass
class KeyPairAttributes:
	KeyPairId: str = None
	KeyFingerprint: str = None
	KeyName: str = None
```

```python
@dataclass
class Tags:
	key: str = None
	Value: str = None
```

### Delete Keypair

You can delete a keypair from AWS by calling the delete method on your keypair_object.

```python3
keypair_object.delete()
```

**[⬆ back to top](#table-of-contents)**