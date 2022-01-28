import argparse, sys, subprocess, os, time
from mtamapper import MTA, Lights, utils, opc

PATH = os.path.dirname(utils.__file__)

def main():
    #!/usr/bin/env python
    # Start the corresponding FC server

    print(sys.platform)

    if sys.platform == "darwin":
        layout = f"{PATH}/lib/layout.json"
        server = "/Users/rbyrne/projects/mta-map/lib/opc/bin/gl_server"
        subprocess.Popen([server,"-l",layout])
    else:
        fcserver = "/usr/local/bin/fcserver"
        config = "/usr/local/bin/fcserver.json"
        subprocess.Popen([fcserver,config])


    mta = MTA()
    lights = Lights()

    lights.startup()

    print("\n*** Updating Trains. Press CTRL+C to Exit *** \n")
    while True:
        # Create empty dictionary to be populated
        trains = mta.update()
        pixels = lights.update_pixels(trains)

def test():

    print("Starting MTAMapper Test Script")
    print('Reading System Platform')

    if sys.platform == "darwin":
        print("Running on MacOSX")
        print("Starting GL Server...")
        layout = f"{PATH}/lib/layout.json"
        server = f"{PATH}/lib/gl_server"
        command = [server,"-l",layout]
    else:
        print("Running on Linux")
        print("Starting FadeCandy Server...")
        fcserver = "/usr/local/bin/fcserver"
        config = "/usr/local/bin/fcserver.json"
        command = [fcserver,config]

    print(f"System Platform is: {sys.platform}")
    print(f"Running: {command}")

    subprocess.Popen(command)

    print("Starting OpenPixelControl Client at localhost:7890")
    client = opc.Client('localhost:7890', verbose=True)

    mta = MTA()
    lights = Lights()

    while True:
        trains = mta.update()
        pixels = lights.update_pixels(trains)
