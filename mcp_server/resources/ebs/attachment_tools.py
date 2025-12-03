from fastmcp.resources import FunctionResource

ebs_attachment_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EBS",
        "domain": "attachment",
        "description": (
            "Attach or detach EBS volumes from EC2 instances. "
            "Use the `aws_ebs` dispatcher tool with the below actions."
        ),
        "actions": {
            "attach_volume": {
                "description": "Attach an EBS volume to an EC2 instance.",
                "required_params": ["VolumeId", "InstanceId", "Device"],
                "optional_params": ["region"],
                "example": {
                    "action": "attach_volume",
                    "VolumeId": "vol-123",
                    "InstanceId": "i-456",
                    "Device": "/dev/sdf"
                }
            },
            "detach_volume": {
                "description": "Detach an attached EBS volume.",
                "required_params": ["VolumeId"],
                "optional_params": ["InstanceId", "Force", "region"],
                "example": {
                    "action": "detach_volume",
                    "VolumeId": "vol-123"
                }
            }
        },
        "notes": [
            "All actions flow through the unified aws_ebs dispatcher.",
            "Force detach may cause data loss if the instance is running."
        ]
    },
    uri="resource://aws/ebs/attachment",
    mime_type="application/json",
    name="ebs_attachment_resource"
)
