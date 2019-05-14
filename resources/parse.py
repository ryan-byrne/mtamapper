import json, math, csv
import pandas as pd

light_order = []

with open("mta_stops.csv", "r") as f:
    stops = pd.read_csv(f)
    channel = 0
    for c in range(7):
        print "x"*100
        for i in range(64):
            try:
                s = stops["Channel "+str(c)][i][:3]
            except (KeyError, TypeError):
                s = ""
            light_order.append(s)
f.close()

with open("light_order.json", "w") as f:
    json.dump(light_order, f)

f.close()
