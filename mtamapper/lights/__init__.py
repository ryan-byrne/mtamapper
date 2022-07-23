import time
from ..utils import COLORS, LIGHT_ORDER

class Lights():

    def __init__(self):
        self.colors = COLORS
        self.light_order = LIGHT_ORDER

    def startup(self, client):

        print("Running Startup...")

        for i in range(443):
            pixels = [ (0,0,0) ] * 443
            pixels[i] = (255, 255, 255)
            client.put_pixels(pixels)
            time.sleep(0.01)

    def update_pixels(self, trains):
        pixels = []
        for stop in self.light_order:
            try:
                color = self.color_blend(trains[stop])
            except KeyError:
                color = (0,0,0)
                # No train at station
            pixels.append(color)
        return pixels
    
    def clear_pixels(self):
        return [(0,0,0) for l in self.light_order]

    def color_blend(self, train_array):
        color_array = [self.hex_to_rgb(self.colors[t]) for t in train_array]
        r = 0
        g = 0
        b = 0
        for c in color_array:
            r += int(c[0])
            g += int(c[1])
            b += int(c[2])

        fr = min(r, 255)
        fg = min(g, 255)
        fb = min(b, 255)
        return (fr, fg, fb)

    def hex_to_rgb(self, hex):
         hex = hex.lstrip('#')
         hlen = len(hex)
         return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))
