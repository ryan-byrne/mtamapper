import os, threading, requests, sys
from ..utils import EXCLUDE, COMBINE
from . import gtfs_realtime_pb2 as gtfs
from google.protobuf.message import DecodeError

class MTA():

    def __init__(self):

        print("Starting the MTA Data Feed...")
        self.exclude = EXCLUDE
        self.combine = COMBINE
        self.trains = {}
        self.url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"
        try:
            self.key = os.environ['MTA_API_KEY']
        except:
            raise PermissionError("\n\nERROR: MTA Realtime Feed Key (MTA_API_KEY) not found \
            \n\nGet one from: https://api.mta.info/ then add it as MTA_API_KEY in your environment\n")
        self.active = True


    def update(self):

        self.trains = {}

        threads = []

        for id in ['-ace','-bdfm','-g','-jz','-nqrw','-l','-7','']:
            threads.append(threading.Thread(target=self._update_trains, args=(id,)))

        for t in threads:
            t.start()

        for t in threads:
            t.join()
        
        #print(f"${datetime.datetime.now()} Trains Updated...")

        return self.trains

    def _update_trains(self, id):
        try:
            #print("Updating train info for ID: {0}...".format(id))
            feed = gtfs.FeedMessage()
            #print("Retriving info from MTA datamine...")
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
        except ConnectionError as e:
            print("Unable to connect to the MTA Data Stream...")
        except DecodeError:
            print("Unable to decode the message from "+id)
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()
