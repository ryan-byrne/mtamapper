import json, math, csv

with open("mta.json", "r") as f:
    mta = json.loads(f.read())
f.close()

closest = {}
combine = {}

for s1 in mta:
    for i1 in s1:
        d_min = 10
        #print i1
        x1 = float(s1[i1]["coor"][0])
        y1 = float(s1[i1]["coor"][2])
        closest[i1] = {}
        for s2 in mta:
            for i2 in s2:
                if i1 == i2:
                    continue
                x2 = float(s2[i2]["coor"][0])
                y2 = float(s2[i2]["coor"][2])
                x_diff = x1-x2
                y_diff = y1-y2
                dist = math.sqrt(x_diff**2 + y_diff**2)
                if dist < 0.04:
                    if i1 in combine.keys():
                        if i2 in combine[i1]:
                            continue
                        else:
                            combine[i1].append(i2)
                    elif i2 in combine.keys():
                        if i1 in combine[i2]:
                            continue
                        else:
                            combine[i2].append(i1)
                    else:
                        combine[i1] = [i2]

with open("google_transit/stops.txt") as f:
    stops = csv.DictReader(f)
    for stop in stops:
        id = stop["stop_id"][:3]
        name = stop["stop_name"]
        for item in combine.keys():
            if id == item:
                print name, id
f.close()
#print closest["R29"]["A41"]
