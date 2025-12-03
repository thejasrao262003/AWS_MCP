from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Literal

class EBSDispatcherParams(BaseModel):
    """
    Unified schema for all EBS actions.
    Dispatcher will read 'action' and route accordingly.
    """

    # REQUIRED for dispatcher routing
    action: Literal[
        "attach_volume",
        "detach_volume",
        "create_snapshot",
        "list_snapshots",
        "describe_snapshot",
        "delete_snapshot",
        "copy_snapshot",
        "restore_volume_from_snapshot",
        "manage_fast_snapshot_restore",
        "create_volume",
        "modify_volume",
        "delete_volume",
        "describe_volumes"
    ] = Field(..., description="EBS action to perform")

    # Shared optional region
    region: Optional[str] = Field("ap-south-1")

    # ===========================
    # ATTACH / DETACH
    # ===========================
    VolumeId: Optional[str] = None
    InstanceId: Optional[str] = None
    Device: Optional[str] = None
    Force: Optional[bool] = None

    # ===========================
    # SNAPSHOT OPERATIONS
    # ===========================
    Description: Optional[str] = None
    Tags: Optional[Dict[str, str]] = None

    OwnerIds: Optional[List[str]] = None
    Filters: Optional[List[Dict[str, Any]]] = None
    SnapshotId: Optional[str] = None

    SourceRegion: Optional[str] = None
    SourceSnapshotId: Optional[str] = None
    Encrypted: Optional[bool] = None
    KmsKeyId: Optional[str] = None

    # Restore volume fields
    AvailabilityZone: Optional[str] = None
    VolumeType: Optional[str] = None
    Size: Optional[int] = None
    Iops: Optional[int] = None
    Throughput: Optional[int] = None
    ExtraParams: Optional[Dict[str, Any]] = None

    # Fast Snapshot Restore
    AvailabilityZones: Optional[List[str]] = None
    State: Optional[str] = None   # “enable” / “disable”

    # ===========================
    # VOLUME OPERATIONS
    # ===========================
    SnapshotId: Optional[str] = None
