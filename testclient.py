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

            for tool in tools.tools:
                print("-", tool.name)

            # Call our search tool
            result = await session.call_tool(
                "search_places_tool",
                {
                    "city": "Chennai",
                    "category": "Temple"
                }
            )

            print("\nSearch result:")
            print(result)
            
            
            trip = await session.call_tool(
                "create_trip_tool",
                {
                    "name": "Chennai Weekend",
                    "destination": "Chennai",
                    "start_date": "2026-10-10",
                    "end_date": "2026-10-12",
                    "budget": 10000
                }
            )

            print("\nCreated trip:")
            print(trip)
            print("\nTrip result type:")
            print(type(trip))

            print("\nStructured content:")
            print(trip.structuredContent)  
            
            
            add_place = await session.call_tool(
                "add_place_to_trip_tool",
                {
                    "trip_id": 1,
                    "place_id": 2
               }
            )
            print("\nAdded place to trip:")
            print(add_place)
            
            trip_details = await session.call_tool(
                "get_trip_tool",
                {
                    "trip_id": 1
               }
        )
        print("\nTrip details:")
        print(trip_details)
        
        remove_place = await session.call_tool(
            "remove_place_from_trip_tool",
            {
                "trip_id": 1,
                "place_id": 2
           }
        )
        print("\nRemoved place from trip:")
        print(remove_place)


if __name__ == "__main__":
    asyncio.run(main())