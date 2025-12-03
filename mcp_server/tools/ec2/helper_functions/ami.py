import boto3
from fastmcp.tools import FunctionTool
from typing import Dict, Any, Optional, List

# Import request schemas
from mcp_server.models.ec2.ami import (
    CreateAMIParams,
    DescribeImagesParams,
    DeregisterAMIParams,
    GetLatestAMIParams,
)


def create_ami(
    *,
    instance_id: str,
    name: str,
    no_reboot: bool = True,
    description: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    req: Dict[str, Any] = {
        "InstanceId": instance_id,
        "Name": name,
        "NoReboot": no_reboot,
    }

    if description:
        req["Description"] = description

    if tags:
        req["TagSpecifications"] = [
            {
                "ResourceType": "image",
                "Tags": [{"Key": k, "Value": v} for k, v in tags.items()],
            }
        ]

    resp = ec2.create_image(**req)

    return {
        "image_id":resp["ImageId"],
        "state":"created",
        "name":name,
        "tags":[{"Key": k, "Value": v} for k, v in (tags or {}).items()]
    }


def describe_images(
    *,
    owners: Optional[List[str]] = None,
    image_ids: Optional[List[str]] = None,
    filters: Optional[List[Dict[str, Any]]] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    req: Dict[str, Any] = {}

    if owners:
        req["Owners"] = owners
    if image_ids:
        req["ImageIds"] = image_ids
    if filters:
        req["Filters"] = filters

    resp = ec2.describe_images(**req)

    return DescribeImagesResponse(
        images=resp.get("Images", [])
    )


def deregister_ami(
    *,
    image_id: str,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    ec2.deregister_image(ImageId=image_id)

    return {
        "image_id": image_id,
        "state": "deregistered"
    }


def get_latest_ami(
    *,
    os_type: str,
    region: str = "ap-south-1",
    architecture: str = "x86_64"
):
    ec2 = boto3.client("ec2", region_name=region)

    # SAME os_filters dictionary as before…
    os_filters = {
        "ubuntu": {
            "owners": ["099720109477"],
            "filters": [
                {"Name": "name", "Values": ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-*"]},
                {"Name": "architecture", "Values": [architecture]},
                {"Name": "state", "Values": ["available"]},
                {"Name": "virtualization-type", "Values": ["hvm"]},
            ]
        },
        "amazon-linux-2": {
            "owners": ["amazon"],
            "filters": [
                {"Name": "name", "Values": ["amzn2-ami-hvm-*-gp2"]},
                {"Name": "architecture", "Values": [architecture]},
                {"Name": "state", "Values": ["available"]},
                {"Name": "virtualization-type", "Values": ["hvm"]},
            ]
        },
        # ...rest unchanged...
        "amazon-linux-2023": {
            "owners": ["amazon"],
            "filters": [
                {"Name": "name", "Values": ["al2023-ami-*"]},
                {"Name": "architecture", "Values": [architecture]},
                {"Name": "state", "Values": ["available"]},
                {"Name": "virtualization-type", "Values": ["hvm"]},
            ]
        },
        "windows-2022": {
            "owners": ["amazon"],
            "filters": [
                {"Name": "name", "Values": ["Windows_Server-2022-English-Full-Base-*"]},
                {"Name": "architecture", "Values": [architecture]},
                {"Name": "state", "Values": ["available"]},
                {"Name": "virtualization-type", "Values": ["hvm"]},
            ]
        },
        "windows-2019": {
            "owners": ["amazon"],
            "filters": [
                {"Name": "name", "Values": ["Windows_Server-2019-English-Full-Base-*"]},
                {"Name": "architecture", "Values": [architecture]},
                {"Name": "state", "Values": ["available"]},
                {"Name": "virtualization-type", "Values": ["hvm"]},
            ]
        },
        "debian": {
            "owners": ["136693071363"],
            "filters": [
                {"Name": "name", "Values": ["debian-12-*"]},
                {"Name": "architecture", "Values": [architecture]},
                {"Name": "state", "Values": ["available"]},
                {"Name": "virtualization-type", "Values": ["hvm"]},
            ]
        },
        "rhel": {
            "owners": ["309956199498"],
            "filters": [
                {"Name": "name", "Values": ["RHEL-9.*_HVM-*"]},
                {"Name": "architecture", "Values": [architecture]},
                {"Name": "state", "Values": ["available"]},
                {"Name": "virtualization-type", "Values": ["hvm"]},
            ]
        },
        "suse": {
            "owners": ["013907871322"],
            "filters": [
                {"Name": "name", "Values": ["suse-sles-15-*"]},
                {"Name": "architecture", "Values": [architecture]},
                {"Name": "state", "Values": ["available"]},
                {"Name": "virtualization-type", "Values": ["hvm"]},
            ]
        },
    }

    os_type_lower = os_type.lower()

    if os_type_lower not in os_filters:
        raise ValueError(f"Unsupported OS type: {os_type}")

    cfg = os_filters[os_type_lower]

    resp = ec2.describe_images(Owners=cfg["owners"], Filters=cfg["filters"])

    images = resp.get("Images", [])
    if not images:
        return {
            "ami_id":"",
            "name":"",
            "description":"No AMI found",
            "creation_date":"",
            "os_type":os_type,
            "region":region,
            "architecture":architecture,
            "owner_id":""
        }

    latest = sorted(images, key=lambda x: x["CreationDate"], reverse=True)[0]

    return {
        "ami_id":latest["ImageId"],
        "name":latest["Name"],
        "description":latest.get("Description", ""),
        "creation_date":latest["CreationDate"],
        "os_type":os_type,
        "region":region,
        "architecture":architecture,
        "owner_id":latest["OwnerId"]
    }
    
EC2_DISPATCH_REGISTRY = {
    "create_ami": {
        "fn": create_ami,
        "schema": CreateAMIParams,
    },
    "describe_images": {
        "fn": describe_images,
        "schema": DescribeImagesParams,
    },
    "deregister_ami": {
        "fn": deregister_ami,
        "schema": DeregisterAMIParams,
    },
    "get_latest_ami": {
        "fn": get_latest_ami,
        "schema": GetLatestAMIParams,
    },
}
