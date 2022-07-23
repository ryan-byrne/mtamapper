import requests, argparse, threading, time
from .mta import MTA
from .lights import opc, Lights

# Get Command Line Arguments
def _get_args():
    parser = argparse.ArgumentParser(description="A Python Package for controlling an LED map of the MTA Subway system")
    parser.add_argument('-v', dest="verbose", action="store_true",help="Run in Verbose Mode")
    parser.add_argument('-s', dest="simulation", action="store_true",help="Run in Simulation Mode")
    parser.add_argument('-i', dest="ip", nargs="?", default='127.0.0.1', help="IP Address for OPC Server (Defaults to localhost)")
    parser.add_argument('-p', dest="port", nargs="?", type=int, default=7890, help="Port for the OPC Server (defaults to )")
    parser.add_argument('--run-startup', dest="startup", action="store_true", help="Run a startup script that illuminates each light one by one")
    return parser.parse_args()

def test():
    mta = MTA()
    while True:
        try:
            trains = mta.update()
            print(trains)
        except KeyboardInterrupt:
            break

def main():
    
    # Get Arguments
    args = _get_args()
    
    # Start the OpenPixelControl Client 
    client = opc.Client(f"{args.ip}:{args.port}", verbose=args.verbose)
    if not client.can_connect():
        raise ConnectionError(f"OPC client was unable to connect to a server at {args.ip}:{args.port}...")
    
    mta = MTA()
    lights = Lights()

    # Run startup function if "--run-startup" argument
    #_ = lights.startup(client) if args.startup else None

    # Start Flask Control Server
    #threading.Thread(target=_flask_server).start()

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