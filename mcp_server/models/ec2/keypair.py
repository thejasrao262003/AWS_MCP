"""Models for EC2 KeyPair management operations."""

from pydantic import BaseModel, Field


class CreateKeyPairParams(BaseModel):
    region: str = Field(default="ap-south-1")
    key_name: str


class DeleteKeyPairParams(BaseModel):
    region: str = Field(default="ap-south-1")
    key_name: str


class ListKeyPairsParams(BaseModel):
    region: str = Field(default="ap-south-1")
