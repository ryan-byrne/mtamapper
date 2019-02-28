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
                stop_dict[stop["stop_id"]] = {}
                stop_dict[stop["stop_id"]]["stop_name"] = stop["stop_name"]
                #print stop["stop_id"]
        f.close()
        for key in stop_dict.keys():
            try:
                int(key[-2:])
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
            response = urllib2.urlopen('http://datamine.mta.info/mta_esi.php?key='+key+'&feed_id='+id, 'rb')
            try:
                feed.ParseFromString(response.read())
            except:
                pass
            feed_array.append(feed)
        return feed_array

    # Generate the list of Station IDs currently with trains
    @staticmethod
    def parse_info(feed):
        stops_array = []
        for entity in feed.entity:
            # Example stop: 206N
            stops = entity.trip_update.stop_time_update
            route = entity.trip_update.trip.route_id
            for stop in stops:
                id = stop.stop_id[0]
                if id == "S" or id == "9" or id == "H":
                    continue
                else:
                    stops_array.append([stop.stop_id[:-1], route])
                    break
            #stop = stops[0]
            #print stops
        return stops_array

    @staticmethod
    def run():
        all_stops = []
        feed_array = Generate.update_train_info()
        for feed in feed_array:
            stops = Generate.parse_info(feed)
            for stop in stops:
                all_stops.append(stop)
        return all_stops
