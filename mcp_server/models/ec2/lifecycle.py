"""Models for EC2 instance lifecycle operations (start, stop, reboot, terminate)."""

from pydantic import BaseModel, Field


class StartInstanceParams(BaseModel):
    instance_id: str = Field(..., description="ID of the EC2 instance")
    region: str = Field(..., description="AWS region of the instance")


class InstanceLifeCycleParams(BaseModel):
    instance_id: str = Field(..., description="ID of the EC2 instance")
    region: str = Field(..., description="AWS region of the instance")
