from fastmcp.resources import FunctionResource

vpc_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "VPC",
        "description": (
            "Manage VPC networks, subnets, and default infrastructure. "
            "Use the unified `aws_vpc` dispatcher with the actions below."
        ),

        "actions": {
            "list_vpcs": {
                "description": "List all VPCs in a region.",
                "required_params": [],
                "optional_params": ["region"],
                "example": {"action": "list_vpcs", "region": "ap-south-1"}
            },

            "get_default_vpc": {
                "description": "Get the default VPC for a region.",
                "required_params": [],
                "optional_params": ["region"],
                "example": {"action": "get_default_vpc"}
            },

            "describe_vpc": {
                "description": "Describe one VPC or all VPCs if no ID is provided.",
                "required_params": [],
                "optional_params": ["vpc_id", "region"],
                "example": {"action": "describe_vpc", "vpc_id": "vpc-123456"}
            },

            "list_subnets": {
                "description": "List all subnets in the region.",
                "required_params": [],
                "optional_params": ["region"],
                "example": {"action": "list_subnets"}
            },

            "get_default_subnets": {
                "description": "Fetch all subnets inside the default VPC.",
                "required_params": [],
                "optional_params": ["region"],
                "example": {"action": "get_default_subnets"}
            },

            "describe_subnet": {
                "description": "Describe a specific subnet or list subnets by VPC.",
                "required_params": [],
                "optional_params": ["subnet_id", "vpc_id", "region"],
                "example": {"action": "describe_subnet", "subnet_id": "subnet-123456"}
            },
        },

        "notes": [
            "All actions must be executed through the aws_vpc dispatcher.",
            "Subnets & VPCs are region-scoped. Defaults to ap-south-1."
        ]
    },
    uri="resource://aws/vpc",
    name="vpc_resource",
    mime_type="application/json"
)
