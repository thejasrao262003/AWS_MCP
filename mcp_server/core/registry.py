import importlib
import sys
import mcp_server.tools


class ToolRegistry:
    @staticmethod
    def load_all_tools():
        all_tools = []
        service_modules = [
            "mcp_server.tools.ec2",
            "mcp_server.tools.ebs",
            "mcp_server.tools.vpc"
        ]

        for module_name in service_modules:
            print(f"[Registry] Loading service module: {module_name}", file=sys.stderr)

            try:
                mod = importlib.import_module(module_name)
            except Exception as e:
                print(f"[Registry] ERROR importing {module_name} => {e}", file=sys.stderr)
                continue

            tools_list = getattr(mod, "tools", None)
            
            if tools_list:
                print(f"[Registry] Found {len(tools_list)} tools from {module_name}", file=sys.stderr)
                all_tools.extend(tools_list)
            else:
                print(f"[Registry] No tools found in {module_name}", file=sys.stderr)

        print(f"[Registry] Total tools loaded: {len(all_tools)}", file=sys.stderr)
        return all_tools
