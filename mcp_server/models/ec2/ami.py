# mcp_server/models/ec2/ami_models.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict

# -------------------------------------------------------
# CREATE AMI
# -------------------------------------------------------
class CreateAMIParams(BaseModel):
    instance_id: str = Field(..., description="Instance ID to create AMI from")
    name: str = Field(..., description="Name of the resulting AMI")
    description: Optional[str] = None
    no_reboot: bool = Field(default=False, description="If True, no reboot occurs during AMI creation")
    region: str = Field(default="ap-south-1")

    tags: Optional[Dict[str, str]] = Field(
        default=None,
        description="Tags to apply to the resulting AMI"
    )

# -------------------------------------------------------
# DESCRIBE IMAGES
# -------------------------------------------------------
class DescribeImagesParams(BaseModel):
    region: str = Field(default="ap-south-1")
    owners: Optional[List[str]] = Field(
        default=None, 
        description="Owners list e.g., ['self', 'amazon']"
    )
    image_ids: Optional[List[str]] = None
    filters: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="EC2 compatible filter list"
    )

# -------------------------------------------------------
# DEREGISTER AMI
# -------------------------------------------------------
class DeregisterAMIParams(BaseModel):
    image_id: str = Field(..., description="AMI ID to deregister")
    region: str = Field(default="ap-south-1")

# -------------------------------------------------------
# GET LATEST AMI
# -------------------------------------------------------
class GetLatestAMIParams(BaseModel):
    os_type: str = Field(
        ..., 
        description="OS type: 'ubuntu', 'amazon-linux-2', 'amazon-linux-2023', 'windows-2022', 'windows-2019', 'debian', 'rhel', 'suse'"
    )
    region: str = Field(default="ap-south-1")
    architecture: str = Field(
        default="x86_64",
        description="Architecture: 'x86_64' or 'arm64'"
    )
