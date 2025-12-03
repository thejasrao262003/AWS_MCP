# mcp_server/resources/ec2_ami.py

from fastmcp.resources import FunctionResource

ec2_ami_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EC2",
        "domain": "AMI",
        "description": (
            "Operations related to Amazon Machine Images (AMIs). "
            "Use the aws_ec2 dispatcher tool with the actions listed below."
        ),

        "actions": {
            "create_ami": {
                "description": "Create an AMI from an EC2 instance.",
                "required_params": ["instance_id", "name"],
                "optional_params": ["description", "tags", "no_reboot", "region"],
                "example": {
                    "action": "create_ami",
                    "instance_id": "i-0123456789abcdef0",
                    "name": "my-backup-image"
                }
            },

            "describe_images": {
                "description": "Describe AMIs using owners, image IDs, or filters.",
                "required_params": [],
                "optional_params": ["owners", "image_ids", "filters", "region"],
                "example": {
                    "action": "describe_images",
                    "owners": ["amazon"]
                }
            },

            "deregister_ami": {
                "description": "Delete/deregister an AMI.",
                "required_params": ["image_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "deregister_ami",
                    "image_id": "ami-0abcd1234example"
                }
            },

            "get_latest_ami": {
                "description": (
                    "Fetch the latest AMI for a given OS type "
                    "(ubuntu, amazon-linux-2, windows-2022, debian, etc.)."
                ),
                "required_params": ["os_type"],
                "optional_params": ["region", "architecture"],
                "example": {
                    "action": "get_latest_ami",
                    "os_type": "ubuntu"
                }
            }
        },

        "notes": [
            "All AMI operations run via the aws_ec2 dispatcher tool.",
            "Ensure your IAM role has permissions: ec2:CreateImage, ec2:DeregisterImage, ec2:DescribeImages.",
            "get_latest_ami supports: ubuntu, amazon-linux-2, amazon-linux-2023, "
            "windows-2022, windows-2019, debian, rhel, suse."
        ]
    },
    uri="resource://aws/ec2/ami",
    mime_type="application/json",
    name="ec2_ami_resource"
)
