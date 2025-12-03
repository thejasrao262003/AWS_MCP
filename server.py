from fastmcp import FastMCP
from mcp_server.core.registry import ToolRegistry
from mcp_server.core.resource_registry import ResourceRegistry

mcp = FastMCP("aws-mcp")

# Auto-load all tools
for tool in ToolRegistry.load_all_tools():
    mcp.add_tool(tool)

for resource in ResourceRegistry.load_all_resources():
    mcp.add_resource(resource)

def run():
    mcp.run()

if __name__ == "__main__":
    run()
