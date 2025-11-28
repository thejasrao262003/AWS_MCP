from fastmcp import FastMCP
from fastmcp.tools import FunctionTool
from mcp_server.models.ec2 import ListEC2Params
from mcp_server.tools.ec2_tools import list_ec2_instances

mcp = FastMCP("aws-mcp")

tool = FunctionTool(
    name="aws.list_ec2_instances",
    description="List EC2 instances in an AWS region",
    fn=list_ec2_instances,
    parameters=ListEC2Params.model_json_schema()
)

mcp.add_tool(tool)

def run():
    mcp.run()

if __name__ == "__main__":
    run()
