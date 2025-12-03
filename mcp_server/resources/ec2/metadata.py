from fastmcp.resources import FunctionResource

ec2_metadata_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EC2",
        "domain": "metadata",
        "description": (
            "Retrieve and modify EC2 instance metadata configuration including user-data "
            "and IMDSv2 settings. Use the aws_ec2 dispatcher tool with the actions below."
        ),

        "actions": {
            "get_user_data": {
                "description": (
                    "Fetch the user-data script of an EC2 instance. "
                    "User-data is base64-decoded in the response."
                ),
                "required_params": ["instance_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "get_user_data",
                    "instance_id": "i-0123456789abcdef0"
                }
            },

            "describe_metadata_options": {
                "description": (
                    "Describe EC2 instance metadata options (IMDS version, HttpTokens requirement, etc)."
                ),
                "required_params": ["instance_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "describe_metadata_options",
                    "instance_id": "i-0123456789abcdef0"
                }
            },

            "modify_metadata_options": {
                "description": (
                    "Modify EC2 metadata configuration. "
                    "Useful for enforcing IMDSv2 or adjusting hop limits."
                ),
                "required_params": ["instance_id"],
                "optional_params": [
                    "region",
                    "http_tokens",
                    "http_endpoint",
                    "http_put_response_hop_limit"
                ],
                "example": {
                    "action": "modify_metadata_options",
                    "instance_id": "i-0123456789abcdef0",
                    "http_tokens": "required"
                }
            }
        },

        "notes": [
            "User-data is only applied during instance launch unless explicitly re-run.",
            "IMDSv2 enforcement is recommended for security (http_tokens='required').",
            "HopLimit determines how many network hops metadata requests may traverse.",
            "metadata_options is returned exactly as EC2 stores it.",
            "All metadata actions must be executed via the aws_ec2 dispatcher tool."
        ]
    },

    uri="resource://aws/ec2/metadata",
    name="ec2_metadata_resource",
    mime_type="application/json"
)
