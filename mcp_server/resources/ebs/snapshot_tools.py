from fastmcp.resources import FunctionResource

ebs_snapshot_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EBS",
        "domain": "snapshots",
        "description": "Manage EBS snapshots (create, list, copy, restore, delete).",
        "actions": {
            "create_snapshot": {
                "description": "Create a snapshot from a volume.",
                "required_params": ["VolumeId"],
                "optional_params": ["Description", "Tags", "region"],
                "example": {"action": "create_snapshot", "VolumeId": "vol-abc"}
            },
            "list_snapshots": {
                "description": "List snapshots with optional filtering.",
                "required_params": [],
                "optional_params": ["OwnerIds", "Filters", "region"],
                "example": {"action": "list_snapshots"}
            },
            "describe_snapshot": {
                "description": "Describe a specific snapshot.",
                "required_params": ["SnapshotId"],
                "optional_params": ["region"],
                "example": {"action": "describe_snapshot", "SnapshotId": "snap-123"}
            },
            "delete_snapshot": {
                "description": "Delete a snapshot.",
                "required_params": ["SnapshotId"],
                "optional_params": ["region"],
                "example": {"action": "delete_snapshot", "SnapshotId": "snap-999"}
            },
            "copy_snapshot": {
                "description": "Copy a snapshot to another region.",
                "required_params": ["SourceRegion", "SourceSnapshotId"],
                "optional_params": ["Description", "Encrypted", "KmsKeyId", "Tags", "region"],
                "example": {
                    "action": "copy_snapshot",
                    "SourceRegion": "us-east-1",
                    "SourceSnapshotId": "snap-111"
                }
            },
            "restore_volume_from_snapshot": {
                "description": "Restore/create volume from a snapshot.",
                "required_params": ["SnapshotId", "AvailabilityZone"],
                "optional_params": [
                    "VolumeType", "Size", "Iops", "Throughput", 
                    "Encrypted", "KmsKeyId", "ExtraParams", "region"
                ],
                "example": {
                    "action": "restore_volume_from_snapshot",
                    "SnapshotId": "snap-111",
                    "AvailabilityZone": "ap-south-1a"
                }
            },
            "manage_fast_snapshot_restore": {
                "description": "Enable/disable fast snapshot restore.",
                "required_params": ["SnapshotId", "AvailabilityZones", "State"],
                "optional_params": ["region"],
                "example": {
                    "action": "manage_fast_snapshot_restore",
                    "SnapshotId": "snap-111",
                    "AvailabilityZones": ["ap-south-1a"],
                    "State": "enable"
                }
            }
        },
        "notes": [
            "Snapshot operations are asynchronous.",
            "Fast snapshot restore incurs extra cost."
        ]
    },
    uri="resource://aws/ebs/snapshots",
    mime_type="application/json",
    name="ebs_snapshot_resource"
)
