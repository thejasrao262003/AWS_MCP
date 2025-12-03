import boto3
import os
from dotenv import load_dotenv
from fastmcp.tools import FunctionTool
from mcp_server.models.ec2 import (
    InstanceLifeCycleParams,
)

load_dotenv()

DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")

def start_instance(*, instance_id: str, region: str = DEFAULT_REGION) -> dict:
    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.start_instances(InstanceIds=[instance_id])
        state = resp["StartingInstances"][0]["CurrentState"]["Name"]

        return {"status": "success", "instance_id": instance_id, "state": state}

    except Exception as e:
        return {"status": "error", "instance_id": instance_id, "error": str(e)}

def stop_instance(*, instance_id: str, region: str = DEFAULT_REGION) -> dict:
    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.stop_instances(InstanceIds=[instance_id])
        state = resp["StoppingInstances"][0]["CurrentState"]["Name"]

        return {"status": "success", "instance_id": instance_id, "state": state}

    except Exception as e:
        return {"status": "error", "instance_id": instance_id, "error": str(e)}

def reboot_instance(*, instance_id: str, region: str = DEFAULT_REGION) -> dict:
    ec2 = boto3.client("ec2", region_name=region)

    try:
        ec2.reboot_instances(InstanceIds=[instance_id])

        return {
            "status": "success",
            "instance_id": instance_id,
            "message": "Reboot initiated"
        }

    except Exception as e:
        return {"status": "error", "instance_id": instance_id, "error": str(e)}

def hard_reboot_instance(*, instance_id: str, region: str = DEFAULT_REGION) -> dict:
    ec2 = boto3.client("ec2", region_name=region)

    try:
        ec2.reboot_instances(InstanceIds=[instance_id], Force=True)

        return {
            "status": "success",
            "instance_id": instance_id,
            "message": "Forced reboot initiated"
        }

    except Exception as e:
        return {"status": "error", "instance_id": instance_id, "error": str(e)}

def terminate_instance(*, instance_id: str, region: str = DEFAULT_REGION) -> dict:
    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.terminate_instances(InstanceIds=[instance_id])
        state = resp["TerminatingInstances"][0]["CurrentState"]["Name"]

        return {"status": "success", "instance_id": instance_id, "state": state}

    except Exception as e:
        return {"status": "error", "instance_id": instance_id, "error": str(e)}

EC2_DISPATCH_REGISTRY = {
    "start_instance": {
        "fn": start_instance,
        "schema": InstanceLifeCycleParams,
    },
    "stop_instance": {
        "fn": stop_instance,
        "schema": InstanceLifeCycleParams,
    },
    "reboot_instance": {
        "fn": reboot_instance,
        "schema": InstanceLifeCycleParams,
    },
    "hard_reboot_instance": {
        "fn": hard_reboot_instance,
        "schema": InstanceLifeCycleParams,
    },
    "terminate_instance": {
        "fn": terminate_instance,
        "schema": InstanceLifeCycleParams,
    },
}
