import time, sys, csv, json, subprocess, os, requests, opc, asyncio, collections
from google.transit import gtfs_realtime_pb2
from google.protobuf.message import DecodeError
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import ConnectionError

exclude = ["S", "9"]

class MTA():

    def __init__(self):
        self.ids = ["1", "26", "16", "21", "2", "31", "36", "51"]
        self.exclude = ["9", "S", "FS", "", "GS", "H"]
        self.url = 'http://datamine.mta.info/mta_esi.php?key=aec131a835263208ee94b402590bb930&feed_id='
        self.dict = {}
        with open("resources/combine.json", "r") as f:
            self.combine = json.load(f)
        f.close()

    def fetch(self, session, id):
        #print("Updating train info for ID: {0}...".format(id))
        feed = gtfs_realtime_pb2.FeedMessage()
        #print "Retriving info from MTA datamine..."
        try:
            with session.get(self.url + id, timeout=5) as response:
                r = response.content
                feed.ParseFromString(r)
                # Parse Entire Feed
                for e in feed.entity:
                    # Record Route of Trip
                    route = e.vehicle.trip.route_id
                    # Exclude particular routes and Trains that are not stopped
                    if route in self.exclude:
                        continue
                    # Record Stop (without direction)
                    stop = e.vehicle.stop_id[:3]
                    if stop not in self.dict.keys():
                        # Check if stop is already in dict
                        self.dict[stop] = [route]
                    elif route in self.dict[stop]:
                        # Check if route is already in dict's list
                        continue
                    else:
                        self.dict[stop].append(route)



        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()
        except ConnectionError:
            print("Error connecting to the {0} Datamine...".format(id))
        except DecodeError:
            print("Error decoding from {0} Datamine...".format(id))


    def fetch2(self, session, id):
        #print("Updating train info for ID: {0}...".format(id))
        feed = gtfs_realtime_pb2.FeedMessage()
        #print "Retriving info from MTA datamine..."
        try:
            with session.get(self.url + id, timeout=5) as response:
                r = response.content
                feed.ParseFromString(r)
                # Parse Entire Feed
                for e in feed.entity:
                    # Record Route of Trip
                    route = e.trip_update.trip.route_id
                    # Exclude particular routes
                    if route in self.exclude:
                        continue
                    else:
                        # Parse Stops in Entire Trip
                        for s in e.trip_update.stop_time_update:
                            print("*"*20)
                            print(s)
                            # Record Stop ID
                            s = s.stop_id[:-1]
                            # Check if the stop is combined to another
                            if s in self.combine.keys():
                                stop = self.combine[s]
                            else:
                                stop = s
                            if stop not in self.dict.keys():
                                # Check if stop is already in dict
                                self.dict[stop] = [route]
                            elif route in self.dict[stop]:
                                # Check if route is already in dict's list
                                continue
                            else:
                                self.dict[stop].append(route)
                            break
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()
        except ConnectionError:
            print("Error connecting to the {0} Datamine...".format(id))
        except DecodeError:
            print("Error decoding from {0} Datamine...".format(id))

    async def get_data_asynchronous(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            with requests.Session() as session:
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        self.fetch,
                        *(session, id)
                    )
                    for id in self.ids
                ]
                for response in await asyncio.gather(*tasks):
                    pass

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
        self.dict = {}
        self.client = opc.Client('localhost:7890')
        with open("resources/light_order.json", "r") as f:
            self.light_order = json.load(f)
        f.close()

    def update_pixels(self, dict):
        pixels = []
        for stop in self.light_order:
            if stop not in dict.keys():
                # No train at station
                pixels.append((0,0,0))
            else:
                pixels.append(self.color_blend(dict[stop]))
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

def startup(test):
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

    print("\n*** Updating Trains. Press CTRL+C to Exit *** \n")
    while True:
        # Create empty dictionary to be populated
        mta.dict = {}
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(mta.get_data_asynchronous())
        loop.run_until_complete(future)
        pixels = lights.update_pixels(mta.dict)
        lights.client.put_pixels(pixels, channel=0)

        #print("Trains Updated in {0} sec".format(round((time.time()-t1),2)))
        #print("Elapsed Time: {0} sec\n".format(round((time.time()-t0),2)))
