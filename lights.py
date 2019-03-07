import sys, opc, json

status = {}

# Creates an object to store train statuses
with open("mta.json") as f:
    mta = json.loads(f.read())
    for item in mta:
        s = item.keys()[0]
        #print s
        #print item[s]
        status[s] = {}
        status[s]['color'] = [(0, 0, 0)]
        status[s]['coor'] = item[s]
f.close()

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
        # Parses the list of "on" trains
        for stop in on:
            if stop == "R65":
                continue
            route = stop[0]
            new_color = hex_to_rgb(colors[route])
            #print stop, "On", new_color
            if status[stop]['color'] == [(0, 0, 0)]:
                status[stop]['color'] = [new_color]
            elif new_color in status[stop]['color']:
                continue
            else:
                status[stop]['color'].append(new_color)
        # Does the same for "off" trains
        for stop in off:
            if stop == "R65":
                continue
            route = stop[0]
            new_color = hex_to_rgb(colors[route])
            #print stop, "Off", new_color
            if len(status[stop]['color']) > 1:
                status[stop]['color'].remove(new_color)
            else:
                color_array = [(0, 0, 0)]
                current_color = color_array[0]
        pixels = []
        for stop in status.keys():
            pixels.append(status[stop]['color'][0])

        #print pixels
        return pixels

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
        client.put_pixels(pixels, channel=0)
