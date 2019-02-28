import time
from generate_stops import Generate
from lights import Lights as l

if __name__ == '__main__':
    old_stops = []
    t = time.time()
    while True:
        stops = Generate.run()
        #print stops
        l.run(stops, old_stops)
        old_stops = stops
        elapsed = time.time() - t
        print "Running for: " + str(elapsed/60) + " minutes"
        time.sleep(1)
