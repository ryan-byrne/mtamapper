import csv, json

exclude = ["S", "9"]

def update_json():
    stop_dict = {}
    with open("google_transit/stops.txt") as f:
        stops = csv.DictReader(f)
        for stop in stops:
            id = stop["stop_id"][:3]
            if id[0] in exclude or id in stop_dict.keys():
                continue
            else:
                stop_dict[id] = {}
            lat = round(20*(float(stop["stop_lat"])-40.7), 5)
            lon = round(20*(float(stop["stop_lon"])+73.9), 5)
            stop_dict[id]["coor"] = [lat, 0, lon]
    f.close()
    with open('mta.json', 'w') as f:
        points = []
        for id in stop_dict.keys():
            points.append({id:stop_dict[id]})
        json.dump(points, f, ensure_ascii=False)

update_json()
