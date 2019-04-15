import sys, opc, json

status = {}
colors = {
    "4":"#00933C",
    "5":"#00933C",
    "6":"#00933C",
    "6X":"#00933C",
    "1":"#EE352E",
    "2":"#EE352E",
    "3":"#EE352E",
    "7":"#B933AD",
    "7X":"#B933AD",
    "A":"#0039A6",
    "C":"#0039A6",
    "E":"#0039A6",
    "B":"#FF6319",
    "D":"#FF6319",
    "F":"#FF6319",
    "M":"#FF6319",
    "N":"#FCCC0A",
    "Q":"#FCCC0A",
    "R":"#FCCC0A",
    "W":"#FCCC0A",
    "G":"#6CBE45",
    "L":"#A7A9AC",
    "J":"#996633",
    "Z":"#996633",
    "9":"#808183",
    "S":"#0039A6",
    "H":"#0039A6"
}
exclude = ["S", "9"]
# Creates an object to store train statuses
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
        status[s]['on'] = []
    status["R60"] = {'color': (0, 0, 0), "coor":[0,0], "on":[]}
f.close()

def color_blend(color_array):
    #print color_array
    r = 0
    g = 0
    b = 0
    for c in color_array:
        r += int(hex_to_rgb(c)[0])
        g += int(hex_to_rgb(c)[1])
        b += int(hex_to_rgb(c)[2])
    l = len(color_array)
    return (r/l, g/l, b/l)

def hex_to_rgb(hex):
     #print hex
     hex = hex.lstrip('#')
     hlen = len(hex)
     return tuple(int(hex[i:i+hlen/3], 16) for i in range(0, hlen, hlen/3))

class Lights():

    @staticmethod
    def control():
        for stop in status.keys():
            #print stop, status[stop]['on']
            train_array = status[stop]['on']
            color_array = []
            for t in train_array:
                c = colors[t]
                if c not in color_array:
                    color_array.append(c)
                else:
                    continue
            if len(color_array) == 0:
                status[stop]['color'] = (0, 0, 0)
            elif len(color_array) == 1:
                status[stop]['color'] = hex_to_rgb(color_array[0])
            else:
                color = color_blend(color_array)
                status[stop]['color'] = color
        pixel_array = []
        for stop in status:
            pixel_array.append(status[stop]["color"])
        return pixel_array



    @staticmethod
    def run(stops, old_stops, client):
        for s in stops:
            if s not in old_stops:
                #print "Turn on ", s[0], " at ", s[1]
                try:
                    if s[0] not in status[s[1]]["on"]:
                        status[s[1]]["on"].append(s[0])
                    else:
                        continue
                except KeyError:
                    continue
        for s in old_stops:
            if s not in stops:
                #print "Turn off ", s[0], " at ", s[1]
                try:
                    if s[0] not in status[s[1]]["on"]:
                        continue
                    else:
                        status[s[1]]["on"].remove(s[0])
                except KeyError:
                    continue
        pixels = Lights.control()
        client.put_pixels(pixels, channel=0)
