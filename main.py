import time, opc, sys, csv, json, subprocess, os
from generate_stops import Generate
from lights import Lights
from opc import struct

# Takes stop IDs from a file and creates a Parsable Python Dictionary
if __name__ == '__main__':
    print "Starting the FadeCandy Server..."
    #os.system("sudo fcserver /usr/local/bin/fcserver.json")
    print "Connect to the LED FadeCandy client..."
    client = opc.Client('localhost:7890')
    old_stops = []
    print "Beginning Timer..."
    t = time.time()
    while True:
        print "Retriving current stops..."
        current_stops = Generate.run()
        try:
            Lights.run(current_stops, old_stops, client)
        except struct.error:
            print "Issue sending pixels to the board. Continuing..."
        old_stops = current_stops
        elapsed = time.time() - t
        print "Running for: " + str(round(elapsed/60,2)) + " minutes"
