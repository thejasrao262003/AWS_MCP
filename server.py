from fastmcp import FastMCP
from mcp_server.core.registry import ToolRegistry

mcp = FastMCP("aws-mcp")

# Auto-load all tools
for tool in ToolRegistry.load_all_tools():
    mcp.add_tool(tool)

def run():
    mcp.run()

if __name__ == "__main__":
    run()
