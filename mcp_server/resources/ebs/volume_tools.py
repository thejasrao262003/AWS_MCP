from fastmcp.resources import FunctionResource

ebs_volumes_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EBS",
        "domain": "volumes",
        "description": "Manage EBS volumes: create, modify, delete, describe.",
        "actions": {
            "create_volume": {
                "description": "Create a new EBS volume.",
                "required_params": ["AvailabilityZone"],
                "optional_params": [
                    "VolumeType", "Size", "SnapshotId", "Iops", "Throughput",
                    "Encrypted", "KmsKeyId", "Tags", "ExtraParams", "region"
                ],
                "example": {
                    "action": "create_volume",
                    "AvailabilityZone": "ap-south-1a",
                    "Size": 20
                }
            },
            "modify_volume": {
                "description": "Modify an existing EBS volume.",
                "required_params": ["VolumeId"],
                "optional_params": ["Size", "VolumeType", "Iops", "Throughput", "region"],
                "example": {"action": "modify_volume", "VolumeId": "vol-123", "Size": 200}
            },
            "delete_volume": {
                "description": "Delete an EBS volume.",
                "required_params": ["VolumeId"],
                "optional_params": ["region"],
                "example": {"action": "delete_volume", "VolumeId": "vol-123"}
            },
            "describe_volumes": {
                "description": "Describe volume(s).",
                "required_params": [],
                "optional_params": ["VolumeId", "Filters", "region"],
                "example": {"action": "describe_volumes"}
            }
        },
        "notes": [
            "Deleting a volume is permanent.",
            "Volumes must be detached before deletion."
        ]
    },
    uri="resource://aws/ebs/volumes",
    mime_type="application/json",
    name="ebs_volumes_resource"
)
