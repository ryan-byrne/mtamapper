import time, opc, sys, csv, json
from generate_stops import Generate
from lights import Lights

# Takes stop IDs from a file and creates a Parsable Python Dictionary

def get_stops():
    stop_dict = {}
    with open("google_transit/stops.txt") as f:
        stops = csv.DictReader(f)
        for stop in stops:
            id = stop["stop_id"]
            if id not in stop_dict.keys() and id[0] not in ["S", "H", "9"]:
                stop_dict[stop["stop_id"]] = {}
                stop_dict[stop["stop_id"]]["stop_name"] = stop["stop_name"]
                stop_dict[stop["stop_id"]]["lat"] = round(20*(float(stop["stop_lat"])-40.7), 5)
                stop_dict[stop["stop_id"]]["lon"] = round(20*(float(stop["stop_lon"])+73.9), 5)
            else:
                continue
    return stop_dict

def TEST_CONNECT():
    #-------------------------------------------------------------------------------
    # handle command line
    if len(sys.argv) == 1:
        IP_PORT = '127.0.0.1:7890'
    elif len(sys.argv) == 2 and ':' in sys.argv[1] and not sys.argv[1].startswith('-'):
        IP_PORT = sys.argv[1]
    else:
        print('''
    Usage: raver_plaid.py [ip:port]

    If not set, ip:port defauls to 127.0.0.1:7890
    ''')
        sys.exit(0)
    #-------------------------------------------------------------------------------
    # connect to server
    client = opc.Client(IP_PORT)
    if client.can_connect():
        print('    connected to %s' % IP_PORT)
    else:
        # can't connect, but keep running in case the server appears later
        print('    WARNING: could not connect to %s' % IP_PORT)
    print('')


    #-------------------------------------------------------------------------------
    # send pixels

    print('    sending pixels forever (control-c to exit)...')
    print('')
    return client

if __name__ == '__main__':
    print "Opening the LED testing client..."
    client = TEST_CONNECT()
    old_stops = []
    print "Beginning Timer..."
    t = time.time()
    print "Populating a dictionary of stops"
    stop_dict = get_stops()
    #l.run(stops, old_stops, stop_dict, client)
    while True:
        print "Retriving current stops..."
        current_stops = Generate.run()
        #print stops
        print "Sending commands to lights..."
        Lights.run(current_stops, old_stops, client)
        old_stops = current_stops
        elapsed = time.time() - t
        print "Complete!"
        print "Running for: " + str(round(elapsed/60,2)) + " minutes"
        time.sleep(0.05)
