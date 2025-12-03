from .describe_vpc import vpc_resource

# Registry of all VPC resources (only 1 for now, but scalable later)
VPC_RESOURCES = {
    "vpc": vpc_resource,
}

# Export as list (for ResourceRegistry loader)
VPC_RESOURCE_LIST = list(VPC_RESOURCES.values())

__all__ = [
    "VPC_RESOURCES",
    "VPC_RESOURCE_LIST",
]
