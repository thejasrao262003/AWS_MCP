from fastmcp.tools import FunctionTool
from mcp_server.models.ec2 import (
    ListEC2Params,
    GetInstanceDetailsParams,
    ListEC2ParamsTagwise,
    ListSpotRequestsParams,
    GetSpotRequestDetailsParams,
    CancelSpotRequestParams
)
import boto3
import os
from typing import Dict, Any, List, Optional

DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# -------------------------
# TOOL FUNCTION 1 — LIST EC2
# -------------------------
def list_ec2_instances(
    *,
    region: Optional[str] = None,
    instance_ids: Optional[List[str]] = None,
    states: Optional[List[str]] = None,
    tag_key: Optional[str] = None,
    tag_value: Optional[str] = None,
    instance_types: Optional[List[str]] = None,
    vpc_ids: Optional[List[str]] = None,
    subnet_ids: Optional[List[str]] = None,
    security_group_ids: Optional[List[str]] = None,
    spot_only: bool = False,
    exclude_spot: bool = False,
    spot_request_id: Optional[str] = None,
    custom_filters: Optional[List[Dict[str, Any]]] = None,
):
    if not region:
        region = DEFAULT_REGION

    ec2 = boto3.client("ec2", region_name=region)
    filters = []

    # ---- Standard Filters ----
    if states:
        filters.append({"Name": "instance-state-name", "Values": states})

    if instance_types:
        filters.append({"Name": "instance-type", "Values": instance_types})

    if vpc_ids:
        filters.append({"Name": "vpc-id", "Values": vpc_ids})

    if subnet_ids:
        filters.append({"Name": "subnet-id", "Values": subnet_ids})

    if security_group_ids:
        filters.append({"Name": "instance.group-id", "Values": security_group_ids})

    if tag_key and tag_value:
        filters.append({"Name": f"tag:{tag_key}", "Values": [tag_value]})

    # ---- Spot Filters ----
    if spot_only:
        filters.append({"Name": "instance-lifecycle", "Values": ["spot"]})

    if exclude_spot:
        filters.append({"Name": "instance-lifecycle", "Values": ["on-demand"]})

    if spot_request_id:
        filters.append({"Name": "spot-instance-request-id", "Values": [spot_request_id]})

    # ---- Custom ----
    if custom_filters:
        filters.extend(custom_filters)

    # ---- Query AWS ----
    try:
        if instance_ids:
            resp = ec2.describe_instances(InstanceIds=instance_ids, Filters=filters) if filters else ec2.describe_instances(InstanceIds=instance_ids)
        else:
            resp = ec2.describe_instances(Filters=filters) if filters else ec2.describe_instances()

        instances = []
        for res in resp.get("Reservations", []):
            instances.extend(res.get("Instances", []))

        return {
            "region": region,
            "filters_applied": filters,
            "instances": instances,
        }

    except Exception as e:
        return {"region": region, "error": str(e)}


# -------------------------
# TOOL FUNCTION 2 — GET DETAILS
# -------------------------
def get_instance_details(*, instance_id: str, region: str = None):
    if not region:
        region = DEFAULT_REGION

    ec2 = boto3.client("ec2", region_name=region)

    resp = ec2.describe_instances(InstanceIds=[instance_id])
    reservations = resp.get("Reservations", [])

    if not reservations or not reservations[0].get("Instances"):
        return {
            "instance_id": instance_id,
            "region": region,
            "details": None,
            "error": f"Instance {instance_id} not found"
        }

    return {
        "instance_id": instance_id,
        "region": region,
        "details": reservations[0]["Instances"][0]
    }

def get_instance_status(*, instance_id: str, region: str = DEFAULT_REGION):
    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.describe_instances(InstanceIds=[instance_id])
        reservations = resp.get("Reservations", [])
        if not reservations:
            return {
                "instance_id": instance_id,
                "state": "not_found",
                "public_ip": None,
                "instance_type": None
            }

        inst = reservations[0]["Instances"][0]

        return {
            "instance_id": instance_id,
            "state": inst["State"]["Name"],
            "public_ip": inst.get("PublicIpAddress"),
            "instance_type": inst.get("InstanceType"),
            "launch_time": str(inst.get("LaunchTime")),
            "lifecycle": inst.get("InstanceLifecycle", "on-demand")
        }

    except Exception as e:
        return {"error": str(e), "instance_id": instance_id}
        
def list_running_instances(*, region: str = DEFAULT_REGION, spot_only: bool = False):
    filters = [
        {"Name": "instance-state-name", "Values": ["running"]}
    ]

    if spot_only:
        filters.append({"Name": "instance-lifecycle", "Values": ["spot"]})

    ec2 = boto3.client("ec2", region_name=region)
    resp = ec2.describe_instances(Filters=filters)

    instances = []
    for reservation in resp.get("Reservations", []):
        for inst in reservation.get("Instances", []):
            instances.append({
                "instance_id": inst["InstanceId"],
                "instance_type": inst["InstanceType"],
                "public_ip": inst.get("PublicIpAddress"),
                "private_ip": inst.get("PrivateIpAddress"),
                "state": inst["State"]["Name"],
                "tags": inst.get("Tags", []),
                "lifecycle": inst.get("InstanceLifecycle", "on-demand"),
                "launch_time": str(inst.get("LaunchTime"))
            })

    return instances


