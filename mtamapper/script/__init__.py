import argparse, sys, subprocess, os, time
from ipaddress import ip_address
from mtamapper import MTA, Lights, utils, opc

PATH = os.path.dirname(utils.__file__)

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
    print(f"Using Configuration at: {PATH}/lib/fcserver.json")

    if sys.platform in ['darwin', 'linux']:
        subprocess.Popen(["sudo","fcserver",f"{PATH}/lib/fcserver.json"])
    else:
        return

def main():

    args = _get_args()

    _ = _start_gl_server() if args.simulation else _start_fc_server()
    time.sleep(3)
    
    print(f'Connecting to OPC Client at {args.IP_ADDR}:{args.PORT}...')
    client = opc.Client(f"{args.IP_ADDR}:{args.PORT}", verbose=args.verbose)
    if not client.can_connect():
        raise ConnectionError(f"OPC client was unable to connect to a server at {args.IP_ADDR}:{args.PORT}...")
    
    print('Starting the MTA Data Feed...')
    mta = MTA()
    
    print('Initializing Light Control...')
    lights = Lights()

    _ = lights.startup(client) if args.startup else None

    print("\n*** Updating Trains. Press CTRL+C to Exit *** \n")

    while True:
        # Create empty dictionary to be populated
        trains = mta.update()
        pixels = lights.update_pixels(trains)
        client.put_pixels(pixels)