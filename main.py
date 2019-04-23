import time, opc, sys, csv, json
from generate_stops import Generate
from lights import Lights

# Takes stop IDs from a file and creates a Parsable Python Dictionary

if __name__ == '__main__':
    print "Opening the LED FadeCandy client..."
    client = opc.Client('localhost:7890')
    old_stops = []
    print "Beginning Timer..."
    t = time.time()
    while True:
        print "Retriving current stops..."
        current_stops = Generate.run()
        Lights.run(current_stops, old_stops, client)
        old_stops = current_stops
        elapsed = time.time() - t
        print "Running for: " + str(round(elapsed/60,2)) + " minutes"
