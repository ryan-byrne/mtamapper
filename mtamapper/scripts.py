import argparse
from .server import start_server

# Get Command Line Arguments
def _get_args():
    parser = argparse.ArgumentParser(description="A Python Package for controlling an LED map of the MTA Subway system")
    parser.add_argument('-i', dest="ip", nargs="?", default='127.0.0.1', help="IP Address for Flask Server")
    parser.add_argument('-p', dest="http_port", nargs="?", type=int, default=5000, help="Port for the Flask Server")
    parser.add_argument('--client_port', default="7890", help="Port for the Client Server")
    parser.add_argument('-d', dest="debug", action="store_true", help="Run the Map in debugging mode")
    parser.add_argument('-v', dest="verbose", action="store_true", help="Run the Client in verbose mode")
    return vars(parser.parse_args())

def test():
    start_server(True)

def main():
    
    # Get Arguments
    args = _get_args()

    start_server(**args)

if __name__ == '__main__':
    main()