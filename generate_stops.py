from google.transit import gtfs_realtime_pb2
import urllib2, csv, time

stops = []
colors = {
    "4":"#00933C",
    "5":"#00933C",
    "6":"#00933C",
    "6X":"#00933C",
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
    "M":"#FF6319",
    "N":"#FCCC0A",
    "Q":"#FCCC0A",
    "R":"#FCCC0A",
    "W":"#FCCC0A",
    "G":"#6CBE45",
    "L":"#A7A9AC",
    "J":"#996633",
    "Z":"#996633",
}


class Generate():
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
                    try:
                        stops_array.append([stop.stop_id[:-1], colors[route]])
                    except KeyError:
                        continue
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
