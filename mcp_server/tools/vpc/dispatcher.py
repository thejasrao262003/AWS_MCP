from fastmcp.tools import FunctionTool
from mcp_server.tools.vpc.helper_functions.describe_vpc import VPC_REGISTRY

def aws_vpc_dispatcher(action: str, **kwargs):
    if action not in VPC_REGISTRY:
        return {"error": f"Unknown VPC action '{action}'"}

    fn = VPC_REGISTRY[action]["fn"]
    schema = VPC_REGISTRY[action]["schema"]

    # Schema validation
    try:
        validated = schema(**kwargs)
    except Exception as e:
        return {"validation_error": str(e)}

    return fn(**validated.model_dump())

aws_vpc_tool = FunctionTool(
    name="aws_vpc",
    description="Unified VPC dispatcher for all VPC & subnet actions.",
    fn=aws_vpc_dispatcher,
    parameters={
        "type": "object",
        "properties": {
            "action": {"type": "string"},
        },
        "required": ["action"],
        "additionalProperties": True,
    }
)
