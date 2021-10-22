from __future__ import annotations

from dataclasses import dataclass, field


from ..ec2common.ec2exceptions import *


@dataclass
class SecurityGroupAttributes:
    GroupId: str = None
    Tags: object = field(default_factory=list)


class SecurityGroupManager:
    def __init__():
        pass


class Security:
    def __init__(self):
        pass
