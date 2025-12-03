from fastmcp.resources import FunctionResource


ec2_security_groups_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EC2",
        "domain": "security_groups",
        "description": (
            "Manage EC2 Security Groups including creation, deletion, rule authorization, "
            "rule revocation, description, and listing. "
            "Use the aws_ec2 dispatcher tool with the actions below."
        ),

        "actions": {
            "create_security_group": {
                "description": (
                    "Create a Security Group within a VPC and optionally attach inbound rules. "
                    "Inbound rules use IpPermission objects (protocol, from_port, to_port, cidr)."
                ),
                "required_params": ["region", "group_name", "description", "vpc_id"],
                "optional_params": ["inbound_rules"],
                "example": {
                    "action": "create_security_group",
                    "region": "ap-south-1",
                    "group_name": "my-sg",
                    "description": "SG for web servers",
                    "vpc_id": "vpc-012abc345",
                    "inbound_rules": [
                        {
                            "protocol": "tcp",
                            "from_port": 80,
                            "to_port": 80,
                            "cidr": "0.0.0.0/0"
                        }
                    ]
                }
            },

            "delete_security_group": {
                "description": "Delete an EC2 Security Group by GroupId.",
                "required_params": ["region", "group_id"],
                "optional_params": [],
                "example": {
                    "action": "delete_security_group",
                    "region": "ap-south-1",
                    "group_id": "sg-012abcd1234"
                }
            },

            "authorize_security_group_rules": {
                "description": (
                    "Add inbound rules to a Security Group. "
                    "Each rule must match the IpPermission schema."
                ),
                "required_params": ["region", "group_id", "rules"],
                "optional_params": [],
                "example": {
                    "action": "authorize_security_group_rules",
                    "region": "ap-south-1",
                    "group_id": "sg-012abcd1234",
                    "rules": [
                        {
                            "protocol": "tcp",
                            "from_port": 22,
                            "to_port": 22,
                            "cidr": "0.0.0.0/0"
                        }
                    ]
                }
            },

            "revoke_security_group_rules": {
                "description": (
                    "Remove inbound rules from a Security Group. "
                    "Rules must match existing rules."
                ),
                "required_params": ["region", "group_id", "rules"],
                "optional_params": [],
                "example": {
                    "action": "revoke_security_group_rules",
                    "region": "ap-south-1",
                    "group_id": "sg-012abcd1234",
                    "rules": [
                        {
                            "protocol": "tcp",
                            "from_port": 22,
                            "to_port": 22,
                            "cidr": "0.0.0.0/0"
                        }
                    ]
                }
            },

            "describe_security_group": {
                "description": (
                    "Describe one or more Security Groups by group_id or group_name."
                ),
                "required_params": ["region"],
                "optional_params": ["group_id", "group_name"],
                "example": {
                    "action": "describe_security_group",
                    "region": "ap-south-1",
                    "group_id": "sg-012abcd1234"
                }
            },

            "list_security_groups": {
                "description": "List every Security Group in the region.",
                "required_params": ["region"],
                "optional_params": [],
                "example": {
                    "action": "list_security_groups",
                    "region": "ap-south-1"
                }
            }
        },

        "notes": [
            "Security Groups are stateful—return traffic is automatically allowed.",
            "Only inbound rules are handled here, outbound rules can be added similarly if required.",
            "All rule definitions must match IpPermission { protocol, from_port, to_port, cidr }.",
            "SG operations require EC2 permissions: CreateSecurityGroup, AuthorizeSecurityGroupIngress, "
            "RevokeSecurityGroupIngress, DescribeSecurityGroups.",
            "All actions must be executed via the aws_ec2 dispatcher."
        ]
    },
    uri="aws://ec2/security-groups",
    mime_type="application/json",
    name="ec2_security_groups_resource"
)
