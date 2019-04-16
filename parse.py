import json

with open("mta.json", "r") as f:
    mta = json.loads(f.read())
f.close()

max_x = 0
max_y = 0
max_z = 0
min_x = 0
min_y = 0
min_z = 0

for stop in mta:
    for item in stop:
        x = stop[item]["coor"][0]
        y = stop[item]["coor"][0]
        z = stop[item]["coor"][0]
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        if z > max_z:
            max_z = z
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if z < min_z:
            min_z = z

print max_x, max_y, max_z
print min_x, min_y, min_z
