"""Models for EC2 instance creation and configuration."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class BaseEC2Tag(BaseModel):
    Key: str
    Value: str


class EBSConfig(BaseModel):
    VolumeSize: Optional[int] = None
    VolumeType: Optional[str] = None
    DeleteOnTermination: Optional[bool] = None
    Encrypted: Optional[bool] = None
    SnapshotId: Optional[str] = None


class BlockDevice(BaseModel):
    DeviceName: str
    Ebs: Optional[EBSConfig] = None


class NetworkInterfaceConfig(BaseModel):
    DeviceIndex: int
    SubnetId: Optional[str] = None
    Description: Optional[str] = None
    Groups: Optional[List[str]] = None
    DeleteOnTermination: Optional[bool] = None
    AssociatePublicIpAddress: Optional[bool] = None


class CreateInstanceParams(BaseModel):
    region: str = Field(default="ap-south-1")

    ImageId: str = Field(..., description="AMI ID to launch")
    InstanceType: str = Field(..., description="EC2 instance type")
    MinCount: int = 1
    MaxCount: int = 1

    KeyName: Optional[str] = None
    SubnetId: Optional[str] = None
    SecurityGroupIds: Optional[List[str]] = None

    BlockDeviceMappings: Optional[List[BlockDevice]] = None
    NetworkInterfaces: Optional[List[NetworkInterfaceConfig]] = None

    TagSpecifications: Optional[List[Dict[str, Any]]] = None

    IamInstanceProfile: Optional[Dict[str, str]] = None
    MetadataOptions: Optional[Dict[str, Any]] = None
    UserData: Optional[str] = None
    
    ExtraParams: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Any additional boto3.run_instances fields"
    )


class CreateSpotInstanceParams(BaseModel):
    region: str = Field(default="ap-south-1")

    ImageId: str = Field(..., description="AMI ID to launch")
    InstanceType: str = Field(..., description="EC2 instance type")

    MaxPrice: Optional[str] = Field(
        None,
        description="Maximum bid price for the Spot instance (e.g. '0.015'). If None, AWS chooses market price."
    )

    KeyName: Optional[str] = None
    SubnetId: Optional[str] = None
    SecurityGroupIds: Optional[List[str]] = None

    BlockDeviceMappings: Optional[List[BlockDevice]] = None
    NetworkInterfaces: Optional[List[NetworkInterfaceConfig]] = None

    TagSpecifications: Optional[List[Dict[str, Any]]] = None

    IamInstanceProfile: Optional[Dict[str, str]] = None
    MetadataOptions: Optional[Dict[str, Any]] = None
    UserData: Optional[str] = None

    ExtraParams: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Any additional boto3.request_spot_instances fields"
    )


class CreateInstanceMinimalParams(BaseModel):
    region: str = Field(default="ap-south-1")

    ImageId: str = Field(..., description="AMI ID")
    InstanceType: str = Field(..., description="EC2 instance type")

    KeyName: Optional[str] = None
    SecurityGroupIds: Optional[List[str]] = None
    SubnetId: Optional[str] = None

    TagSpecifications: Optional[List[Dict[str, Any]]] = None


class InstanceSSHInstructionParams(BaseModel):
    instance_id: str = Field(..., description="ID of the EC2 instance")
    region: str = Field(default="ap-south-1")
    key_name: Optional[str] = Field(
        None, description="Name of the keypair used for SSH"
    )
    pem_path: Optional[str] = Field(
        None, description="Local path where the PEM is saved"
    )
