import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")

CATEGORY_MAP = {
    "temple": "religion.place_of_worship.hinduism",
    "beach": "beach",
   "museum": "entertainment.museum",
    "park": "leisure.park"
}

def geocode_city(city):
    url = "https://api.geoapify.com/v1/geocode/search"

    params = {
        "text": city,
        "apiKey": API_KEY,
        "limit": 1
    }

    response = requests.get(url, params=params)

    print("Status:", response.status_code)

    data = response.json()

    if not data["features"]:
        return None

    location = data["features"][0]

    return {
        "latitude": location["properties"]["lat"],
        "longitude": location["properties"]["lon"]
    }

def search_allplaces(city, category):
    location = geocode_city(city)

    if location is None:
        return []

    geoapify_category = CATEGORY_MAP.get(category.lower())

    if geoapify_category is None:
        return []

    url = "https://api.geoapify.com/v2/places"

    params = {
        "categories": geoapify_category,
        "bias": f"proximity:{location['longitude']},{location['latitude']}",
        "limit": 10,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    print("Status:", response.status_code)

    data = response.json()

    results = []

    for feature in data.get("features", []):
        properties = feature["properties"]
        #print(properties.keys())
        
        name = properties.get("name")
        if not name:
            continue

        results.append({
            "place_id": properties.get("place_id"),
            "name": properties.get("name"),
            "city": properties.get("city"),
            "address": properties.get("formatted"),
            "latitude": properties.get("lat"),
            "longitude": properties.get("lon"),
            "categories": properties.get("categories", [])
        })

    return results


def calculate_route(origin, destination):
    url = "https://api.geoapify.com/v1/routing"

    params = {
        "waypoints": (
            f"{origin['latitude']},{origin['longitude']}|"
            f"{destination['latitude']},{destination['longitude']}"
        ),
        "mode": "drive",
        "format": "json",
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    routes = data.get("results", [])

    if not routes:
        return {"error": "No route found"}

    route = routes[0]

    return {
        "distance_meters": route["distance"],
        "distance_km": round(route["distance"] / 1000, 2),
        "time_seconds": round(route["time"]),
        "time_minutes": round(route["time"] / 60, 2),
        "mode": route["mode"]
    }



def get_real_place_details(place_id):
    """Fetch detailed information about a real place using Geoapify."""

    url = "https://api.geoapify.com/v2/place-details"

    params = {
        "id": place_id,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    # Find the main details feature in the GeoJSON response.
    for feature in data.get("features", []):
        properties = feature.get("properties", {})

        if properties.get("feature_type") == "details":
            return {
                "place_id": properties.get("place_id", place_id),
                "name": properties.get("name"),
                "address": properties.get("formatted"),
                "city": properties.get("city"),
                "country": properties.get("country"),
                "categories": properties.get("categories", []),
                "website": properties.get("website"),
                "opening_hours": properties.get("opening_hours"),
                "phone": properties.get("contact", {}).get("phone")
                    or properties.get("phone"),
                "latitude": properties.get("lat"),
                "longitude": properties.get("lon")
            }

    return {"error": "No details found for this place"}




# print("Starting Geoapify test...")

# # print(search_places("Chennai", "museum"))
# # print(search_places("Chennai", "beach"))
# print(search_places("Chennai", "temple"))

if __name__ == "__main__":
    places = search_allplaces("Chennai", "temple")

    if places:
        place_id = places[0]["place_id"]
        details = get_real_place_details(place_id)
        print(details)
    else:
        print("No places found")
