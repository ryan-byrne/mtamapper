from google.transit import gtfs_realtime_pb2
import urllib2, csv, time

stops = []

class Generate():

    # Takes stop IDs from a file and creates a Parsable Python Dictionary
    @staticmethod
    def get_stops():
        count = 0
        stop_dict = {}
        stop_list = []
        with open("google_transit/stops.txt") as f:
            stops = csv.DictReader(f)
            for stop in stops:
                #print stop["stop_name"], stop["stop_id"]
                stop_dict[stop["stop_id"]] = {}
                stop_dict[stop["stop_id"]]["stop_name"] = stop["stop_name"]
                #print stop["stop_id"]
        f.close()
        for key in stop_dict.keys():
            try:
                int(key[-2:])
                if key[0] == "5":
                    print stop_dict[key]["stop_name"]
                if key[0] == "S" or key[0] == "9" or key[0] == "H":
                    #print key[0]
                    continue
                elif stop_dict[key]["stop_name"] in stop_list:
                    #print stop_dict[key]["stop_name"], key
                    continue
                else:
                    #print stop_dict[key]["stop_name"]
                    stop_list.append(stop_dict[key]["stop_name"])
                    count += 1
            except ValueError:
                continue
        #print stop_dict
        #print len(stop_list)
        #print count
        #print stop_list
        return stop_dict

    # Pull real time train data from google transit
    @staticmethod
    def update_train_info():
        feed_array = []
        id_array = ["1", "26", "16", "21", "2", "31", "36", "51"]
        key = "aec131a835263208ee94b402590bb930"
        for id in id_array:
            feed = gtfs_realtime_pb2.FeedMessage()
            response = urllib2.urlopen('http://datamine.mta.info/mta_esi.php?key='+key+'&feed_id='+id)
            try:
                feed.ParseFromString(response.read())
            except google.protobuf.message.DecodeError:
                print "Too many requests. Waiting..."
                time.sleep(3)
                self.update_train_info()
            feed_array.append(feed)
        return feed_array

    # Generate the list of Station IDs currently with trains
    @staticmethod
    def parse_info(feed, stop_dict):
        for entity in feed.entity:
            id = entity.id
            vehicle = entity.vehicle
            #print vehicle
            stop = vehicle.stop_id
            # Example stop: 206N
            if vehicle.current_status == 1:
                if stop == "":
                    #dir = vehicle.trip.trip_id[-1:]
                    stop_seq = vehicle.current_stop_sequence
                    if stop_seq < 10:
                        stop_seq = "0"+str(stop_seq)
                    else:
                        stop_seq = str(stop_seq)
                    route = vehicle.trip.route_id
                    stop = route+stop_seq
                """
                else:
                    dir = stop[-1:]
                print vehicle.trip.route_id+" train is stopped at "+stop
                print vehicle
                """
                try:
                    int(stop[-2:])
                    stops.append(stop)
                except ValueError:
                    continue

    @staticmethod
    def run():
        sorted_stops = []
        stop_dict = Generate.get_stops()
        feed_array = Generate.update_train_info()
        for feed in feed_array:
            Generate.parse_info(feed, stop_dict)
        for stop in stops:
            if stop not in sorted_stops:
                sorted_stops.append(stop)
        return sorted_stops
