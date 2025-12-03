"""
EC2 Module

This module exposes both:
1. The unified EC2 dispatcher tool (aws_ec2)
2. Individual EC2 action tools auto-generated from helper_functions

All individual EC2 operations are located inside:

    mcp_server.tools.ec2.helper_functions

They are discovered dynamically and exposed as separate tools.
"""

from .dispatcher import aws_ec2_tool, EC2_REGISTRY
from fastmcp.tools import FunctionTool

# Generate individual tools from the registry
individual_tools = []

for action_name, action_config in EC2_REGISTRY.items():
    fn = action_config["fn"]
    schema = action_config["schema"]
    
    # Create a wrapper that validates with schema
    def make_tool_fn(action_fn, action_schema):
        def tool_fn(**kwargs):
            try:
                validated = action_schema(**kwargs)
                return action_fn(**validated.model_dump())
            except Exception as e:
                return {"error": str(e)}
        return tool_fn
    
    # Build parameter schema from Pydantic model
    properties = {}
    required = []
    
    for field_name, field_info in schema.model_fields.items():
        field_type = "string"  # Default to string for simplicity
        properties[field_name] = {
            "type": field_type,
            "description": field_info.description or f"{field_name} parameter"
        }
        if field_info.is_required():
            required.append(field_name)
    
    # Create individual tool
    tool = FunctionTool(
        name=f"ec2_{action_name}",
        description=fn.__doc__ or f"EC2 action: {action_name}",
        fn=make_tool_fn(fn, schema),
        parameters={
            "type": "object",
            "properties": properties,
            "required": required,
        }
    )
    individual_tools.append(tool)

# Tools exposed by EC2 service: dispatcher + individual tools
tools = [aws_ec2_tool] + individual_tools

__all__ = ["tools", "aws_ec2_tool"]
