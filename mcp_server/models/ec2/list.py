"""Models for EC2 instance listing and querying operations."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ListEC2ParamsTagwise(BaseModel):
    region: str
    tag_key: Optional[str] = None
    tag_value: Optional[str] = None
    spot_only: bool = False


class EC2ListFilters(BaseModel):
    region: Optional[str] = Field(default=None)
    instance_ids: Optional[List[str]] = Field(default=None)
    states: Optional[List[str]] = Field(default=None)
    
    tag_key: Optional[str] = None
    tag_value: Optional[str] = None

    instance_types: Optional[List[str]] = None
    vpc_ids: Optional[List[str]] = None
    subnet_ids: Optional[List[str]] = None
    security_group_ids: Optional[List[str]] = None

    # ----- SPOT SUPPORT -----
    spot_only: bool = Field(
        default=False, 
        description="If true, only return Spot instances."
    )
    exclude_spot: bool = Field(
        default=False, 
        description="If true, exclude Spot instances (only on-demand)."
    )
    spot_request_id: Optional[str] = Field(
        default=None,
        description="Filter instances that were created from a specific Spot Request ID."
    )

    # ----- RAW CUSTOM FILTERS -----
    custom_filters: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Pass raw EC2 filter structures: [{'Name': '...', 'Values': [...]}]"
    )


# Alias for backward compatibility
ListEC2Params = EC2ListFilters


class GetInstanceDetailsParams(BaseModel):
    instance_id: str = Field(..., description="ID of the EC2 instance")
    region: str = Field(..., description="AWS region of the instance")


class ListSpotRequestsParams(BaseModel):
    region: Optional[str] = Field(
        None, description="AWS region to query. Defaults to the global DEFAULT_REGION."
    )
    spot_request_ids: Optional[List[str]] = Field(
        None, description="List of specific Spot Request IDs to fetch."
    )
    states: Optional[List[str]] = Field(
        None,
        description="Filter spot requests by state. Examples: open, active, closed, cancelled, failed.",
    )


class GetSpotRequestDetailsParams(BaseModel):
    spot_request_id: str = Field(
        ..., description="The Spot Instance Request ID (sir-xxxxxxxx)."
    )
    region: Optional[str] = Field(
        None, description="AWS region. Defaults to the global DEFAULT_REGION."
    )


class CancelSpotRequestParams(BaseModel):
    spot_request_id: str = Field(
        ..., description="The Spot Instance Request ID to cancel."
    )
    region: Optional[str] = Field(
        None, description="AWS region. Defaults to the global DEFAULT_REGION."
    )
