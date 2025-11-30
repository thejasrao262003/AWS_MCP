"""Models for EC2 Security Group management operations."""

from pydantic import BaseModel, Field
from typing import Optional, List


class IpPermission(BaseModel):
    protocol: str = Field(..., description="tcp | udp | icmp | -1")
    from_port: Optional[int] = Field(None, description="From port")
    to_port: Optional[int] = Field(None, description="To port")
    cidr: str = Field(..., description="CIDR block e.g. 0.0.0.0/0")


class CreateSecurityGroupParams(BaseModel):
    region: str = Field(default="ap-south-1")
    group_name: str
    description: str
    vpc_id: str
    inbound_rules: Optional[List[IpPermission]] = None


class DeleteSecurityGroupParams(BaseModel):
    region: str = Field(default="ap-south-1")
    group_id: str


class ModifyRulesParams(BaseModel):
    region: str = Field(default="ap-south-1")
    group_id: str
    rules: List[IpPermission]


class DescribeSGParams(BaseModel):
    region: str = Field(default="ap-south-1")
    group_id: Optional[str] = None
    group_name: Optional[str] = None


class ListSGParams(BaseModel):
    region: str = Field(default="ap-south-1")
