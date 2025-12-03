from fastmcp.resources import FunctionResource

ec2_launch_templates_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EC2",
        "domain": "launch_templates",
        "description": (
            "Manage EC2 Launch Templates, including creation, versioning, "
            "description, deletion, listing, and launching instances from templates. "
            "Use the aws_ec2 dispatcher tool with the actions below."
        ),

        "actions": {
            "create_launch_template": {
                "description": "Create a new EC2 Launch Template.",
                "required_params": [
                    "LaunchTemplateName",
                    "ImageId",
                    "InstanceType"
                ],
                "optional_params": [
                    "VersionDescription", "KeyName", "SecurityGroupIds",
                    "SubnetId", "UserData", "TagSpecifications",
                    "BlockDeviceMappings", "NetworkInterfaces",
                    "IamInstanceProfile", "MetadataOptions",
                    "ExtraParams", "region"
                ],
                "example": {
                    "action": "create_launch_template",
                    "LaunchTemplateName": "my-app-template",
                    "ImageId": "ami-0abcd1234example",
                    "InstanceType": "t3.micro"
                }
            },

            "create_launch_template_version": {
                "description": "Create a new version of an existing Launch Template.",
                "required_params": ["LaunchTemplateName"],
                "optional_params": [
                    "VersionDescription", "ImageId", "InstanceType",
                    "KeyName", "SecurityGroupIds", "SubnetId",
                    "UserData", "TagSpecifications", "BlockDeviceMappings",
                    "NetworkInterfaces", "IamInstanceProfile",
                    "MetadataOptions", "ExtraParams", "region"
                ],
                "example": {
                    "action": "create_launch_template_version",
                    "LaunchTemplateName": "my-app-template",
                    "ImageId": "ami-0abcd1234example"
                }
            },

            "describe_launch_template": {
                "description": "Describe a Launch Template by name or ID.",
                "required_params": [],
                "optional_params": ["LaunchTemplateName", "LaunchTemplateId", "region"],
                "example": {
                    "action": "describe_launch_template",
                    "LaunchTemplateName": "my-app-template"
                }
            },

            "delete_launch_template": {
                "description": "Delete a Launch Template by name or ID.",
                "required_params": [],
                "optional_params": ["LaunchTemplateName", "LaunchTemplateId", "region"],
                "example": {
                    "action": "delete_launch_template",
                    "LaunchTemplateName": "my-app-template"
                }
            },

            "list_launch_templates": {
                "description": "List all Launch Templates in a region.",
                "required_params": ["region"],
                "optional_params": [],
                "example": {
                    "action": "list_launch_templates",
                    "region": "ap-south-1"
                }
            },

            "launch_from_template": {
                "description": (
                    "Launch an EC2 instance using a Launch Template. "
                    "Uses the specified version or falls back to `$Latest`."
                ),
                "required_params": ["LaunchTemplateName"],
                "optional_params": ["Version", "MinCount", "MaxCount", "region"],
                "example": {
                    "action": "launch_from_template",
                    "LaunchTemplateName": "my-app-template",
                    "Version": "$Latest"
                }
            }
        },

        "notes": [
            "Launch Templates allow reusable instance configuration.",
            "UserData is automatically base64-encoded inside the tool implementation.",
            "Versioning lets you maintain multiple configurations under one template name.",
            "Use launch_from_template when you want consistent reproducible instances.",
            "All actions must be executed through the aws_ec2 dispatcher."
        ]
    },

    uri="resource://aws/ec2/launch_templates",
    name="ec2_launch_templates_resource",
    mime_type="application/json"
)
