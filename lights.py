import sys, opc

# Creates an object to store train statuses
status = {}

def hex_to_rgb(hex):
     hex = hex.lstrip('#')
     hlen = len(hex)
     return tuple(int(hex[i:i+hlen/3], 16) for i in range(0, hlen, hlen/3))

def pixel_color(coord, pixel_values):
    return pixel_values

class Lights():

    @staticmethod
    def control(on, off, stop_dict):
        coordinates = []
        color_values = []
        # Parses the list of "on" trains
        for stop in on:
            if stop[0] not in status:
                status[stop[0]] = [stop[1]]
            else:
                if stop[1] not in status[stop[0]]:
                    status[stop[0]].append(stop[1])
                else:
                    continue
        # Does the same for "off" trains
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
                # Signal to be sent is off
                signal = (0, 0, 0)
            elif len(status[stop]) > 1:
                # Multiple colors found, blending
                signal = Lights.color_blend(status[stop])
            else:
                # Single color
                signal = hex_to_rgb(status[stop][0])
            try:
                lat = stop_dict[stop]["lat"]
                lon = stop_dict[stop]["lon"]
            except KeyError:
                continue
            coordinates.append((lat, 0, lon))
            color_values.append((signal))
        pixels = [color_values[i] for i in range(len(coordinates))]
        return pixels

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
        pixels = Lights.control(on, off, stop_dict)
        client.put_pixels(pixels, channel=0)
