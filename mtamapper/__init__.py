from flask import Flask, render_template_string
import argparse, sys, subprocess, os, time, threading, json
from .lights import Lights
from .mta import MTA
from .utils import APP_TEMPLATE, opc

PATH = os.path.dirname(argparse.__file__)
print(PATH)
app = Flask(__name__)
mta = MTA()
lights = Lights()

# API
@app.route('/stop', methods=['POST'])
def stop():
    if mta.active:
        mta.active = False
        return "Stopped", 200
    else:
        return "Lights are already stopped", 500

@app.route('/start', methods=['POST'])
def start():
    if mta.active:
        mta.active = True
        return "Started", 200
    else:
        return "Lights are already on", 500

@app.route('/status', methods=['GET'])
def status():
    return(json.dumps({"active":mta.active}))

@app.route('/', methods=['GET'])
def index():
    return render_template_string(APP_TEMPLATE)

# SCRIPTS

# Get Command Line Arguments
def _get_args():
    parser = argparse.ArgumentParser(description="A Python Package for controlling an LED map of the MTA Subway system")
    parser.add_argument('-v', dest="verbose", action="store_true",help="Run in Verbose Mode")
    parser.add_argument('-s', dest="simulation", action="store_true",help="Run in Simulation Mode")
    parser.add_argument('-i', dest="IP_ADDR", nargs="?", default='localhost', const="localhost", help="IP Address for OPC Server (Defaults to localhost)")
    parser.add_argument('-p', dest="PORT", nargs="?", type=int, default=7890, const=7890, help="Port for the OPC Server (defaults to )")
    parser.add_argument('--run-startup', dest="startup", action="store_true", help="Run a startup script that illuminates each light one by one")
    return parser.parse_args()

def _flask_server():
    print("Starting Flask Server...")
    app.run(host='0.0.0.0', port=5000)

def _fc_server():
    STATUS = "starting-fadecandy"
    print("Starting the FadeCandy Server...")
    CONFIG_PATH = os.path.normpath(f"{PATH}/lib/fcserver.json")
    print(f"Using Configuration at: {CONFIG_PATH}")

    if sys.platform == 'linux':
        subprocess.Popen(["sudo","fcserver",f"{PATH}/lib/fcserver.json"])
    elif sys.platform == 'win32':
        subprocess.Popen([f"{PATH}\\bin\\fcserver.exe",f"{PATH}/lib/fcserver.json"])
    else:
        subprocess.Popen(["source",f"{PATH}/bin/fcserver-osx",f"{PATH}/lib/fcserver.json"])

def _gl_server():

    print("Starting Simulation Server")

    if sys.platform in ['win32', 'linux']:
        raise OSError('gl_server can only run on MacOSX')

    subprocess.Popen([f"{PATH}/bin/gl_server","-l",f"{PATH}/lib/layout.json"], shell=True)

def main():
    
    # Get Arguments
    args = _get_args()
    
    # Start the fadecandy server
    if args.simulation:
        threading.Thread(target=_gl_server).start()
    else:
        threading.Thread(target=_fc_server).start()
    
    # Start the OpenPixelControl Client 
    client = opc.Client(f"{args.IP_ADDR}:{args.PORT}", verbose=args.verbose)
    if not client.can_connect():
        raise ConnectionError(f"OPC client was unable to connect to a server...")
    

    # Run startup function if "--run-startup" argument
    _ = lights.startup(client) if args.startup else None

    # Start Flask Control Server
    threading.Thread(target=_flask_server).start()

    print("\n*** Updating Trains. Press CTRL+C to Exit *** \n")

    while True:
        if mta.active:
            # Update the current status of trains
            trains = mta.update()
            # Set the color of their respective LEDs
            pixels = lights.update_pixels(trains)
            # Send LED colors to the FadeCandy Server
            client.put_pixels(pixels)
        else:
            no_pixels = lights.clear_pixels()
            client.put_pixels(no_pixels)
            time.sleep(3)

if __name__ == '__main__':
    main()