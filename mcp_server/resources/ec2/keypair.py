from fastmcp.resources import FunctionResource

ec2_keypair_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EC2",
        "domain": "keypair",
        "description": "Create, delete, and list EC2 SSH KeyPairs. Use the aws_ec2 dispatcher tool.",

        "actions": {
            "create_keypair": {
                "description": "Create an EC2 KeyPair. Returns key material (PEM) that you must save locally.",
                "required_params": ["region", "key_name"],
                "optional_params": [],
                "example": {
                    "action": "create_keypair",
                    "region": "ap-south-1",
                    "key_name": "my-server-key"
                }
            },

            "delete_keypair": {
                "description": "Delete an EC2 KeyPair by name.",
                "required_params": ["region", "key_name"],
                "optional_params": [],
                "example": {
                    "action": "delete_keypair",
                    "region": "ap-south-1",
                    "key_name": "my-server-key"
                }
            },

            "list_keypairs": {
                "description": "List all EC2 KeyPairs in the given region.",
                "required_params": ["region"],
                "optional_params": [],
                "example": {
                    "action": "list_keypairs",
                    "region": "ap-south-1"
                }
            }
        },

        "notes": [
            "KeyPairs are required for SSH authentication for many AMIs.",
            "PEM material is returned only during creation — save it immediately.",
            "Deleting a keypair does NOT delete local PEM files.",
            "save_pem_file is a backend helper, not exposed as a tool.",
            "All keypair actions must be executed using the aws_ec2 dispatcher."
        ]
    },

    uri="resource://aws/ec2/keypair",
    name="ec2_keypair_resource",
    mime_type="application/json"
)
