import argparse, sys, subprocess, os, time, threading
from flask import Flask
from mtamapper import MTA, Lights, utils, opc

PATH = os.path.dirname(utils.__file__)
ACTIVE = False

app = Flask(__name__)

@app.route('/start', methods=['POST'])
def start():
    return "Success!", 200

@app.route('/stop', methods=['POST'])
def stop():
    return "Success!", 200

@app.route('/', methods=['GET'])
def index():
    return "Hello world"

def _get_args():
    parser = argparse.ArgumentParser(description="A Python Package for controlling an LED map of the MTA Subway system")
    parser.add_argument('-v', dest="verbose", action="store_true",help="Run in Verbose Mode")
    parser.add_argument('-s', dest="simulation", action="store_true",help="Run in Simulation Mode")
    parser.add_argument('-i', dest="IP_ADDR", nargs="?", default='localhost', const="localhost", help="IP Address for OPC Server (Defaults to localhost)")
    parser.add_argument('-p', dest="PORT", nargs="?", type=int, default=7890, const=7890, help="Port for the OPC Server (defaults to )")
    parser.add_argument('--run-startup', dest="startup", action="store_true", help="Run a startup script that illuminates each light one by one")
    return parser.parse_args()

def _start_gl_server():

    print("Starting Simulation Server")

    if sys.platform in ['win32', 'linux']:
        raise OSError('gl_server can only run on MacOSX')

    subprocess.Popen([f"{PATH}/bin/gl_server","-l",f"{PATH}/lib/layout.json"], shell=True)

def _start_fc_server():

    print("Starting the FadeCandy Server...")
    CONFIG_PATH = os.path.normpath(f"{PATH}/lib/fcserver.json")
    print(f"Using Configuration at: {CONFIG_PATH}")

    if sys.platform == 'linux':
        subprocess.Popen(["sudo","fcserver",f"{PATH}/lib/fcserver.json"])
    elif sys.platform == 'win32':
        subprocess.Popen([f"{PATH}\\bin\\fcserver.exe",f"{PATH}/lib/fcserver.json"])
    else:
        subprocess.Popen(["source",f"{PATH}/bin/fcserver-osx",f"{PATH}/lib/fcserver.json"])

def _start_flask_server():
    print("Starting Flask Server...")
    app.run(host='0.0.0.0', port=5000)

def main():

    args = _get_args()

    _ = _start_gl_server() if args.simulation else _start_fc_server()

    mta = MTA()
    lights = Lights()
    
    client = opc.Client(f"{args.IP_ADDR}:{args.PORT}", verbose=args.verbose)
    if not client.can_connect():
        raise ConnectionError(f"OPC client was unable to connect to a server at {args.IP_ADDR}:{args.PORT}...")

    _ = lights.startup(client) if args.startup else None

    threading.Thread(target=_start_flask_server).start()

    print("\n*** Updating Trains. Press CTRL+C to Exit *** \n")

    while True:
        # Update the current status of trains
        trains = mta.update()
        # Set the color of their respective LEDs
        pixels = lights.update_pixels(trains)
        # Send LED colors to the FadeCandy Server
        client.put_pixels(pixels)