import boto3
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from fastmcp.tools import FunctionTool
from mcp_server.models.ec2 import (
    IpPermission,
    CreateSecurityGroupParams,
    DeleteSecurityGroupParams,
    ModifyRulesParams,
    DescribeSGParams,
    ListSGParams
)

def to_ip_permissions(rules: List[IpPermission]):
    """Convert Pydantic rules → Boto3 IpPermission structure"""
    perms = []
    for r in rules:
        perms.append({
            "IpProtocol": r.protocol,
            "FromPort": r.from_port,
            "ToPort": r.to_port,
            "IpRanges": [{"CidrIp": r.cidr}],
        })
    return perms

def create_security_group(
    region: str,
    group_name: str,
    description: str,
    vpc_id: str,
    inbound_rules: Optional[List[IpPermission]] = None,
) -> Dict[str, Any]:
    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id,
        )
        group_id = resp["GroupId"]
        if inbound_rules:
            ec2.authorize_security_group_ingress(
                GroupId=group_id,
                IpPermissions=to_ip_permissions(inbound_rules),
            )

        return {
            "group_name": group_name,
            "group_id": group_id,
            "inbound_rules_added": bool(inbound_rules),
        }

    except Exception as e:
        return {"error": str(e)}


def delete_security_group(region: str, group_id: str) -> Dict[str, Any]:
    ec2 = boto3.client("ec2", region_name=region)

    try:
        ec2.delete_security_group(GroupId=group_id)
        return {"deleted": True, "group_id": group_id}

    except Exception as e:
        return {"error": str(e), "group_id": group_id}


def authorize_rules(region: str, group_id: str, rules: List[IpPermission]):
    ec2 = boto3.client("ec2", region_name=region)

    try:
        ec2.authorize_security_group_ingress(
            GroupId=group_id,
            IpPermissions=to_ip_permissions(rules),
        )
        return {"authorized": True, "group_id": group_id, "rules_added": len(rules)}

    except Exception as e:
        return {"error": str(e), "group_id": group_id}


def revoke_rules(region: str, group_id: str, rules: List[IpPermission]):
    ec2 = boto3.client("ec2", region_name=region)

    try:
        ec2.revoke_security_group_ingress(
            GroupId=group_id,
            IpPermissions=to_ip_permissions(rules),
        )
        return {"revoked": True, "group_id": group_id, "rules_removed": len(rules)}

    except Exception as e:
        return {"error": str(e), "group_id": group_id}


def describe_security_group(region: str, group_id: str = None, group_name: str = None):
    ec2 = boto3.client("ec2", region_name=region)

    try:
        filters = []
        if group_id:
            filters.append({"Name": "group-id", "Values": [group_id]})
        if group_name:
            filters.append({"Name": "group-name", "Values": [group_name]})

        resp = ec2.describe_security_groups(Filters=filters) if filters else ec2.describe_security_groups()

        return {"security_groups": resp.get("SecurityGroups", [])}

    except Exception as e:
        return {"error": str(e)}


def list_security_groups(region: str):
    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.describe_security_groups()
        sgs = []

        for sg in resp.get("SecurityGroups", []):
            sgs.append({
                "group_id": sg["GroupId"],
                "group_name": sg["GroupName"],
                "description": sg.get("Description"),
                "vpc_id": sg.get("VpcId"),
                "inbound_rule_count": len(sg.get("IpPermissions", [])),
            })

        return {"region": region, "security_groups": sgs}

    except Exception as e:
        return {"error": str(e)}
    
EC2_DISPATCH_REGISTRY = {
    "create_security_group": {
        "fn": create_security_group,
        "schema": CreateSecurityGroupParams,
    },
    "delete_security_group": {
        "fn": delete_security_group,
        "schema": DeleteSecurityGroupParams,
    },
    "authorize_security_group_rules": {
        "fn": authorize_rules,
        "schema": ModifyRulesParams,
    },
    "revoke_security_group_rules": {
        "fn": revoke_rules,
        "schema": ModifyRulesParams,
    },
    "describe_security_group": {
        "fn": describe_security_group,
        "schema": DescribeSGParams,
    },
    "list_security_groups": {
        "fn": list_security_groups,
        "schema": ListSGParams,
    },
}
