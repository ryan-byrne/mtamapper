import csv, json

def update_json():
    stop_dict = {}
    with open("google_transit/stops.txt") as f:
        stops = csv.DictReader(f)
        for stop in stops:
            id = stop["stop_id"]
            if len(id) == 4 or id in stop_dict.keys() or id in ["9", "H", "S"]:
                continue
            lat = round(20*(float(stop["stop_lat"])-40.7), 5)
            lon = round(20*(float(stop["stop_lon"])+73.9), 5)
            stop_dict[id] = [lat, 0, lon]
    f.close()
    with open('mta.json', 'w') as f:
        points = []
        for id in stop_dict.keys():
            points.append({id:stop_dict[id]})
        json.dump(points, f, ensure_ascii=False)

update_json()
