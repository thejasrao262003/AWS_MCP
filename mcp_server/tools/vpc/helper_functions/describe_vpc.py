# mcp_server/tools/ec2/vpc_tools.py

import boto3
from fastmcp.tools import FunctionTool
from typing import Optional

from mcp_server.models.vpc.describe_vpc import (
    RegionOnlyParams,
    DescribeVpcParams,
    DescribeSubnetParams
)

# ============================================================
# LIST ALL VPCS
# ============================================================

def list_vpcs(*, region: str = "ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)
    resp = ec2.describe_vpcs()
    return {
        "region": region,
        "vpcs": resp.get("Vpcs", [])
    }


# ============================================================
# GET DEFAULT VPC
# ============================================================

def get_default_vpc(*, region: str = "ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)
    resp = ec2.describe_vpcs(
        Filters=[{"Name": "isDefault", "Values": ["true"]}]
    )

    vpcs = resp.get("Vpcs", [])
    return {
        "region": region,
        "default_vpc": vpcs[0] if vpcs else None
    }


# ============================================================
# DESCRIBE SPECIFIC VPC
# ============================================================

def describe_vpc(*, vpc_id: Optional[str] = None, region: str = "ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)

    if vpc_id:
        resp = ec2.describe_vpcs(VpcIds=[vpc_id])
    else:
        resp = ec2.describe_vpcs()

    return {
        "region": region,
        "vpcs": resp.get("Vpcs", [])
    }


# ============================================================
# LIST SUBNETS
# ============================================================

def list_subnets(*, region: str = "ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)
    resp = ec2.describe_subnets()
    return {
        "region": region,
        "subnets": resp.get("Subnets", [])
    }


# ============================================================
# GET ALL SUBNETS IN DEFAULT VPC
# ============================================================

def get_default_subnets(*, region: str = "ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)

    # Fetch default VPC
    vpcs = ec2.describe_vpcs(
        Filters=[{"Name": "isDefault", "Values": ["true"]}]
    ).get("Vpcs", [])

    if not vpcs:
        return {
            "region": region,
            "error": "Default VPC not found",
            "subnets": []
        }

    default_vpc_id = vpcs[0]["VpcId"]

    resp = ec2.describe_subnets(
        Filters=[{"Name": "vpc-id", "Values": [default_vpc_id]}]
    )

    return {
        "region": region,
        "default_vpc_id": default_vpc_id,
        "subnets": resp.get("Subnets", [])
    }


# ============================================================
# DESCRIBE SPECIFIC SUBNET OR FILTER BY VPC
# ============================================================

def describe_subnet(
    *,
    subnet_id: Optional[str] = None,
    vpc_id: Optional[str] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    filters = []
    if vpc_id:
        filters.append({"Name": "vpc-id", "Values": [vpc_id]})

    if subnet_id:
        resp = ec2.describe_subnets(SubnetIds=[subnet_id])
    else:
        resp = ec2.describe_subnets(Filters=filters or None)

    return {
        "region": region,
        "subnets": resp.get("Subnets", [])
    }


VPC_REGISTRY = {
    "list_vpcs": {
        "fn": list_vpcs,
        "schema": RegionOnlyParams
    },
    "get_default_vpc": {
        "fn": get_default_vpc,
        "schema": RegionOnlyParams
    },
    "describe_vpc": {
        "fn": describe_vpc,
        "schema": DescribeVpcParams
    },
    "list_subnets": {
        "fn": list_subnets,
        "schema": RegionOnlyParams
    },
    "get_default_subnets": {
        "fn": get_default_subnets,
        "schema": RegionOnlyParams
    },
    "describe_subnet": {
        "fn": describe_subnet,
        "schema": DescribeSubnetParams
    },
}
