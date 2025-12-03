import importlib
import sys


class ResourceRegistry:
    @staticmethod
    def load_all_resources():
        all_resources = []

        # Only load from service-level directories
        service_modules = [
            "mcp_server.resources.ec2",
            "mcp_server.resources.ebs",
            "mcp_server.resources.vpc",
            # Add more top-level service resource modules later:
            # "mcp_server.resources.s3",
            # "mcp_server.resources.cloudwatch",
        ]

        for module_name in service_modules:
            print(f"[ResourceRegistry] Loading service resource module: {module_name}", file=sys.stderr)

            try:
                mod = importlib.import_module(module_name)
            except Exception as e:
                print(f"[ResourceRegistry] ERROR importing {module_name} => {e}", file=sys.stderr)
                continue

            # Try to find the resource list with service-specific naming
            resource_list = None
            
            # Try EC2_RESOURCE_LIST, EBS_RESOURCE_LIST, VPC_RESOURCE_LIST, etc.
            for attr_name in dir(mod):
                if attr_name.endswith("_RESOURCE_LIST"):
                    resource_list = getattr(mod, attr_name)
                    break

            if resource_list:
                print(f"[ResourceRegistry] Found {len(resource_list)} resources in {module_name}", file=sys.stderr)
                all_resources.extend(resource_list)
            else:
                print(f"[ResourceRegistry] No *_RESOURCE_LIST found in {module_name}", file=sys.stderr)

        print(f"[ResourceRegistry] Total resources loaded: {len(all_resources)}", file=sys.stderr)
        return all_resources
