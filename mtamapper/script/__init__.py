import argparse, sys, subprocess, os, time
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

    if sys.platform in ['win32', 'linux']:
        raise OSError('gl_server can only run on MacOSX')

    resp = subprocess.Popen(
        [f"{PATH}/bin/gl_server","-l",f"{PATH}/lib/layout.json"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, error = resp.communicate()

    print('error',error)

def _start_fc_server():

    if sys.platform == 'linux':
        command = [f"{PATH}/bin/fcserver-rpi",f"{PATH}/lib/fcserver.json"]
    elif sys.platform == 'darwin':
        command = [f".{PATH}/bin/fcserver-macos",f"{PATH}/lib/fcserver.json"]
    else:
        command = [f".{PATH}/bin/fcserver.exe",f"{PATH}/lib/fcserver.json"]

    resp = subprocess.Popen(command, shell=True)

    output, error = resp.communicate()

    print('output',output)

def main():

    args = _get_args()

    _ = _start_gl_server() if args.simulation else _start_fc_server()

    client = opc.Client(f'{args.IP_ADDR}:{args.PORT}', verbose=args.verbose)

    mta = MTA()
    lights = Lights()

    lights.startup()

    print("\n*** Updating Trains. Press CTRL+C to Exit *** \n")

    while True:
        # Create empty dictionary to be populated
        trains = mta.update()
        pixels = lights.update_pixels(trains)
