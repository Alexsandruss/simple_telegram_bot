import jsondb


locations_list = jsondb.load_db("locations.json")["locations"]


def get_coordinates(location_name):
    for location in locations_list:
        if location["name"] == location_name:
            return location["coordinates"]
    return {"latitude": 0.0, "longitude": 0.0}
