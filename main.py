import time, sys, csv, json, os, requests, opc, threading
from google.transit import gtfs_realtime_pb2
from google.protobuf.message import DecodeError
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import ConnectionError

class MTA():

    def __init__(self):
        self.exclude = ["9", "S", "FS", "", "GS", "H"]
        self.trains = {}
        self.url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"
        self.key = os.getenv("GMAPS")
        with open("resources/combine.json", "r") as f:
            self.combine = json.load(f)
        f.close()

    def update(self):

        self.trains = {}

        threads = []

        for id in ['-ace','-bdfm','-g','-jz','-nqrw','-l','-7','']:
            threads.append(threading.Thread(target=self._update_trains, args=(id,)))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        return self.trains

    def _update_trains(self, id):
        try:
            #print("Updating train info for ID: {0}...".format(id))
            feed = gtfs_realtime_pb2.FeedMessage()
            #print "Retriving info from MTA datamine..."
            response = requests.get(self.url+id, headers={"x-api-key":self.key})
            feed.ParseFromString(response.content)
            # Parse Entire Feed
            for e in feed.entity:
                # Record Route of Trip
                route = e.vehicle.trip.route_id
                # Exclude particular routes and record the Stop
                if route in self.exclude:
                    continue
                elif route == "L":
                    i = int(e.vehicle.current_stop_sequence)
                    if i < 10:
                        stop = "L0{0}".format(i)
                    else:
                        stop = "L{0}".format(i)
                else:
                    stop = e.vehicle.stop_id[:3]
                if stop in self.combine.keys():
                    stop = self.combine[stop]
                if stop not in self.trains.keys():
                    # Check if stop is already in dict
                    self.trains[stop] = [route]
                elif route in self.trains[stop]:
                    # Check if route is already in dict's list
                    continue
                else:
                    self.trains[stop].append(route)

        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()
        except ConnectionError:
            print("Error connecting to the {0} Datamine...".format(id))
        except DecodeError:
            print("Error decoding from {0} Datamine...".format(id))

class Lights():

    def __init__(self):
        self.colors = {
            "4":"#00933C",
            "5":"#00933C",
            "6":"#00933C",
            "6X":"#00933C",
            "5X":"#00933C",
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
            "FX":"#FF6319",
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
        self.client = opc.Client('localhost:7890')
        with open("resources/light_order.json", "r") as f:
            self.light_order = json.load(f)
        f.close()

    def update_pixels(self, trains):
        pixels = []
        for stop in self.light_order:
            if stop == "":
                continue
            elif stop not in trains.keys():
                # No train at station
                pixels.append((0,0,0))
            else:
                pixels.append(self.color_blend(trains[stop]))
        return pixels

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

def startup():
    print("Starting FadeCandy Server...")
    #os.system("sudo fcserver /usr/local/bin/fcserver.json")
    print("Connecting to the LED FadeCandy client...")
    client = opc.Client('localhost:7890')
    print("Running Startup...")

    for i in range(443):
        pixels = [ (0,0,0) ] * 443
        pixels[i] = (255, 255, 255)
        client.put_pixels(pixels)
        time.sleep(0.01)
    return client

# Takes stop IDs from a file and creates a Parsable Python Dictionary
if __name__ == '__main__':

    mta = MTA()
    lights = Lights()

    startup()

    print("\n*** Updating Trains. Press CTRL+C to Exit *** \n")
    while True:
        # Create empty dictionary to be populated
        trains = mta.update()
        pixels = lights.update_pixels(trains)
        lights.client.put_pixels(pixels)
