import sys, opc

# Creates an object to store train statuses
status = {}

def hex_to_rgb(hex):
     hex = hex.lstrip('#')
     hlen = len(hex)
     return tuple(int(hex[i:i+hlen/3], 16) for i in range(0, hlen, hlen/3))

class Lights():

    @staticmethod
    def control(on, off, stop_dict, client):
        # Parses the list of "on" trains
        for stop in on:
            if stop[0] not in status:
                status[stop[0]] = [stop[1]]
            else:
                if stop[1] not in status[stop[0]]:
                    status[stop[0]].append(stop[1])
                else:
                    continue
        for stop in off:
            if stop[0] not in status:
                status[stop[0]] = []
            else:
                try:
                    status[stop[0]].remove(stop[1])
                except ValueError:
                    #print status[stop[0]]
                    continue
        # Here's where the magic baby. Later add LED control via
        # the raspberry Pi.
        for stop in status.keys():
            if status[stop] == []:
                signal = (0, 0, 0)
            elif len(status[stop]) > 1:
                signal = Lights.color_blend(status[stop])
            else:
                signal = hex_to_rgb(status[stop][0])
            print stop, signal
        Lights.test_lights(stop_dict, client)

    @staticmethod
    def test_lights(stop_dict, client):
        #print stop_dict
        for id in status.keys():
            if status[id] == []:
                # Eventually this will shut off the LED
                continue
            else:
                # Otherwise turn on the LED
                try:
                    lat = stop_dict[id]["lat"]
                    lon = stop_dict[id]["lon"]
                    #print status[id], " at ", [lat, lon, 0]
                    client.put_pixels([(0,1,0)], channel=0)
                except KeyError:
                    continue

    @staticmethod
    def color_blend(color_array):
        #print color_array
        a = hex_to_rgb(color_array[0])
        b = hex_to_rgb(color_array[1])
        r = (int(a[0])+int(b[0]))/2
        g = (int(a[1])+int(b[1]))/2
        b = (int(a[2])+int(b[2]))/2
        return r, g, b


    @staticmethod
    def run(stops, old_stops, stop_dict, client):
        off = []
        on = []
        for stop in stops:
            if stop not in old_stops:
                on.append(stop)
        for stop in old_stops:
            if stop not in stops:
                off.append(stop)
        Lights.control(on, off, stop_dict, client)
