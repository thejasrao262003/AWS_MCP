# mcp_server/tools/ec2/ebs/attachment_tools.py

import boto3
from fastmcp.tools import FunctionTool
from typing import Optional
from mcp_server.models.ebs import (
    AttachVolumeParams,
    DetachVolumeParams,
)

# =======================================================
# ATTACH
# =======================================================
def attach_volume(
    *,
    VolumeId: str,
    InstanceId: str,
    Device: str,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)
    return ec2.attach_volume(
        VolumeId=VolumeId,
        InstanceId=InstanceId,
        Device=Device,
    )


# =======================================================
# DETACH
# =======================================================
def detach_volume(
    *,
    VolumeId: str,
    InstanceId: Optional[str] = None,
    Force: Optional[bool] = False,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)
    return ec2.detach_volume(
        VolumeId=VolumeId,
        InstanceId=InstanceId,
        Force=Force,
    )

ATTACHMENT_REGISTRY = {
    "attach_volume": {
        "fn": attach_volume,
        "schema": AttachVolumeParams
    },
    "detach_volume": {
        "fn": detach_volume,
        "schema": DetachVolumeParams
    },
}

# Export for dispatcher auto-discovery
EBS_DISPATCH_REGISTRY = ATTACHMENT_REGISTRY