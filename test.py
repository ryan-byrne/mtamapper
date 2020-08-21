import opc, sys, subprocess, time, json
import pandas as pd

if sys.platform == "darwin":
    layout = "/Users/rbyrne/projects/mta-map/resources/layout.json"
    server = "/Users/rbyrne/projects/mta-map/resources/opc/bin/gl_server"
    command = [server,"-l",layout]
else:
    fcserver = "/usr/local/bin/fcserver"
    config = "/usr/local/bin/fcserver.json"
    command = [fcserver,config]

subprocess.Popen(command)
client = opc.Client('localhost:7890')

with open("resources/light_order.json") as f:
    light_order = json.load(f)
f.close()

df = pd.read_csv("google_transit/stops.txt")
for i, light in enumerate(light_order):
    pixels = [ (0,0,0) ] * 443
    pixels[i] = (255, 255, 255)
    client.put_pixels(pixels)
    print(light, df.loc[df['stop_id'] == light]["stop_name"].values)
    time.sleep(1)
