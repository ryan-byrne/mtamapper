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
            print "Retriving info from MTA datamine..."
            try:
                response = urllib2.urlopen('http://datamine.mta.info/mta_esi.php?key='+key+'&feed_id='+id, 'rb')
            except URLError:
                print "Error reading data from MTA datamine. Continuing..."
            print "Parsing response into Python Object"
            try:
                feed.ParseFromString(response.read())
            except DecodeError:
                print "Error reading group ", id," from Google. Continuing..."
                continue
            print "Generating list of current stops for array #", id
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
        try:
            current_trains = Generate.update_train_info()
        except UnboundLocalError:
            print "Recieved a corrupt message from the Data Feed. Retrying..."
            return
        return current_trains
