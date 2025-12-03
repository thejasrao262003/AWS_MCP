# mcp_server/tools/ec2/metadata_tools.py

import boto3
import base64
from fastmcp.tools import FunctionTool
from typing import Optional

from mcp_server.models.ec2.metadata import (
    GetUserDataParams,
    DescribeMetadataOptionsParams,
    ModifyMetadataOptionsParams
)

def get_user_data(
    *,
    instance_id: str,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    resp = ec2.describe_instance_attribute(
        InstanceId=instance_id,
        Attribute="userData"
    )

    raw_b64 = resp.get("UserData", {}).get("Value")

    if not raw_b64:
        return {"instance_id": instance_id, "user_data": None}

    decoded = base64.b64decode(raw_b64).decode(errors="replace")

    return {
        "instance_id": instance_id,
        "user_data": decoded,
    }

def describe_metadata_options(
    *,
    instance_id: str,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    resp = ec2.describe_instances(InstanceIds=[instance_id])

    instance = resp["Reservations"][0]["Instances"][0]

    return {
        "instance_id": instance_id,
        "metadata_options": instance.get("MetadataOptions", {})
    }

def modify_metadata_options(
    *,
    instance_id: str,
    http_tokens: Optional[str] = None,
    http_endpoint: Optional[str] = None,
    http_put_response_hop_limit: Optional[int] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    req = {"InstanceId": instance_id}

    if http_tokens:
        req["HttpTokens"] = http_tokens

    if http_endpoint:
        req["HttpEndpoint"] = http_endpoint

    if http_put_response_hop_limit is not None:
        req["HttpPutResponseHopLimit"] = http_put_response_hop_limit

    return ec2.modify_instance_metadata_options(**req)

EC2_DISPATCH_REGISTRY = {
    "get_user_data": {
        "fn": get_user_data,
        "schema": GetUserDataParams,
    },
    "describe_metadata_options": {
        "fn": describe_metadata_options,
        "schema": DescribeMetadataOptionsParams,
    },
    "modify_metadata_options": {
        "fn": modify_metadata_options,
        "schema": ModifyMetadataOptionsParams,
    },
}
