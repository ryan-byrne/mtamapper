import time, opc, sys
from generate_stops import Generate
from lights import Lights as l


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