def list_instances_by_tag(*, tag_key: str, tag_value: str, region: str = DEFAULT_REGION, spot_only=False):
    filters = [
        {"Name": f"tag:{tag_key}", "Values": [tag_value]}
    ]

    if spot_only:
        filters.append({"Name": "instance-lifecycle", "Values": ["spot"]})

    ec2 = boto3.client("ec2", region_name=region)

    resp = ec2.describe_instances(Filters=filters)

    instances = []
    for reservation in resp.get("Reservations", []):
        for inst in reservation.get("Instances", []):
            instances.append({
                "instance_id": inst["InstanceId"],
                "instance_type": inst.get("InstanceType"),
                "public_ip": inst.get("PublicIpAddress"),
                "private_ip": inst.get("PrivateIpAddress"),
                "state": inst["State"]["Name"],
                "tags": inst.get("Tags", []),
                "lifecycle": inst.get("InstanceLifecycle", "on-demand"),
                "launch_time": str(inst.get("LaunchTime"))
            })

    return instances

def list_spot_requests(
    *,
    region: Optional[str] = None,
    spot_request_ids: Optional[List[str]] = None,
    states: Optional[List[str]] = None,
):
    """
    List all Spot Instance Requests (SIRs).
    """

    if not region:
        region = DEFAULT_REGION

    ec2 = boto3.client("ec2", region_name=region)

    filters = []
    if states:
        filters.append({"Name": "state", "Values": states})

    try:
        if spot_request_ids:
            resp = ec2.describe_spot_instance_requests(
                SpotInstanceRequestIds=spot_request_ids,
                Filters=filters
            ) if filters else ec2.describe_spot_instance_requests(
                SpotInstanceRequestIds=spot_request_ids
            )
        else:
            resp = ec2.describe_spot_instance_requests(Filters=filters) if filters else ec2.describe_spot_instance_requests()

        return {
            "region": region,
            "filters_applied": filters,
            "spot_requests": resp.get("SpotInstanceRequests", [])
        }

    except Exception as e:
        return {"region": region, "error": str(e)}
    
def get_spot_request_details(
    *,
    spot_request_id: str,
    region: Optional[str] = None
):
    """
    Fetch details of a specific Spot Instance Request.
    """

    if not region:
        region = DEFAULT_REGION

    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.describe_spot_instance_requests(
            SpotInstanceRequestIds=[spot_request_id]
        )

        if not resp.get("SpotInstanceRequests"):
            return {
                "spot_request_id": spot_request_id,
                "error": "Spot request not found",
                "region": region
            }

        return {
            "region": region,
            "spot_request_id": spot_request_id,
            "details": resp["SpotInstanceRequests"][0]
        }

    except Exception as e:
        return {
            "region": region,
            "spot_request_id": spot_request_id,
            "error": str(e)
        }
        
def cancel_spot_request(
    *,
    spot_request_id: str,
    region: Optional[str] = None
):
    """
    Cancel a Spot Instance Request.
    """

    if not region:
        region = DEFAULT_REGION

    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.cancel_spot_instance_requests(
            SpotInstanceRequestIds=[spot_request_id]
        )

        cancelled = resp.get("CancelledSpotInstanceRequests", [])

        return {
            "region": region,
            "spot_request_id": spot_request_id,
            "cancelled": cancelled
        }

    except Exception as e:
        return {
            "region": region,
            "spot_request_id": spot_request_id,
            "error": str(e)
        }

EC2_DISPATCH_REGISTRY = {

    # ------------ INSTANCE LISTING ------------
    "list_ec2_instances": {
        "fn": list_ec2_instances,
        "schema": ListEC2Params,
    },

    "get_instance_details": {
        "fn": get_instance_details,
        "schema": GetInstanceDetailsParams,
    },

    "get_instance_status": {
        "fn": get_instance_status,
        "schema": GetInstanceDetailsParams,
    },

    "list_running_instances": {
        "fn": list_running_instances,
        "schema": ListEC2Params,
    },

    "list_instances_by_tag": {
        "fn": list_instances_by_tag,
        "schema": ListEC2ParamsTagwise,
    },

    # ------------ SPOT REQUESTS ------------
    "list_spot_requests": {
        "fn": list_spot_requests,
        "schema": ListSpotRequestsParams,
    },

    "get_spot_request_details": {
        "fn": get_spot_request_details,
        "schema": GetSpotRequestDetailsParams,
    },

    "cancel_spot_request": {
        "fn": cancel_spot_request,
        "schema": CancelSpotRequestParams,
    },
}
