import json

layout = []

with open("combine.json", "r") as f:
    combine = json.load(f)
f.close()

with open("mta.json", "r") as f:
    mta = json.load(f)
f.close()

with open("light_order.json", "r") as f:
    order = json.load(f)
f.close()

print(combine.keys())

for stop in order:
    for s in mta:
        if stop in s.keys() and stop not in combine.keys():
            layout.append({"point":s[stop]["coor"]})

with open("layout.json",'w') as f:
    json.dump(layout, f)
f.close()
