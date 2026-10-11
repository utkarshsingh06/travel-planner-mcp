import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
)


async def main():

    async with stdio_client(server_params) as (read_stream, write_stream):

        async with ClientSession(read_stream, write_stream) as session:

            # Initialize MCP connection
            await session.initialize()

            # Get available tools
            tools = await session.list_tools()

            print("Available tools:")
            
           
# 1. Search for real temples
            search_result = await session.call_tool(
            "search_real_places_tool",
            {
                "city": "Chennai",
                "category": "temple"
            }
        )
            print("\n1. Search Results:")
            print(search_result)




if __name__ == "__main__":
    asyncio.run(main())