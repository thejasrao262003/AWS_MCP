import pkgutil
import importlib
import mcp_server.tools


class ToolRegistry:
    @staticmethod
    def load_all_tools():
        all_tools = []

        package_path = mcp_server.tools.__path__
        package_prefix = mcp_server.tools.__name__ + "."

        for module in pkgutil.walk_packages(package_path, package_prefix):
            module_name = module.name

            # Skip __init__.py
            if module_name.endswith("__init__"):
                continue

            print(f"[Registry] Found module: {module_name}")

            try:
                mod = importlib.import_module(module_name)
                print(f"[Registry] Imported: {module_name}")
            except Exception as e:
                print(f"[Registry] ERROR importing {module_name} => {e}")
                continue

            tools_list = getattr(mod, "tools", None)
            print(f"[Registry] Module tools: {tools_list}")

            if tools_list:
                all_tools.extend(tools_list)

        print(f"[Registry] FINAL TOOLS: {all_tools}")
        return all_tools
