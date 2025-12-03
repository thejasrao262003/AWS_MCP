from .ami import ec2_ami_resource
from .instance_creation import ec2_instance_creation_resource
from .instance_lifecycle import ec2_instance_lifecycle_resource
from .keypair import ec2_keypair_resource
from .launch_templates import ec2_launch_templates_resource
from .list import ec2_instance_listing_resource, ec2_spot_requests_resource
from .metadata import ec2_metadata_resource
from .pricing import ec2_pricing_resource
from .security_groups import ec2_security_groups_resource

EC2_RESOURCES = {
    "ami": ec2_ami_resource,
    "instance_creation": ec2_instance_creation_resource,
    "instance_lifecycle": ec2_instance_lifecycle_resource,
    "keypair": ec2_keypair_resource,
    "launch_templates": ec2_launch_templates_resource,
    "instance_listing": ec2_instance_listing_resource,
    "spot_requests": ec2_spot_requests_resource,
    "metadata": ec2_metadata_resource,
    "pricing": ec2_pricing_resource,
    "security_groups": ec2_security_groups_resource,
}

# Use __builtins__.list to avoid shadowing from .list import
import builtins
EC2_RESOURCE_LIST = builtins.list(EC2_RESOURCES.values())

__all__ = [
    "EC2_RESOURCES",
    "EC2_RESOURCE_LIST",
]
