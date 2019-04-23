import time, opc, sys, csv, json
from generate_stops import Generate
from lights import Lights

# Takes stop IDs from a file and creates a Parsable Python Dictionary

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
    print
    print(' Ready to send pixels!')
    print('')
    return client

if __name__ == '__main__':
    print "Opening the LED testing client..."
    #client = TEST_CONNECT()
    client = opc.Client('localhost:7890')
    old_stops = []
    print "Beginning Timer..."
    t = time.time()
    #l.run(stops, old_stops, stop_dict, client)
    while True:
        print "Retriving current stops..."
        current_stops = Generate.run()
        Lights.run(current_stops, old_stops, client)
        old_stops = current_stops
        elapsed = time.time() - t
        print "Running for: " + str(round(elapsed/60,2)) + " minutes"
