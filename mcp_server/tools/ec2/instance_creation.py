from mcp_server.models.ec2 import (
    CreateInstanceParams,
    CreateInstanceMinimalParams,
    InstanceSSHInstructionParams,
    CreateSpotInstanceParams
)
import boto3
import os

DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

def create_instance(params: CreateInstanceParams):
    region = params.region or DEFAULT_REGION
    ec2 = boto3.client("ec2", region_name=region)

    payload = {
        "ImageId": params.ImageId,
        "InstanceType": params.InstanceType,
        "MinCount": params.MinCount,
        "MaxCount": params.MaxCount,
    }

    if params.KeyName:
        payload["KeyName"] = params.KeyName

    if params.SubnetId:
        payload["SubnetId"] = params.SubnetId

    if params.SecurityGroupIds:
        payload["SecurityGroupIds"] = params.SecurityGroupIds

    if params.BlockDeviceMappings:
        payload["BlockDeviceMappings"] = [
            bd.model_dump(exclude_none=True)
            for bd in params.BlockDeviceMappings
        ]

    if params.NetworkInterfaces:
        payload["NetworkInterfaces"] = [
            ni.model_dump(exclude_none=True)
            for ni in params.NetworkInterfaces
        ]

    if params.TagSpecifications:
        payload["TagSpecifications"] = params.TagSpecifications

    if params.IamInstanceProfile:
        payload["IamInstanceProfile"] = params.IamInstanceProfile

    if params.MetadataOptions:
        payload["MetadataOptions"] = params.MetadataOptions

    if params.UserData:
        payload["UserData"] = params.UserData

    if params.ExtraParams:
        payload.update(params.ExtraParams)

    try:
        resp = ec2.run_instances(**payload)
        inst = resp["Instances"][0]

        return {
            "region": region,
            "instance_id": inst["InstanceId"],
            "instance_type": inst["InstanceType"],
            "state": inst["State"]["Name"],
        }

    except Exception as e:
        return {"error": str(e)}

def create_instance_minimal(params: CreateInstanceMinimalParams):
    region = params.region or DEFAULT_REGION
    ec2 = boto3.client("ec2", region_name=region)

    try:
        payload = {
            "ImageId": params.ImageId,
            "InstanceType": params.InstanceType,
            "MinCount": 1,
            "MaxCount": 1,
        }

        if params.KeyName:
            payload["KeyName"] = params.KeyName

        if params.SecurityGroupIds:
            payload["SecurityGroupIds"] = params.SecurityGroupIds

        if params.SubnetId:
            payload["SubnetId"] = params.SubnetId

        if params.TagSpecifications:
            payload["TagSpecifications"] = params.TagSpecifications

        resp = ec2.run_instances(**payload)
        inst = resp["Instances"][0]

        return {
            "region": region,
            "instance_id": inst["InstanceId"],
            "public_ip": inst.get("PublicIpAddress"),
            "state": inst["State"]["Name"]
        }

    except Exception as e:
        return {"error": str(e)}

def create_spot_instance(params: CreateSpotInstanceParams):
    region = params.region or DEFAULT_REGION
    ec2 = boto3.client("ec2", region_name=region)

    launch_spec = {
        "ImageId": params.ImageId,
        "InstanceType": params.InstanceType,
    }

    if params.KeyName:
        launch_spec["KeyName"] = params.KeyName

    if params.SecurityGroupIds:
        launch_spec["SecurityGroupIds"] = params.SecurityGroupIds

    if params.SubnetId:
        launch_spec["SubnetId"] = params.SubnetId

    if params.BlockDeviceMappings:
        launch_spec["BlockDeviceMappings"] = [
            bd.model_dump(exclude_none=True)
            for bd in params.BlockDeviceMappings
        ]

    if params.NetworkInterfaces:
        launch_spec["NetworkInterfaces"] = [
            ni.model_dump(exclude_none=True)
            for ni in params.NetworkInterfaces
        ]

    if params.TagSpecifications:
        launch_spec["TagSpecifications"] = params.TagSpecifications

    if params.IamInstanceProfile:
        launch_spec["IamInstanceProfile"] = params.IamInstanceProfile

    if params.MetadataOptions:
        launch_spec["MetadataOptions"] = params.MetadataOptions

    if params.UserData:
        launch_spec["UserData"] = params.UserData

    if params.ExtraParams:
        launch_spec.update(params.ExtraParams)

    try:
        resp = ec2.request_spot_instances(
            LaunchSpecification=launch_spec,
            InstanceCount=1,
            Type="one-time",
            MaxPrice=params.MaxPrice,
        )

        sir = resp["SpotInstanceRequests"][0]

        return {
            "region": region,
            "spot_request_id": sir["SpotInstanceRequestId"],
            "state": sir["State"],
        }

    except Exception as e:
        return {"error": str(e)}
    
def generate_instance_ssh_instruction(params: InstanceSSHInstructionParams):
    region = params.region or DEFAULT_REGION
    ec2 = boto3.client("ec2", region_name=region)

    try:
        resp = ec2.describe_instances(InstanceIds=[params.instance_id])
        inst = resp["Reservations"][0]["Instances"][0]

        pub_ip = inst.get("PublicIpAddress")
        if not pub_ip:
            return {"error": "Instance has no public IP"}

        key_name = params.key_name or inst.get("KeyName")
        if not key_name:
            return {"error": "No KeyPair associated with instance"}

        pem_path = params.pem_path or f"~/{key_name}.pem"

        # Best-effort username guess
        ami = inst["ImageId"]
        if "ubuntu" in ami.lower():
            user = "ubuntu"
        elif "amazon" in ami.lower() or "amzn" in ami.lower():
            user = "ec2-user"
        else:
            user = "ec2-user"

        ssh_command = f"ssh -i {pem_path} {user}@{pub_ip}"

        return {
            "instance_id": params.instance_id,
            "region": region,
            "public_ip": pub_ip,
            "key_name": key_name,
            "pem_path": pem_path,
            "recommended_user": user,
            "ssh_command": ssh_command
        }

    except Exception as e:
        return {"error": str(e)}