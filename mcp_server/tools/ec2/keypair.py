import boto3
from typing import Dict, Any
from pathlib import Path
import stat
from fastmcp.tools import FunctionTool
from mcp_server.models.ec2 import (
    CreateKeyPairParams,
    DeleteKeyPairParams,
    ListKeyPairsParams
)

def create_keypair(region: str, key_name: str) -> Dict[str, Any]:
    """
    Creates an EC2 KeyPair and returns the PEM material.
    """
    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.create_key_pair(KeyName=key_name)
        return {
            "key_name": resp["KeyName"],
            "key_type": resp.get("KeyType", "rsa"),
            "key_material": resp["KeyMaterial"],
        }

    except Exception as e:
        return {"error": str(e), "key_name": key_name}


def delete_keypair(region: str, key_name: str) -> Dict[str, Any]:
    """
    Deletes an EC2 KeyPair.
    """
    ec2 = boto3.client("ec2", region_name=region)

    try:
        ec2.delete_key_pair(KeyName=key_name)
        return {
            "deleted": True,
            "key_name": key_name,
        }

    except Exception as e:
        return {"error": str(e), "key_name": key_name}


def list_keypairs(region: str) -> Dict[str, Any]:
    """
    Returns all key pairs in the region.
    """
    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.describe_key_pairs()
        pairs = []

        for kp in resp.get("KeyPairs", []):
            pairs.append({
                "key_name": kp["KeyName"],
                "key_type": kp.get("KeyType"),
                "fingerprint": kp.get("KeyFingerprint"),
            })

        return {"region": region, "keypairs": pairs}

    except Exception as e:
        return {"error": str(e), "region": region}

def save_pem_file(key_name: str, pem_data: str) -> str:
    """
    Saves key material to ~/.aws/mcp_keys/<key_name>.pem
    with secure permissions (chmod 600).
    """

    base_dir = Path.home() / ".aws" / "mcp_keys"
    base_dir.mkdir(parents=True, exist_ok=True)

    pem_path = base_dir / f"{key_name}.pem"

    with open(pem_path, "w") as pem_file:
        pem_file.write(pem_data)

    # chmod 600 — required for SSH usage
    pem_path.chmod(stat.S_IRUSR | stat.S_IWUSR)

    return str(pem_path)

tools = [
    FunctionTool(
        name="aws.create_keypair",
        description="Create an EC2 KeyPair and optionally save the PEM file locally.",
        fn=create_keypair,
        parameters=CreateKeyPairParams.model_json_schema(),
    ),
    FunctionTool(
        name="aws.delete_keypair",
        description="Delete an EC2 KeyPair by name.",
        fn=delete_keypair,
        parameters=DeleteKeyPairParams.model_json_schema(),
    ),
    FunctionTool(
        name="aws.list_keypairs",
        description="List all EC2 KeyPairs in a region.",
        fn=list_keypairs,
        parameters=ListKeyPairsParams.model_json_schema(),
    ),
]