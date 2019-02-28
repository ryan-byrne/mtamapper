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
        off = []
        on = []
        for stop in stops:
            if stop not in old_stops:
                on.append(stop)
        for stop in old_stops:
            if stop not in stops:
                off.append(stop)
        Lights.control(on, off)
