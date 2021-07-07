# from distutils.core import setup
##How to package
##From your root package dir...
##python3 setup.py sdist
##twine check dist/*
##twine upload dist/*


from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="ec2objects",
    packages=[
        "ec2objects",
        "ec2objects.ec2common",
        "ec2objects.ec2api",
        "ec2objects.ec2object",
    ],
    version="0.0.1",
    license="MIT",
    description="ec2objects, represents all aws ec2 services as objects, hiding all those horrible api calls.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zoran ilievski",
    author_email="pythonic@clientuser.net",
    url="https://github.com/zorani/aws-ec2-objects",
    download_url="https://github.com/zorani/aws-ec2-objects/archive/refs/tags/v0.0.1.tar.gz",
    keywords=["aws", "api", "ec2", "objects", "awsapi"],
    install_requires=["cloudapi", "bs4"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
