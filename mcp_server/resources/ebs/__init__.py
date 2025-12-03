from .attachment_tools import ebs_attachment_resource
from .snapshot_tools import ebs_snapshot_resource
from .volume_tools import ebs_volumes_resource

# Registry of all EBS resources
EBS_RESOURCES = {
    "attachment": ebs_attachment_resource,
    "snapshot": ebs_snapshot_resource,
    "volume": ebs_volumes_resource,
}

# Export as list (for ResourceRegistry loader)
EBS_RESOURCE_LIST = list(EBS_RESOURCES.values())

__all__ = [
    "EBS_RESOURCES",
    "EBS_RESOURCE_LIST",
]
