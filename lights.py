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
with open("mta.json") as f:
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
        status[s]['coor'] = item[s]
    for item in status.keys():
        print item, status[item]
    print len(status.keys())
f.close()

def color_blend(color_array):
    #print color_array
    a = color_array[0]
    b = color_array[1]
    r = (int(a[0])+int(b[0]))/2
    g = (int(a[1])+int(b[1]))/2
    b = (int(a[2])+int(b[2]))/2
    return (r, g, b)

def hex_to_rgb(hex):
     #print hex
     hex = hex.lstrip('#')
     hlen = len(hex)
     return tuple(int(hex[i:i+hlen/3], 16) for i in range(0, hlen, hlen/3))

def pixel_color(coord, pixel_values):
    return pixel_values

class Lights():

    @staticmethod
    def control(on, off):
        coordinates = []
        color_values = []
        print "Turn on:"
        for s in on:
            if s[1] == "R60" or s[1] == "R65":
                continue
            current_color = status[s[1]]["color"]
            print current_color
            print "Send ", colors[s[0][0]], " to ", s[1]
        print "Turn off:"
        for s in off:
            if s[1] == "R60" or s[1] == "R65":
                continue
            current_color = status[s[1]]["color"]
            print current_color
            print "Remove ", colors[s[0][0]], " from ", s[1]


    @staticmethod
    def run(stops, old_stops, client):
        off = []
        on = []
        for stop in stops:
            if stop not in old_stops:
                on.append(stop)
        for stop in old_stops:
            if stop not in stops:
                off.append(stop)
        pixels = Lights.control(on, off)
        #client.put_pixels(pixels, channel=0)
