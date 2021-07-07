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

## Token

Set the AWS_ACCESS_KEY_ID, and the AWS_SECRET_ACCESS_KEY environment variables with your amazon aws access credentials.

    export AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    export AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

## Default Region

Some API calls are not specific to any particular region.

All API calls need to be signed with a sig version 4 process which needs a region that you have access to.

So.. to make things easy on our selves please set the AWS_DEFAULT_REGION environment variable to a region you know you  have enabled for your credentials.

For example:

    export AWS_SECRET_ACCESS_KEY='us-east-1'




## api connection settings

You don't need to look too deeply here, this is for information only.

ec2objects is powered by a baserestapi class from the following project.

https://github.com/zorani/cloudapi/blob/main/cloudapi/baserestapi.py

ec2objects/ec2api/ec2apiconnection.py inherits baserestapi, 
baseresapi takes care of all the tricky rate limiting.

Inside /ec2apiconnection.py you will find
a 'callrateperhour' variable set to a limit of 5000 which is common for other services.
ec2objects converts 'callrateperhour' to seconds between requests.

You will also see the following variables.

geometric_delay_multiplier: If a request fails, the 'seconds between requests' is increased by multiplying by this number.

maximum_geometric_delay_multiplicaiton: How many times should you increase the 'seconds between requests' before considering it a fail.

maximum_failed_attempts: a failed attempt is put to the back of an internal queue for a retry. how many failed attempts are allowed before
                         returning the response with failure codes and content.

```python
        BaseRESTAPI.__init__(
            self,
            baseurl="https://ec2.amazonaws.com",
            callrateperhour=5000,
            geometric_delay_multiplier=2,
            maximum_geometric_delay_multiplications=6,
            maximum_failed_attempts=3,
        )
```

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


```python
class Region:
    def __init__(self):
        self.attributes = RegionAttributes()
        ...
```
```python
@dataclass
class RegionAttributes:
    regionName: str = None
    regionEndpoint: str = None
```
**[⬆ back to top](#table-of-contents)**