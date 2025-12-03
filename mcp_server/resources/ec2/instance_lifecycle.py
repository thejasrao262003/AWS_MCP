from fastmcp.resources import FunctionResource

ec2_instance_lifecycle_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EC2",
        "domain": "instance_lifecycle",
        "description": (
            "Start, stop, reboot, hard-reboot, and terminate EC2 instances. "
            "Execute using the aws_ec2 dispatcher tool."
        ),

        "actions": {
            "start_instance": {
                "description": "Start an EC2 instance.",
                "required_params": ["instance_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "start_instance",
                    "instance_id": "i-0123456789abcdef"
                }
            },

            "stop_instance": {
                "description": "Stop a running EC2 instance.",
                "required_params": ["instance_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "stop_instance",
                    "instance_id": "i-0123456789abcdef"
                }
            },

            "reboot_instance": {
                "description": "Soft reboot an EC2 instance (graceful).",
                "required_params": ["instance_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "reboot_instance",
                    "instance_id": "i-0123456789abcdef"
                }
            },

            "hard_reboot_instance": {
                "description": (
                    "Hard reboot an EC2 instance (force reboot). Equivalent to pulling the power plug."
                ),
                "required_params": ["instance_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "hard_reboot_instance",
                    "instance_id": "i-0123456789abcdef"
                }
            },

            "terminate_instance": {
                "description": "Permanently terminate an EC2 instance (cannot be undone).",
                "required_params": ["instance_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "terminate_instance",
                    "instance_id": "i-0123456789abcdef"
                }
            }
        },

        "notes": [
            "Lifecycle operations require the instance to be in a valid state.",
            "stop_instance works only on running instances.",
            "start_instance works only on stopped instances.",
            "terminate_instance is irreversible.",
            "hard_reboot_instance immediately restarts the instance (not graceful).",
            "All lifecycle actions must be used with the aws_ec2 dispatcher."
        ]
    },
    uri="resource://aws/ec2/instance_lifecycle",
    mime_type="application/json",
    name="ec2_instance_lifecycle_resource"
)
