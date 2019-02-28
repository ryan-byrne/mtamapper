

class Lights():

    @staticmethod
    def control(on, off):
        print "Turn on"
        for stop in on:
            print stop
        print "Turn off"
        for stop in off:
            print stop

    @staticmethod
    def run(stops, old_stops):
        for stop in stops:
            print ""
            print "There is a " + str(stop[1]) + " train at " + str(stop[0])
        #on = set(stops) - set(old_stops)
        #off = set(old_stops) - set(stops)
        #Lights.control(on, off)
