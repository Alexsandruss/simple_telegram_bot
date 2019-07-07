from jsondb import JsonDB


locations_list = JsonDB("data/locations.json")["locations"]


def get_coordinates(location_name):
    for location in locations_list:
        if location["name"] == location_name:
            return location["coordinates"]
    return {"latitude": 0.0, "longitude": 0.0}
