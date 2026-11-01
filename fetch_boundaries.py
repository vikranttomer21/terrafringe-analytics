import requests
import json
import time

corridors = {
    "Wayanad-Bandipur Link": ["Wayanad Wildlife Sanctuary", "Bandipur National Park"],
    "Kanha-Pench Corridor": ["Kanha National Park", "Pench National Park"],
    "Rajaji-Corbett Link": ["Rajaji National Park", "Jim Corbett National Park"]
}

features = []
headers = {'User-Agent': 'TerraFringe_Pipeline/1.0'}

for zone, parks in corridors.items():
    for park in parks:
        url = f"https://nominatim.openstreetmap.org/search.php?q={park.replace(' ', '+')}&polygon_geojson=1&format=json"
        response = requests.get(url, headers=headers).json()
        for result in response:
            geom = result.get('geojson', {})
            if geom.get('type') in ['Polygon', 'MultiPolygon']:
                features.append({"type": "Feature", "properties": {"zone_name": zone}, "geometry": geom})
                break 
        time.sleep(1.5) 

with open("raw_corridors.geojson", "w") as f:
    json.dump({"type": "FeatureCollection", "features": features}, f)
print("Extraction complete.")