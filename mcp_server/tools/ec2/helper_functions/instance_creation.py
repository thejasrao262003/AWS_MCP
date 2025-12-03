from mcp_server.models.ec2 import (
    CreateInstanceParams,
    CreateInstanceMinimalParams,
    InstanceSSHInstructionParams,
    CreateSpotInstanceParams
)
import boto3
import os
from fastmcp.tools import FunctionTool
from typing import Optional, List, Dict, Any

DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

def create_instance(
    *,
    ImageId: str,
    InstanceType: str,
    MinCount: int = 1,
    MaxCount: int = 1,
    KeyName: Optional[str] = None,
    SubnetId: Optional[str] = None,
    SecurityGroupIds: Optional[List[str]] = None,
    BlockDeviceMappings: Optional[List[Dict[str, Any]]] = None,
    NetworkInterfaces: Optional[List[Dict[str, Any]]] = None,
    TagSpecifications: Optional[List[Dict[str, Any]]] = None,
    IamInstanceProfile: Optional[Dict[str, str]] = None,
    MetadataOptions: Optional[Dict[str, Any]] = None,
    UserData: Optional[str] = None,
    ExtraParams: Optional[Dict[str, Any]] = None,
    region: str = "ap-south-1"
):
    region = region or DEFAULT_REGION
    ec2 = boto3.client("ec2", region_name=region)

    payload = {
        "ImageId": ImageId,
        "InstanceType": InstanceType,
        "MinCount": MinCount,
        "MaxCount": MaxCount,
    }

    if KeyName:
        payload["KeyName"] = KeyName

    if SubnetId:
        payload["SubnetId"] = SubnetId

    if SecurityGroupIds:
        payload["SecurityGroupIds"] = SecurityGroupIds

    if BlockDeviceMappings:
        payload["BlockDeviceMappings"] = BlockDeviceMappings

    if NetworkInterfaces:
        payload["NetworkInterfaces"] = NetworkInterfaces

    if TagSpecifications:
        payload["TagSpecifications"] = TagSpecifications

    if IamInstanceProfile:
        payload["IamInstanceProfile"] = IamInstanceProfile

    if MetadataOptions:
        payload["MetadataOptions"] = MetadataOptions

    if UserData:
        payload["UserData"] = UserData

    if ExtraParams:
        payload.update(ExtraParams)

    try:
        resp = ec2.run_instances(**payload)
        inst = resp["Instances"][0]

        return {
            "region": region,
            "instance_id": inst["InstanceId"],
            "instance_type": inst["InstanceType"],
            "state": inst["State"]["Name"],
        }

    except Exception as e:
        return {"error": str(e)}

def create_instance_minimal(
    *,
    ImageId: str,
    InstanceType: str,
    KeyName: Optional[str] = None,
    SecurityGroupIds: Optional[List[str]] = None,
    SubnetId: Optional[str] = None,
    TagSpecifications: Optional[List[Dict[str, Any]]] = None,
    region: str = "ap-south-1"
):
    region = region or DEFAULT_REGION
    ec2 = boto3.client("ec2", region_name=region)

    try:
        payload = {
            "ImageId": ImageId,
            "InstanceType": InstanceType,
            "MinCount": 1,
            "MaxCount": 1,
        }

        if KeyName:
            payload["KeyName"] = KeyName

        if SecurityGroupIds:
            payload["SecurityGroupIds"] = SecurityGroupIds

        if SubnetId:
            payload["SubnetId"] = SubnetId

        if TagSpecifications:
            payload["TagSpecifications"] = TagSpecifications

        resp = ec2.run_instances(**payload)
        inst = resp["Instances"][0]

        return {
            "region": region,
            "instance_id": inst["InstanceId"],
            "public_ip": inst.get("PublicIpAddress"),
            "state": inst["State"]["Name"]
        }

    except Exception as e:
        return {"error": str(e)}

