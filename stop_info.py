import csv, json, math, collections

with open("resources/light_order.json", "r") as f:
    order = json.load(f)
f.close()

coor = {}

# {"point": [1.32, 0.00, 1.32]}

s = {}

with open("resources/mta.json", "r") as f:
    stops = json.load(f)
    for stop in stops:
        s[stop.keys()[0]] = stop[stop.keys()[0]]
f.close()

order_coor = []

# {"point": [1.32, 0.00, 1.32]}

for stop in order:
    try:
        order_coor.append({"point":s[stop]["coor"]})
    except KeyError:
        continue

with open("mta.json", "w+") as f:
    json.dump(order_coor, f)
f.close()
