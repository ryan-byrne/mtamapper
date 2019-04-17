from google.transit import gtfs_realtime_pb2
from google.protobuf.message import DecodeError
import urllib2, csv, time, json
from urllib2 import URLError

stops = []

class Generate():
    # Pull real time train data from google transit
    @staticmethod
    def update_train_info():
        current_trains = []
        id_array = ["1", "26", "16", "21", "2", "31", "36", "51"]
        key = "aec131a835263208ee94b402590bb930"
        exclude = ["9", "S", "FS", "", "GS"]
        recording = False
        for id in id_array:
            feed = gtfs_realtime_pb2.FeedMessage()
            try:
                response = urllib2.urlopen('http://datamine.mta.info/mta_esi.php?key='+key+'&feed_id='+id, 'rb')
            except URLError:
                print "Error reading data from MTA datamine. Continuing..."
            try:
                feed.ParseFromString(response.read())
                print "Sending commands to the lights..."
            except DecodeError:
                print "Error reading data from Google. Continuing..."
                return []
            for e in feed.entity:
                r = e.trip_update.trip.route_id
                if r in exclude:
                    continue
                else:
                    for stops in e.trip_update.stop_time_update:
                        s = stops.stop_id[:-1]
                        break
                    current_trains.append([r, s])
        return current_trains

    # Generate the list of Station IDs currently with trains
    @staticmethod
    def run():
        current_trains = Generate.update_train_info()
        return current_trains
