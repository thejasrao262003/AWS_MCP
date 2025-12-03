import importlib
import pkgutil
from fastmcp.tools import FunctionTool


def load_ec2_registry():
    """
    Auto-discovers all EC2 action modules inside:
        mcp_server.tools.ec2.helper_functions
    and merges their EC2_DISPATCH_REGISTRY dictionaries.
    """
    registry = {}

    base_package = "mcp_server.tools.ec2.helper_functions"

    # Load the helper_functions package
    package = importlib.import_module(base_package)

    # Iterate inside helper_functions directory
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        # Skip __init__
        if module_name == "__init__":
            continue

        module_path = f"{base_package}.{module_name}"
        module = importlib.import_module(module_path)

        # Collect registry blocks
        if hasattr(module, "EC2_DISPATCH_REGISTRY"):
            reg = getattr(module, "EC2_DISPATCH_REGISTRY")
            if isinstance(reg, dict):
                registry.update(reg)

    return registry


# Load registry once at import time
EC2_REGISTRY = load_ec2_registry()


def aws_ec2_dispatcher(action: str, **kwargs):
    """
    Unified EC2 dispatcher.
    It receives:
        - action: str
        - kwargs: dict (validated by schema)
    Then dispatches into helper_functions.* automatically.
    """
    if action not in EC2_REGISTRY:
        return {"error": f"Unknown EC2 action '{action}'"}

    fn = EC2_REGISTRY[action]["fn"]
    schema = EC2_REGISTRY[action]["schema"]

    # Schema validation
    try:
        validated = schema(**kwargs)
    except Exception as e:
        return {"validation_error": str(e)}

    # Execute underlying function
    return fn(**validated.model_dump())


aws_ec2_tool = FunctionTool(
    name="aws_ec2",
    description="Unified EC2 dispatcher (auto-discovers actions from helper_functions).",
    fn=aws_ec2_dispatcher,
    parameters={
        "type": "object",
        "properties": {
            "action": {"type": "string"},
        },
        "required": ["action"],
        "additionalProperties": True,
    },
)
