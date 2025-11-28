import boto3
import os

DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

def list_ec2_instances(region: str = DEFAULT_REGION):
    ec2 = boto3.client("ec2", region_name=region)
    resp = ec2.describe_instances()

    instances = []
    for r in resp.get("Reservations", []):
        for inst in r.get("Instances", []):
            instances.append(inst)

    return {
        "region": region,
        "instances": instances
    }
