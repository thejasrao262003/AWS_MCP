"""
EBS Module

This module exposes both:
1. The unified EBS dispatcher tool (aws_ebs)
2. Individual EBS action tools auto-generated from helper_functions

All individual EBS operations are located inside:

    mcp_server.tools.ebs.helper_functions

They are discovered dynamically and exposed as separate tools.
"""

from .dispatcher import aws_ebs_tool, EBS_REGISTRY
from fastmcp.tools import FunctionTool

# Generate individual tools from the registry
individual_tools = []

for action_name, action_config in EBS_REGISTRY.items():
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
        name=f"ebs_{action_name}",
        description=fn.__doc__ or f"EBS action: {action_name}",
        fn=make_tool_fn(fn, schema),
        parameters={
            "type": "object",
            "properties": properties,
            "required": required,
        }
    )
    individual_tools.append(tool)

# Tools exposed by EBS service: dispatcher + individual tools
tools = [aws_ebs_tool] + individual_tools

__all__ = ["tools", "aws_ebs_tool"]