def create_spot_instance(
    *,
    ImageId: str,
    InstanceType: str,
    MaxPrice: Optional[str] = None,
    KeyName: Optional[str] = None,
    SecurityGroupIds: Optional[List[str]] = None,
    SubnetId: Optional[str] = None,
    BlockDeviceMappings: Optional[List[Dict[str, Any]]] = None,
    NetworkInterfaces: Optional[List[Dict[str, Any]]] = None,
    TagSpecifications: Optional[List[Dict[str, Any]]] = None,
    IamInstanceProfile: Optional[Dict[str, str]] = None,
    MetadataOptions: Optional[Dict[str, Any]] = None,
    UserData: Optional[str] = None,
    ExtraParams: Optional[Dict[str, Any]] = None,
    region: str = "ap-south-1"
):
    region = region or DEFAULT_REGION
    ec2 = boto3.client("ec2", region_name=region)

    launch_spec = {
        "ImageId": ImageId,
        "InstanceType": InstanceType,
    }

    if KeyName:
        launch_spec["KeyName"] = KeyName

    if SecurityGroupIds:
        launch_spec["SecurityGroupIds"] = SecurityGroupIds

    if SubnetId:
        launch_spec["SubnetId"] = SubnetId

    if BlockDeviceMappings:
        launch_spec["BlockDeviceMappings"] = BlockDeviceMappings

    if NetworkInterfaces:
        launch_spec["NetworkInterfaces"] = NetworkInterfaces

    if TagSpecifications:
        launch_spec["TagSpecifications"] = TagSpecifications

    if IamInstanceProfile:
        launch_spec["IamInstanceProfile"] = IamInstanceProfile

    if MetadataOptions:
        launch_spec["MetadataOptions"] = MetadataOptions

    if UserData:
        launch_spec["UserData"] = UserData

    if ExtraParams:
        launch_spec.update(ExtraParams)

    try:
        resp = ec2.request_spot_instances(
            LaunchSpecification=launch_spec,
            InstanceCount=1,
            Type="one-time",
            MaxPrice=MaxPrice,
        )

        sir = resp["SpotInstanceRequests"][0]

        return {
            "region": region,
            "spot_request_id": sir["SpotInstanceRequestId"],
            "state": sir["State"],
        }

    except Exception as e:
        return {"error": str(e)}
    
def generate_instance_ssh_instruction(
    *,
    instance_id: str,
    key_name: Optional[str] = None,
    pem_path: Optional[str] = None,
    region: str = "ap-south-1"
):
    region = region or DEFAULT_REGION
    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.describe_instances(InstanceIds=[instance_id])
        inst = resp["Reservations"][0]["Instances"][0]

        pub_ip = inst.get("PublicIpAddress")
        if not pub_ip:
            return {"error": "Instance has no public IP"}

        key_name = key_name or inst.get("KeyName")
        if not key_name:
            return {"error": "No KeyPair associated with instance"}

        pem_path = pem_path or f"~/{key_name}.pem"

        # Best-effort username guess
        ami = inst["ImageId"]
        if "ubuntu" in ami.lower():
            user = "ubuntu"
        elif "amazon" in ami.lower() or "amzn" in ami.lower():
            user = "ec2-user"
        else:
            user = "ec2-user"

        ssh_command = f"ssh -i {pem_path} {user}@{pub_ip}"

        return {
            "instance_id": instance_id,
            "region": region,
            "public_ip": pub_ip,
            "key_name": key_name,
            "pem_path": pem_path,
            "recommended_user": user,
            "ssh_command": ssh_command
        }

    except Exception as e:
        return {"error": str(e)}
    
EC2_DISPATCH_REGISTRY = {
    "create_instance": {
        "fn": create_instance,
        "schema": CreateInstanceParams,
    },
    "create_instance_minimal": {
        "fn": create_instance_minimal,
        "schema": CreateInstanceMinimalParams,
    },
    "create_spot_instance": {
        "fn": create_spot_instance,
        "schema": CreateSpotInstanceParams,
    },
    "generate_instance_ssh_instruction": {
        "fn": generate_instance_ssh_instruction,
        "schema": InstanceSSHInstructionParams,
    },
}
