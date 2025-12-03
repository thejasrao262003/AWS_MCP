from fastmcp.resources import FunctionResource

ec2_pricing_resource = FunctionResource.from_function(
    fn=lambda: {
        "service": "EC2",
        "domain": "pricing",
        "description": (
            "Query AWS EC2 on-demand pricing, spot pricing history, and monthly cost estimates. "
            "Use the aws_ec2 dispatcher tool with the actions below."
        ),

        "actions": {
            "get_ondemand_price": {
                "description": (
                    "Retrieve real-time on-demand pricing for an EC2 instance type in a given region. "
                    "Returns both hourly and monthly cost."
                ),
                "required_params": ["instance_type"],
                "optional_params": ["operating_system", "region"],
                "example": {
                    "action": "get_ondemand_price",
                    "instance_type": "t3.micro",
                    "region": "ap-south-1"
                }
            },

            "get_spot_price_history": {
                "description": (
                    "Retrieve historical spot pricing data for a given instance type. "
                    "You may also filter by time range or an availability zone."
                ),
                "required_params": ["instance_type"],
                "optional_params": [
                    "product_description",
                    "start_time",
                    "end_time",
                    "availability_zone",
                    "region"
                ],
                "example": {
                    "action": "get_spot_price_history",
                    "instance_type": "t3.large",
                    "availability_zone": "ap-south-1a"
                }
            },

            "estimate_instance_cost": {
                "description": (
                    "Estimate monthly EC2 cost using on-demand pricing. "
                    "Defaults to 730 hours/month unless specified."
                ),
                "required_params": ["instance_type"],
                "optional_params": ["hours_per_month", "operating_system", "region"],
                "example": {
                    "action": "estimate_instance_cost",
                    "instance_type": "t3.micro",
                    "hours_per_month": 100
                }
            }
        },

        "notes": [
            "On-demand pricing uses the AWS Pricing API (always queried via us-east-1).",
            "Spot pricing fluctuates by AZ, OS, market supply, and time.",
            "Monthly cost estimation is based on hourly on-demand price × hours_per_month.",
            "Region mapping automatically converts region → AWS pricing location name.",
            "All pricing operations must be routed via the aws_ec2 dispatcher."
        ]
    },

    uri="resource://aws/ec2/pricing",
    name="ec2_pricing_resource",
    mime_type="application/json"
)
