import argparse, sys, subprocess, os, time
from mtamapper import MTA, Lights, utils, opc

PATH = os.path.dirname(utils.__file__)

def _get_args():
    parser = argparse.ArgumentParser(description="A Python Package for controlling an LED map of the MTA Subway system")
    parser.add_argument('-v', dest="verbose", action="store_true",help="Run in Verbose Mode")
    parser.add_argument('-s', dest="simulation", action="store_true",help="Run in Simulation Mode")
    parser.add_argument('-i', dest="IP_ADDR", nargs="?", default='localhost', const="localhost", help="IP Address where the OPC Server will run")
    parser.add_argument('-p', dest="PORT", nargs="?", default='localhost', const="7890", help="Port where the OPC Server will run")
    return parser.parse_args()

def main():

    args = _get_args()

    print(f".{PATH}/bin/fcserver-osx")

    if args.simulation:
        command = [f"{PATH}/lib/gl_server","-l",f"{PATH}/lib/layout.json"]
    elif sys.platform == 'linux':
        command = [f".{PATH}/bin/fcserver-rpi",f"{PATH}/lib/fcserver.json"]
    elif sys.platform == 'darwin':
        command = [f".{PATH}/bin/fcserver-osx"]
    else:
        raise OSError("Windows is not supported")

    subprocess.Popen(command, shell=True)

    client = opc.Client('localhost:7890', verbose=args.verbose)

    mta = MTA()
    lights = Lights()

    lights.startup()

    print("\n*** Updating Trains. Press CTRL+C to Exit *** \n")

    while True:
        # Create empty dictionary to be populated
        trains = mta.update()
        pixels = lights.update_pixels(trains)
