import csv, json

exclude = ["S", "9"]
status = {}

with open("mta.json", "r") as f:
    mta = json.loads(f.read())
    for item in mta:
        s = item.keys()[0]
        r = s[0]
        if r in exclude:
            continue
        #print s
        #print item[s]
        status[s] = {}
        status[s]['color'] = (0, 0, 0)
        status[s]['coor'] = item[s]["coor"]
        new_coor = []
        for item in status[s]['coor']:
            new_coor.append(item)
        status[s]["coor"] = new_coor
        status[s]['on'] = []
    status["R60"] = {'color': (0, 0, 0), "coor":[0,0], "on":[]}

coor_array = []

with open("resources/openpixelcontrol/layouts/mta.json", "w+") as f:
    for stop in status:
        coor = status[stop]["coor"]
        coor_array.append({"point":coor})
    json.dump(coor_array, f)
f.close()
