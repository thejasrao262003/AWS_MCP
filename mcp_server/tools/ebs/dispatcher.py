import importlib
import pkgutil
from fastmcp.tools import FunctionTool


def load_ebs_registry():
    """
    Auto-discovers all EBS action modules inside:
        mcp_server.tools.ebs.helper_functions
    and merges their EBS_DISPATCH_REGISTRY dictionaries.
    """
    registry = {}

    base_package = "mcp_server.tools.ebs.helper_functions"

    # Load main helper_functions package
    package = importlib.import_module(base_package)

    # Scan modules inside helper_functions/
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        if module_name == "__init__":
            continue

        module_path = f"{base_package}.{module_name}"
        module = importlib.import_module(module_path)

        # Each file should expose:  EBS_DISPATCH_REGISTRY = { "action": { fn, schema }}
        if hasattr(module, "EBS_DISPATCH_REGISTRY"):
            reg = getattr(module, "EBS_DISPATCH_REGISTRY")
            if isinstance(reg, dict):
                registry.update(reg)

    return registry


# Load registry once
EBS_REGISTRY = load_ebs_registry()


def ebs_dispatcher(action: str, **kwargs):
    """
    Unified EBS dispatcher.
    Input example:
        { "action": "attach_volume", "VolumeId": "...", "InstanceId": "...", ... }

    Automatically routes action → correct helper module.
    """
    if action not in EBS_REGISTRY:
        return {"error": f"Unknown EBS action '{action}'"}

    fn = EBS_REGISTRY[action]["fn"]
    schema = EBS_REGISTRY[action]["schema"]

    # Validate arguments
    try:
        validated = schema(**kwargs)
    except Exception as e:
        return {"validation_error": str(e)}

    # Execute real AWS call
    return fn(**validated.model_dump())


aws_ebs_tool = FunctionTool(
    name="aws_ebs",
    description="Unified EBS dispatcher (auto-discovers actions from helper_functions).",
    fn=ebs_dispatcher,
    parameters={
        "type": "object",
        "properties": {
            "action": {"type": "string"},
        },
        "required": ["action"],
        "additionalProperties": True,
    },
)
