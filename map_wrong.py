import requests

def map_right_data(url):
    map_code = url.split('/')[-2]
    json_url = f"https://green.api.mapright.com/ranching/maps/{map_code}/share.json"


    response = requests.get(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code != 200:
        print("Unsuccessful MapRight Request")
        return None
    data = response.json()
    geojson = {
        "type": "FeatureCollection",
        "features": data['geoJSON']
    }
    return geojson
