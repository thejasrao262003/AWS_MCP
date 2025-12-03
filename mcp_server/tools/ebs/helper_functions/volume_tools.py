# mcp_server/tools/ec2/ebs/volume_tools.py

import boto3
from fastmcp.tools import FunctionTool
from typing import Optional, Dict, Any, List
from mcp_server.models.ebs import (
    CreateVolumeParams,
    ModifyVolumeParams,
    DeleteVolumeParams,
    DescribeVolumeParams,
)

# =======================================================
# CREATE VOLUME
# =======================================================
def create_volume(
    *,
    AvailabilityZone: str,
    VolumeType: str = "gp3",
    Size: Optional[int] = None,
    SnapshotId: Optional[str] = None,
    Iops: Optional[int] = None,
    Throughput: Optional[int] = None,
    Encrypted: Optional[bool] = None,
    KmsKeyId: Optional[str] = None,
    Tags: Optional[Dict[str, str]] = None,
    ExtraParams: Optional[Dict[str, Any]] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    req = {
        "AvailabilityZone": AvailabilityZone,
        "VolumeType": VolumeType,
    }

    if Size:
        req["Size"] = Size
    if SnapshotId:
        req["SnapshotId"] = SnapshotId
    if Iops:
        req["Iops"] = Iops
    if Throughput:
        req["Throughput"] = Throughput
    if Encrypted is not None:
        req["Encrypted"] = Encrypted
    if KmsKeyId:
        req["KmsKeyId"] = KmsKeyId

    if Tags:
        req["TagSpecifications"] = [
            {
                "ResourceType": "volume",
                "Tags": [{"Key": k, "Value": v} for k, v in Tags.items()],
            }
        ]

    if ExtraParams:
        req.update(ExtraParams)

    return ec2.create_volume(**req)


# =======================================================
# MODIFY VOLUME
# =======================================================
def modify_volume(
    *,
    VolumeId: str,
    Size: Optional[int] = None,
    VolumeType: Optional[str] = None,
    Iops: Optional[int] = None,
    Throughput: Optional[int] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    req = {"VolumeId": VolumeId}

    if Size:
        req["Size"] = Size
    if VolumeType:
        req["VolumeType"] = VolumeType
    if Iops:
        req["Iops"] = Iops
    if Throughput:
        req["Throughput"] = Throughput

    return ec2.modify_volume(**req)


# =======================================================
# DELETE VOLUME
# =======================================================
def delete_volume(
    *,
    VolumeId: str,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)
    return ec2.delete_volume(VolumeId=VolumeId)


# =======================================================
# DESCRIBE VOLUMES
# =======================================================
def describe_volumes(
    *,
    VolumeId: Optional[str] = None,
    Filters: Optional[List[Dict[str, Any]]] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    if VolumeId:
        resp = ec2.describe_volumes(VolumeIds=[VolumeId])
    else:
        resp = ec2.describe_volumes(Filters=Filters or [])

    return resp.get("Volumes", [])

VOLUME_REGISTRY = {
    "create_volume": {
        "fn": create_volume,
        "schema": CreateVolumeParams
    },
    "modify_volume": {
        "fn": modify_volume,
        "schema": ModifyVolumeParams
    },
    "delete_volume": {
        "fn": delete_volume,
        "schema": DeleteVolumeParams
    },
    "describe_volumes": {
        "fn": describe_volumes,
        "schema": DescribeVolumeParams
    },
}

# Export for dispatcher auto-discovery
EBS_DISPATCH_REGISTRY = VOLUME_REGISTRY
