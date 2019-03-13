from google.transit import gtfs_realtime_pb2
import urllib2, csv, time, json

stops = []

class Generate():
    # Pull real time train data from google transit
    @staticmethod
    def update_train_info():
        current_trains = []
        id_array = ["1", "26", "16", "21", "2", "31", "36", "51"]
        exclude = ["9", "S"]
        key = "aec131a835263208ee94b402590bb930"
        for id in id_array:
            feed = gtfs_realtime_pb2.FeedMessage()
            response = urllib2.urlopen('http://datamine.mta.info/mta_esi.php?key='+key+'&feed_id='+id, 'rb')
            feed.ParseFromString(response.read())
            for entity in feed.entity:
                for stop in entity.trip_update.stop_time_update:
                    s = stop.stop_id[:-1]
                    r = stop.stop_id[0]
                    if s == "R60" or s in current_trains or r in exclude:
                        continue
                    else:
                        current_trains.append(stop.stop_id[:-1])
                    break
        return current_trains

    # Generate the list of Station IDs currently with trains
    @staticmethod
    def run():
        current_trains = Generate.update_train_info()
        return current_trains
