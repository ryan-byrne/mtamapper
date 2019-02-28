import csv

with open("google_transit/stops.txt") as f:
    stops = csv.DictReader(f)
    sorted_stops = []
    for stop in stops:
        l = stop["stop_id"][-1]
        ll = stop["stop_id"][0]
        if l == "N" or l == "S" or ll == "S" or ll == "H":
            continue
        else:
            sorted_stops.append(stop["stop_id"])
            
f.close()

print len(sorted_stops)
