import csv, json, math

exclude = ["S", "9"]
status = {}
combine = {}
combine_list = []

with open("mta.json", "r") as f:
    mta = json.loads(f.read())
    for s1 in mta:
        for i1 in s1:
            d_min = 10
            #print i1
            x1 = float(s1[i1]["coor"][0])
            y1 = float(s1[i1]["coor"][2])
            for s2 in mta:
                for i2 in s2:
                    if i1 == i2:
                        continue
                    x2 = float(s2[i2]["coor"][0])
                    y2 = float(s2[i2]["coor"][2])
                    x_diff = x1-x2
                    y_diff = y1-y2
                    dist = math.sqrt(x_diff**2 + y_diff**2)
                    if dist < 0.03:
                        if i1 in combine.keys():
                            if i2 in combine[i1]:
                                continue
                            else:
                                combine_list.append(i2)
                                combine[i1].append(i2)
                        elif i2 in combine.keys():
                            if i1 in combine[i2]:
                                continue
                            else:
                                combine_list.append(i1)
                                combine[i2].append(i1)
                        else:
                            combine_list.append(i2)
                            combine[i1] = [i2]
    for item in mta:
        s = item.keys()[0]
        r = s[0]
        if r in exclude:
            continue
        # If stop has combined coordinates
        if s in combine_list:
            # Search for it in each of the Dictionary entries
            for key in combine.keys():
                # If found in a dictionary
                if s in combine[key]:
                    # Use the coordinates of the dictionary entry
                    coor = status[key]["coor"]
        else:
            coor = item[s]["coor"]
        status[s] = {}
        status[s]['color'] = (0, 0, 0)
        status[s]['coor'] = coor
        status[s]['on'] = []
    status["R60"] = {'color': (0, 0, 0), "coor":[0,0], "on":[]}

for item in status:
    print item

coor_array = []
with open("resources/openpixelcontrol/layouts/mta.json", "w+") as f:
    for stop in status:
        coor = status[stop]["coor"]
        coor_array.append({"point":coor})
    json.dump(coor_array, f)
f.close()
