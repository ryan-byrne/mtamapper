from flask import Flask, render_template
import json, time, threading
from ..mta import MTA
from ..lights import Lights, Client

app = Flask(__name__)
ACTIVE = False

@app.route('/stop', methods=['POST'])
def stop():

    global ACTIVE

    if ACTIVE:
        ACTIVE = False
        return "Stopped", 200
    else:
        return "Lights are already stopped", 500

@app.route('/start', methods=['POST'])
def start():

    global ACTIVE

    if ACTIVE:
        return "Map is already active", 500
    else:
        ACTIVE = True
        return "Map has been started", 200

@app.route('/status', methods=['GET'])
def status():

    global ACTIVE

    return(json.dumps({"active":ACTIVE}))

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

def _update_thread(ip, port, verbose, startup):

    client = Client(f"{ip}:{port}", verbose=verbose)
    mta = MTA()
    lights = Lights()


    if client.can_connect() and startup:
        lights.startup(client)

    while True:

        global ACTIVE

        if not client.can_connect():
            print("[WARNING] Unable to connect to FadeCandy Server...")
            time.sleep(3)
        elif not ACTIVE:
            pixels = lights.clear_pixels()
            client.put_pixels(pixels)
            time.sleep(3)
        else:
            trains = mta.update()
            pixels = lights.update_pixels(trains)
            client.put_pixels(pixels)

def run(args):

    print([args.ip, args.client_port, args.verbose, args.startup])

    # Start Updating the Trains
    threading.Thread( target=_update_thread, args=[args.ip, args.client_port, args.verbose, args.startup] ).start()
    # Start the HTTP Server
    app.run( host=args.ip, port=args.http_port, debug=args.debug )
