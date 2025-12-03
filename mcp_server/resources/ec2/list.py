from fastmcp.resources import FunctionResource

# ============================================================
# RESOURCE 1 — EC2 INSTANCE LISTING & DETAILS
# ============================================================

ec2_instance_listing_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EC2",
        "domain": "instance_listing",
        "description": (
            "Retrieve EC2 instance information: listings, filters, status, and tag-based queries. "
            "Use the aws_ec2 dispatcher tool with the actions below."
        ),

        "actions": {
            "list_ec2_instances": {
                "description": (
                    "List EC2 instances with advanced filtering options: state, type, VPC, subnet, SG, "
                    "spot filters and custom_filters."
                ),
                "required_params": [],
                "optional_params": [
                    "region", "instance_ids", "states", "tag_key", "tag_value",
                    "instance_types", "vpc_ids", "subnet_ids", "security_group_ids",
                    "spot_only", "exclude_spot", "spot_request_id", "custom_filters"
                ],
                "example": {
                    "action": "list_ec2_instances",
                    "states": ["running"]
                }
            },

            "get_instance_details": {
                "description": "Fetch full EC2 instance details by instance ID.",
                "required_params": ["instance_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "get_instance_details",
                    "instance_id": "i-0123456789abcdef0"
                }
            },

            "get_instance_status": {
                "description": "Get instance state, public IP, instance type, and lifecycle.",
                "required_params": ["instance_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "get_instance_status",
                    "instance_id": "i-0123456789abcdef0"
                }
            },

            "list_running_instances": {
                "description": "List only EC2 instances currently in the 'running' state.",
                "required_params": [],
                "optional_params": ["region", "spot_only"],
                "example": {"action": "list_running_instances"}
            },

            "list_instances_by_tag": {
                "description": "List instances filtered by tag key & value.",
                "required_params": ["tag_key", "tag_value"],
                "optional_params": ["region", "spot_only"],
                "example": {
                    "action": "list_instances_by_tag",
                    "tag_key": "env",
                    "tag_value": "prod"
                }
            },
        },

        "notes": [
            "This resource covers all non-spot EC2 listing operations.",
            "Use the EC2 Spot Requests resource for spot request APIs.",
            "All actions are routed via the aws_ec2 dispatcher."
        ]
    },

    uri="resource://aws/ec2/instance_listing",
    name="ec2_instance_listing_resource",
    mime_type="application/json",
)


# ============================================================
# RESOURCE 2 — EC2 SPOT REQUEST MANAGEMENT
# ============================================================

ec2_spot_requests_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EC2",
        "domain": "spot_requests",
        "description": (
            "Manage EC2 Spot Instance Requests: listing, detail lookup, and cancellation."
        ),

        "actions": {
            "list_spot_requests": {
                "description": "List AWS Spot Instance Requests (SIRs).",
                "required_params": [],
                "optional_params": ["region", "spot_request_ids", "states"],
                "example": {
                    "action": "list_spot_requests",
                    "states": ["open", "active"]
                }
            },

            "get_spot_request_details": {
                "description": "Retrieve details of a specific Spot Instance Request.",
                "required_params": ["spot_request_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "get_spot_request_details",
                    "spot_request_id": "sir-1234567890abcdef"
                }
            },

            "cancel_spot_request": {
                "description": (
                    "Cancel a Spot Instance Request. This does NOT terminate any launched instance."
                ),
                "required_params": ["spot_request_id"],
                "optional_params": ["region"],
                "example": {
                    "action": "cancel_spot_request",
                    "spot_request_id": "sir-1234567890abcdef"
                }
            }
        },

        "notes": [
            "Cancelling a Spot Request does NOT terminate the instance.",
            "Spot instance pricing/history is found in the EC2 pricing resource.",
            "All actions use the aws_ec2 dispatcher."
        ]
    },

    uri="resource://aws/ec2/spot_requests",
    name="ec2_spot_requests_resource",
    mime_type="application/json",
)


# ============================================================
# EXPORT LIST
# ============================================================

EC2_LISTING_AND_SPOT_RESOURCES = [
    ec2_instance_listing_resource,
    ec2_spot_requests_resource,
]

__all__ = [
    "ec2_instance_listing_resource",
    "ec2_spot_requests_resource",
    "EC2_LISTING_AND_SPOT_RESOURCES",
]
