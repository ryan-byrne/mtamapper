from flask import Flask, render_template
import json, time, threading
from ..mta import MTA
from ..lights import Lights, Client

app = Flask(__name__)
mta = MTA()
lights = Lights()

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

def _update_thread(client):

    global ACTIVE

    if client.can_connect():
        # Startup Script
        lights.startup(client)

    while True:
        if not client.can_connect():
            print("[WARNING] Unable to connect to FadeCandy Server...")
            time.sleep(3)
        elif not ACTIVE:
            print("[INFO] Map is inactive")
            time.sleep(3)
        else:
            trains = mta.update()
            pixels = lights.update_pixels(trains)
            client.put_pixels(pixels)


def start_server(ip="127.0.0.1", http_port="5000", client_port="7890", debug=False, verbose=False):
    # Connect to Client
    client = Client(f"{ip}:{client_port}", verbose=verbose, long_connection=True)
    # Start the update thread
    threading.Thread(target=_update_thread, args=(client,)).start()
    # Start the Server
    app.run(ip, http_port, debug)