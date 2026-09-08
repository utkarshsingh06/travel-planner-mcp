from mcp.server.fastmcp import FastMCP

from database import (add_place_to_trip, create_trip, get_place_details,
                      get_trip, initialize_database, remove_place_from_trip,
                      search_places, seed_places)

mcp = FastMCP("Travel Planner")

@mcp.tool()
def hello():
    """Test the Travel Planner MCP server."""
    return "Travel Planner MCP is working!"

@mcp.tool()
def search_places_tool(city: str, category: str = ""):
    """Search tourist places in a city, optionally filtered by category."""

    places = search_places(city, category)

    return places

@mcp.tool()
def get_place_details_tool(place_id: int):
    """Get detailed information about a specific tourist place."""

    place = get_place_details(place_id)

    if place is None:
        return {
            "error": "Place not found"
        }

    return place

@mcp.tool()
def create_trip_tool(
    name: str,
    destination: str,
    start_date: str,
    end_date: str,
    budget: int
):
    """Create a new travel trip."""

    return create_trip(
        name,
        destination,
        start_date,
        end_date,
        budget
    )

@mcp.tool()
def get_trip_tool(trip_id: int):
    """Get a trip and all places added to it."""

    trip = get_trip(trip_id)

    if trip is None:
        return {
            "error": "Trip not found"
        }

    return trip

@mcp.tool()
def add_place_to_trip_tool(trip_id: int, place_id: int):
    """Add a place to a trip."""

    return add_place_to_trip(trip_id, place_id)

@mcp.tool()
def remove_place_from_trip_tool(trip_id: int, place_id: int):
    """Remove a place from a trip."""

    return remove_place_from_trip(trip_id, place_id)

if __name__ == "__main__":
    initialize_database()
    seed_places()
    print(search_places("Chennai", "Temple"))

    print("Travel Planner MCP server starting...")
    mcp.run()
    