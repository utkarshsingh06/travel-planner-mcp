import sqlite3

DB_NAME = "travel.db"


def initialize_database():
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS places (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            estimated_cost INTEGER
        )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        destination TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        budget INTEGER
    )
""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trip_places (
        trip_id INTEGER NOT NULL,
        place_id INTEGER NOT NULL,
        PRIMARY KEY (trip_id, place_id)
    )
""")

    connection.commit()
    connection.close()
    
    
    
def seed_places():
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    places = [
        (
            "Kapaleeshwarar Temple",
            "Chennai",
            "Temple",
            "Famous Hindu temple in Mylapore",
            0
        ),
        (
            "Marina Beach",
            "Chennai",
            "Beach",
            "One of the most famous beaches in Chennai",
            0
        ),
        (
            "Fort St. George",
            "Chennai",
            "Historical",
            "Historic fort and museum",
            200
        ),
        (
            "Government Museum",
            "Chennai",
            "Museum",
            "Museum complex in Egmore",
            50
        ),
        (
            "Arignar Anna Zoological Park",
            "Chennai",
            "Wildlife",
            "Large zoological park near Vandalur",
            200
        )
    ]

    cursor.executemany("""
       INSERT OR IGNORE INTO places
        (name, city, category, description, estimated_cost)
        VALUES (?, ?, ?, ?, ?)
    """, places)

    connection.commit()
    connection.close()
    
def search_places(city, category=""):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    if category:
        cursor.execute("""
            SELECT id, name, city, category, description, estimated_cost
            FROM places
            WHERE city = ? AND category = ?
        """, (city, category))
    else:
        cursor.execute("""
            SELECT id, name, city, category, description, estimated_cost
            FROM places
            WHERE city = ?
        """, (city,))
    rows = cursor.fetchall()
    connection.close()
    results = []
    for row in rows:
     results.append({
         "id": row[0],
         "name": row[1],
         "city": row[2],
         "category": row[3],
         "description": row[4],
         "estimated_cost": row[5]
     })
     return results


def get_place_details(place_id):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, city, category, description, estimated_cost
        FROM places
        WHERE id = ?
    """, (place_id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "city": row[2],
        "category": row[3],
        "description": row[4],
        "estimated_cost": row[5]
    }
    
def create_trip(name, destination, start_date, end_date, budget):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO trips
        (name, destination, start_date, end_date, budget)
        VALUES (?, ?, ?, ?, ?)
    """, (name, destination, start_date, end_date, budget))

    connection.commit()

    trip_id = cursor.lastrowid

    connection.close()

    return {
        "id": trip_id,
        "name": name,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget
    }
    
def add_place_to_trip(trip_id, place_id):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO trip_places (trip_id, place_id)
        VALUES (?, ?)
    """, (trip_id, place_id))

    connection.commit()
    connection.close()

    return {
        "trip_id": trip_id,
        "place_id": place_id,
        "message": "Place added to trip successfully"
    }
    
def get_trip(trip_id):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, destination, start_date, end_date, budget
        FROM trips
        WHERE id = ?
    """, (trip_id,))

    trip = cursor.fetchone()

    if trip is None:
        connection.close()
        return None

    cursor.execute("""
        SELECT p.id, p.name, p.city, p.category
        FROM places p
        JOIN trip_places tp
        ON p.id = tp.place_id
        WHERE tp.trip_id = ?
    """, (trip_id,))

    places = cursor.fetchall()

    connection.close()

    result = {
        "id": trip[0],
        "name": trip[1],
        "destination": trip[2],
        "start_date": trip[3],
        "end_date": trip[4],
        "budget": trip[5],
        "places": []
    }

    for place in places:
        result["places"].append({
            "id": place[0],
            "name": place[1],
            "city": place[2],
            "category": place[3]
        })

    return result

def remove_place_from_trip(trip_id, place_id):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM trip_places
        WHERE trip_id = ? AND place_id = ?
    """, (trip_id, place_id))

    connection.commit()

    connection.close()

    return {
        "trip_id": trip_id,
        "place_id": place_id,
        "message": "Place removed from trip successfully"
    }