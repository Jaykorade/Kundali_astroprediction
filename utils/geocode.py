import requests

def get_lat_lon(place):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place,
        "format": "json"
    }

    response = requests.get(url, params=params).json()

    if response:
        return float(response[0]["lat"]), float(response[0]["lon"])

    return None, None