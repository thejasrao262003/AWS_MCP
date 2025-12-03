# mcp_server/tools/ec2/pricing_tools.py

import boto3
import json
from fastmcp.tools import FunctionTool
from botocore.exceptions import ClientError
from typing import Optional
from datetime import datetime

from mcp_server.models.ec2.pricing import (
    EC2OnDemandPriceParams,
    SpotPriceHistoryParams,
    EC2CostEstimateParams
)

AWS_PRICING_REGION_MAP = {
    "us-east-1": "US East (N. Virginia)",
    "us-east-2": "US East (Ohio)",
    "us-west-1": "US West (N. California)",
    "us-west-2": "US West (Oregon)",

    "af-south-1": "Africa (Cape Town)",
    "ap-east-1": "Asia Pacific (Hong Kong)",
    "ap-south-1": "Asia Pacific (Mumbai)",
    "ap-south-2": "Asia Pacific (Hyderabad)",
    "ap-southeast-1": "Asia Pacific (Singapore)",
    "ap-southeast-2": "Asia Pacific (Sydney)",
    "ap-southeast-3": "Asia Pacific (Jakarta)",
    "ap-southeast-4": "Asia Pacific (Melbourne)",
    "ap-northeast-1": "Asia Pacific (Tokyo)",
    "ap-northeast-2": "Asia Pacific (Seoul)",
    "ap-northeast-3": "Asia Pacific (Osaka)",

    "ca-central-1": "Canada (Central)",
    "ca-west-1": "Canada West (Calgary)",

    "eu-central-1": "EU (Frankfurt)",
    "eu-central-2": "EU (Zurich)",
    "eu-west-1": "EU (Ireland)",
    "eu-west-2": "EU (London)",
    "eu-west-3": "EU (Paris)",
    "eu-north-1": "EU (Stockholm)",
    "eu-south-1": "EU (Milan)",
    "eu-south-2": "EU (Spain)",

    "me-south-1": "Middle East (Bahrain)",
    "me-central-1": "Middle East (UAE)",

    "sa-east-1": "South America (São Paulo)",

    "us-gov-east-1": "AWS GovCloud (US-East)",
    "us-gov-west-1": "AWS GovCloud (US-West)"
}

def get_ondemand_price(
    *, 
    instance_type: str, 
    operating_system: str = "Linux",
    region: str = "ap-south-1"
):

    pricing = boto3.client("pricing", region_name="us-east-1")

    region_name = AWS_PRICING_REGION_MAP.get(region)
    if not region_name:
        return {"error": f"Region {region} not supported for pricing API"}

    filters = [
        {"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance_type},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region_name},
        {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": operating_system},
        {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": "NA"},
        {"Type": "TERM_MATCH", "Field": "capacitystatus", "Value": "Used"},
    ]

    resp = pricing.get_products(ServiceCode="AmazonEC2", Filters=filters)

    if not resp["PriceList"]:
        return {"error": "No pricing data available"}

    price_item = json.loads(resp["PriceList"][0])

    # Get the OnDemand price per hour
    on_demand_terms = next(iter(price_item["terms"]["OnDemand"].values()))
    price_dimension = next(iter(on_demand_terms["priceDimensions"].values()))
    price_per_hour = float(price_dimension["pricePerUnit"]["USD"])

    return {
        "instance_type": instance_type,
        "operating_system": operating_system,
        "region": region,
        "price_per_hour_usd": price_per_hour,
        "price_per_month_usd": round(price_per_hour * 720, 2),
    }


def get_spot_price_history(
    *,
    instance_type: str,
    product_description: str = "Linux/UNIX",
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    availability_zone: Optional[str] = None,
    region: str = "ap-south-1"
):
    ec2 = boto3.client("ec2", region_name=region)

    req = {
        "InstanceTypes": [instance_type],
        "ProductDescriptions": [product_description],
    }

    if start_time:
        req["StartTime"] = start_time

    if end_time:
        req["EndTime"] = end_time

    if availability_zone:
        req["AvailabilityZone"] = availability_zone

    resp = ec2.describe_spot_price_history(**req)

    history = [
        {
            "timestamp": h["Timestamp"].isoformat(),
            "spot_price": h["SpotPrice"],
            "instance_type": h["InstanceType"],
            "az": h["AvailabilityZone"]
        }
        for h in resp["SpotPriceHistory"]
    ]

    return {
        "instance_type": instance_type,
        "region": region,
        "history_count": len(history),
        "history": history,
    }

def estimate_instance_cost(
    *,
    instance_type: str,
    operating_system: str = "Linux",
    hours_per_month: int = 730,
    region: str = "ap-south-1"
):
    price_info = get_ondemand_price(
        instance_type=instance_type,
        operating_system=operating_system,
        region=region
    )

    if "error" in price_info:
        return price_info

    hourly = price_info["price_per_hour_usd"]
    monthly = hourly * hours_per_month

    return {
        "instance_type": instance_type,
        "hours_per_month": hours_per_month,
        "price_per_hour_usd": hourly,
        "estimated_cost_usd": round(monthly, 2)
    }
    
EC2_DISPATCH_REGISTRY = {
    "get_ondemand_price": {
        "fn": get_ondemand_price,
        "schema": EC2OnDemandPriceParams,
    },
    "get_spot_price_history": {
        "fn": get_spot_price_history,
        "schema": SpotPriceHistoryParams,
    },
    "estimate_instance_cost": {
        "fn": estimate_instance_cost,
        "schema": EC2CostEstimateParams,
    },
}
