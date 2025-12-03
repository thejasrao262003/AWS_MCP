from fastmcp.resources import FunctionResource

ec2_instance_creation_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EC2",
        "domain": "instance_creation",
        "description": (
            "Operations for creating EC2 instances: on-demand, minimal, spot, and SSH helper generation."
        ),

        "actions": {
            "create_instance": {
                "description": "Create a fully-configurable EC2 on-demand instance.",
                "required_params": ["ImageId", "InstanceType"],
                "optional_params": [
                    "MinCount", "MaxCount",
                    "KeyName", "SubnetId", "SecurityGroupIds",
                    "BlockDeviceMappings", "NetworkInterfaces",
                    "TagSpecifications", "IamInstanceProfile",
                    "MetadataOptions", "UserData", "ExtraParams",
                    "region"
                ],
                "example": {
                    "action": "create_instance",
                    "ImageId": "ami-0abcd1234example",
                    "InstanceType": "t3.micro"
                }
            },

            "create_instance_minimal": {
                "description": (
                    "Create an EC2 instance with only required fields. "
                    "This is the simplest and safest creation pathway."
                ),
                "required_params": ["ImageId", "InstanceType"],
                "optional_params": [
                    "KeyName", "SecurityGroupIds",
                    "SubnetId", "TagSpecifications",
                    "region"
                ],
                "example": {
                    "action": "create_instance_minimal",
                    "ImageId": "ami-0abcd1234example",
                    "InstanceType": "t3.micro"
                }
            },

            "create_spot_instance": {
                "description": "Launch a Spot EC2 instance using request_spot_instances API.",
                "required_params": ["ImageId", "InstanceType"],
                "optional_params": [
                    "MaxPrice", "KeyName", "SecurityGroupIds",
                    "SubnetId", "BlockDeviceMappings",
                    "NetworkInterfaces", "TagSpecifications",
                    "IamInstanceProfile", "MetadataOptions",
                    "UserData", "ExtraParams", "region"
                ],
                "example": {
                    "action": "create_spot_instance",
                    "ImageId": "ami-0abcd1234example",
                    "InstanceType": "t3.micro",
                    "MaxPrice": "0.0050"
                }
            },

            "generate_instance_ssh_instruction": {
                "description": "Generate SSH instructions (username + command) based on AMI family and public IP.",
                "required_params": ["instance_id"],
                "optional_params": [
                    "key_name", "pem_path", "region"
                ],
                "example": {
                    "action": "generate_instance_ssh_instruction",
                    "instance_id": "i-0123456789abcdef"
                }
            },
        },

        "notes": [
            "create_instance offers the full AWS EC2 run_instances flexibility.",
            "create_instance_minimal is recommended for basic setups.",
            "Spot instances may take time to fulfill depending on capacity/price.",
            "SSH usernames differ based on AMI (ubuntu → ubuntu, amazon-linux → ec2-user).",
            "All actions must be executed using the aws_ec2 dispatcher tool."
        ]
    },
    uri="resource://aws/ec2/instance_creation",
    mime_type="application/json",
    name="ec2_instance_creation_resource"
)
