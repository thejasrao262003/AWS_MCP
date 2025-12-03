# mcp_server/tools/ec2/ebs/snapshot_tools.py

import boto3
from fastmcp.tools import FunctionTool
from typing import Optional, Dict, Any, List

from mcp_server.models.ebs import (
    ListSnapshotsParams,
    SnapshotIdParam,
    DeleteSnapshotParams,
    CopySnapshotParams,
    CreateVolumeFromSnapshotParams,
    FastRestoreParams,
    CreateSnapshotParams,
)

# =======================================================
# CREATE SNAPSHOT
# =======================================================
def create_snapshot(
    *,
    VolumeId: str,
    Description: Optional[str] = None,
    Tags: Optional[Dict[str, str]] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    req = {
        "VolumeId": VolumeId,
        "Description": Description or f"Snapshot of {VolumeId}",
    }

    if Tags:
        req["TagSpecifications"] = [
            {
                "ResourceType": "snapshot",
                "Tags": [{"Key": k, "Value": v} for k, v in Tags.items()],
            }
        ]

    return ec2.create_snapshot(**req)


# =======================================================
# LIST SNAPSHOTS
# =======================================================
def list_snapshots(
    *,
    OwnerIds: Optional[List[str]] = None,
    Filters: Optional[List[Dict[str, Any]]] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    req = {}

    if OwnerIds:
        req["OwnerIds"] = OwnerIds

    if Filters:
        req["Filters"] = Filters

    resp = ec2.describe_snapshots(**req)
    return resp.get("Snapshots", [])


# =======================================================
# DESCRIBE A SPECIFIC SNAPSHOT
# =======================================================
def describe_snapshot(
    *,
    SnapshotId: str,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)
    resp = ec2.describe_snapshots(SnapshotIds=[SnapshotId])
    return resp.get("Snapshots", [])


# =======================================================
# DELETE SNAPSHOT
# =======================================================
def delete_snapshot(
    *,
    SnapshotId: str,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)
    return ec2.delete_snapshot(SnapshotId=SnapshotId)


# =======================================================
# COPY SNAPSHOT (Cross Region Snapshot Copy)
# =======================================================
def copy_snapshot(
    *,
    SourceRegion: str,
    SourceSnapshotId: str,
    Description: Optional[str] = None,
    Encrypted: Optional[bool] = None,
    KmsKeyId: Optional[str] = None,
    Tags: Optional[Dict[str, str]] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    req = {
        "SourceRegion": SourceRegion,
        "SourceSnapshotId": SourceSnapshotId,
        "Description": Description or f"Copy of {SourceSnapshotId}",
    }

    if Encrypted is not None:
        req["Encrypted"] = Encrypted

    if KmsKeyId:
        req["KmsKeyId"] = KmsKeyId

    if Tags:
        req["TagSpecifications"] = [
            {
                "ResourceType": "snapshot",
                "Tags": [{"Key": k, "Value": v} for k, v in Tags.items()],
            }
        ]

    return ec2.copy_snapshot(**req)


# =======================================================
# CREATE VOLUME FROM SNAPSHOT (RESTORE)
# =======================================================
def restore_volume_from_snapshot(
    *,
    SnapshotId: str,
    AvailabilityZone: str,
    VolumeType: str = "gp3",
    Size: Optional[int] = None,
    Iops: Optional[int] = None,
    Throughput: Optional[int] = None,
    Encrypted: Optional[bool] = None,
    KmsKeyId: Optional[str] = None,
    ExtraParams: Optional[Dict[str, Any]] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    req = {
        "SnapshotId": SnapshotId,
        "AvailabilityZone": AvailabilityZone,
        "VolumeType": VolumeType,
    }

    if Size:
        req["Size"] = Size
    if Iops:
        req["Iops"] = Iops
    if Throughput:
        req["Throughput"] = Throughput
    if Encrypted is not None:
        req["Encrypted"] = Encrypted
    if KmsKeyId:
        req["KmsKeyId"] = KmsKeyId
    if ExtraParams:
        req.update(ExtraParams)

    return ec2.create_volume(**req)


# =======================================================
# FAST SNAPSHOT RESTORE (ENABLE/DISABLE)
# =======================================================
def manage_fast_snapshot_restore(
    *,
    SnapshotId: str,
    AvailabilityZones: List[str],
    State: str,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    if State not in ("enable", "disable"):
        return {"error": "State must be 'enable' or 'disable'"}

    if State == "enable":
        return ec2.enable_fast_snapshot_restores(
            SnapshotId=SnapshotId,
            AvailabilityZones=AvailabilityZones,
        )

    if State == "disable":
        return ec2.disable_fast_snapshot_restores(
            SnapshotId=SnapshotId,
            AvailabilityZones=AvailabilityZones,
        )



SNAPSHOT_REGISTRY = {
    "create_snapshot": {
        "fn": create_snapshot,
        "schema": CreateSnapshotParams
    },
    "list_snapshots": {
        "fn": list_snapshots,
        "schema": ListSnapshotsParams
    },
    "describe_snapshot": {
        "fn": describe_snapshot,
        "schema": SnapshotIdParam
    },
    "delete_snapshot": {
        "fn": delete_snapshot,
        "schema": DeleteSnapshotParams
    },
    "copy_snapshot": {
        "fn": copy_snapshot,
        "schema": CopySnapshotParams
    },
    "restore_volume_from_snapshot": {
        "fn": restore_volume_from_snapshot,
        "schema": CreateVolumeFromSnapshotParams
    },
    "manage_fast_snapshot_restore": {
        "fn": manage_fast_snapshot_restore,
        "schema": FastRestoreParams
    },
}

# Export for dispatcher auto-discovery
EBS_DISPATCH_REGISTRY = SNAPSHOT_REGISTRY