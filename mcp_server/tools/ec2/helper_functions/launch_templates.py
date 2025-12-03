from mcp_server.models.ec2.launch_templates import (
    CreateLaunchTemplateParams,
    CreateLaunchTemplateVersionParams,
    DescribeLaunchTemplateParams,
    DeleteLaunchTemplateParams,
    LaunchFromTemplateParams
)
import boto3
import base64
from fastmcp.tools import FunctionTool
from typing import Optional, List, Dict, Any


def create_launch_template(
    *,
    LaunchTemplateName: str,
    ImageId: str,
    InstanceType: str,
    VersionDescription: Optional[str] = None,
    KeyName: Optional[str] = None,
    SecurityGroupIds: Optional[List[str]] = None,
    SubnetId: Optional[str] = None,
    UserData: Optional[str] = None,
    TagSpecifications: Optional[List[Dict[str, Any]]] = None,
    BlockDeviceMappings: Optional[List[Dict[str, Any]]] = None,
    NetworkInterfaces: Optional[List[Dict[str, Any]]] = None,
    IamInstanceProfile: Optional[Dict[str, str]] = None,
    MetadataOptions: Optional[Dict[str, Any]] = None,
    ExtraParams: Optional[Dict[str, Any]] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    lt_data = {
        "ImageId": ImageId,
        "InstanceType": InstanceType,
    }

    if KeyName:
        lt_data["KeyName"] = KeyName

    if SecurityGroupIds:
        lt_data["SecurityGroupIds"] = SecurityGroupIds

    if SubnetId:
        lt_data["SubnetId"] = SubnetId

    if UserData:
        lt_data["UserData"] = base64.b64encode(UserData.encode()).decode()

    if TagSpecifications:
        lt_data["TagSpecifications"] = TagSpecifications

    if BlockDeviceMappings:
        lt_data["BlockDeviceMappings"] = BlockDeviceMappings

    if NetworkInterfaces:
        lt_data["NetworkInterfaces"] = NetworkInterfaces

    if IamInstanceProfile:
        lt_data["IamInstanceProfile"] = IamInstanceProfile

    if MetadataOptions:
        lt_data["MetadataOptions"] = MetadataOptions

    if ExtraParams:
        lt_data.update(ExtraParams)

    resp = ec2.create_launch_template(
        LaunchTemplateName=LaunchTemplateName,
        VersionDescription=VersionDescription or "",
        LaunchTemplateData=lt_data
    )
    return resp


# ================================================
# CREATE NEW VERSION
# ================================================

def create_launch_template_version(
    *,
    LaunchTemplateName: str,
    VersionDescription: Optional[str] = None,
    ImageId: Optional[str] = None,
    InstanceType: Optional[str] = None,
    KeyName: Optional[str] = None,
    SecurityGroupIds: Optional[List[str]] = None,
    SubnetId: Optional[str] = None,
    UserData: Optional[str] = None,
    TagSpecifications: Optional[List[Dict[str, Any]]] = None,
    BlockDeviceMappings: Optional[List[Dict[str, Any]]] = None,
    NetworkInterfaces: Optional[List[Dict[str, Any]]] = None,
    IamInstanceProfile: Optional[Dict[str, str]] = None,
    MetadataOptions: Optional[Dict[str, Any]] = None,
    ExtraParams: Optional[Dict[str, Any]] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    lt_data = {}

    if ImageId:
        lt_data["ImageId"] = ImageId
    if InstanceType:
        lt_data["InstanceType"] = InstanceType
    if KeyName:
        lt_data["KeyName"] = KeyName
    if SecurityGroupIds:
        lt_data["SecurityGroupIds"] = SecurityGroupIds
    if SubnetId:
        lt_data["SubnetId"] = SubnetId
    if UserData:
        lt_data["UserData"] = base64.b64encode(UserData.encode()).decode()
    if TagSpecifications:
        lt_data["TagSpecifications"] = TagSpecifications
    if BlockDeviceMappings:
        lt_data["BlockDeviceMappings"] = BlockDeviceMappings
    if NetworkInterfaces:
        lt_data["NetworkInterfaces"] = NetworkInterfaces
    if IamInstanceProfile:
        lt_data["IamInstanceProfile"] = IamInstanceProfile
    if MetadataOptions:
        lt_data["MetadataOptions"] = MetadataOptions
    if ExtraParams:
        lt_data.update(ExtraParams)

    resp = ec2.create_launch_template_version(
        LaunchTemplateName=LaunchTemplateName,
        VersionDescription=VersionDescription or "",
        LaunchTemplateData=lt_data
    )

    return resp


# ================================================
# DESCRIBE TEMPLATE
# ================================================

def describe_launch_template(
    *,
    LaunchTemplateName: Optional[str] = None,
    LaunchTemplateId: Optional[str] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    if LaunchTemplateId:
        return ec2.describe_launch_templates(
            LaunchTemplateIds=[LaunchTemplateId]
        )
    else:
        return ec2.describe_launch_templates(
            LaunchTemplateNames=[LaunchTemplateName]
        )


# ================================================
# DELETE TEMPLATE
# ================================================

def delete_launch_template(
    *,
    LaunchTemplateName: Optional[str] = None,
    LaunchTemplateId: Optional[str] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    if LaunchTemplateId:
        return ec2.delete_launch_template(
            LaunchTemplateId=LaunchTemplateId
        )
    else:
        return ec2.delete_launch_template(
            LaunchTemplateName=LaunchTemplateName
        )


# ================================================
# LIST ALL TEMPLATES
# ================================================

def list_launch_templates(region: str = "ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)
    return ec2.describe_launch_templates()


# ================================================
# LAUNCH INSTANCE FROM TEMPLATE
# ================================================

def launch_from_template(
    *,
    LaunchTemplateName: str,
    Version: Optional[str] = None,
    MinCount: int = 1,
    MaxCount: int = 1,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    resp = ec2.run_instances(
        LaunchTemplate={
            "LaunchTemplateName": LaunchTemplateName,
            "Version": Version or "$Latest"
        },
        MinCount=MinCount,
        MaxCount=MaxCount
    )

    return resp

EC2_DISPATCH_REGISTRY = {
    "create_launch_template": {
        "fn": create_launch_template,
        "schema": CreateLaunchTemplateParams,
    },
    "create_launch_template_version": {
        "fn": create_launch_template_version,
        "schema": CreateLaunchTemplateVersionParams,
    },
    "describe_launch_template": {
        "fn": describe_launch_template,
        "schema": DescribeLaunchTemplateParams,
    },
    "delete_launch_template": {
        "fn": delete_launch_template,
        "schema": DeleteLaunchTemplateParams,
    },
    "list_launch_templates": {
        "fn": list_launch_templates,
        "schema": DeleteLaunchTemplateParams,
    },
    "launch_from_template": {
        "fn": launch_from_template,
        "schema": LaunchFromTemplateParams,
    },
}
