locations_list = [
    {
        "name": "Paris",
        "coordinates": {
            "latitude": 48.854596,
            "longitude": 2.347727
        }
    },
    {
        "name": "London",
        "coordinates": {
            "latitude": 51.500932,
            "longitude": -0.123857
        }
    },
    {
        "name": "Berlin",
        "coordinates": {
            "latitude": 52.518242,
            "longitude": 13.400813
        }
    },
    {
        "name": "Washington",
        "coordinates": {
            "latitude": 38.897320,
            "longitude": -77.036441
        }
    }
]


def get_coordinates(location_name):
    for location in locations_list:
        if location["name"] == location_name:
            return location["coordinates"]
    return {"latitude": 0.0, "longitude": 0.0}
