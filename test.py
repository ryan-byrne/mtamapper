import opc, sys, subprocess,time

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

while True:
    pixels = [ (0,0,250) ] * 443
    client.put_pixels(pixels, channel=1)
    time.sleep(1)
    pixels = [ (0,250,0) ] * 443
    client.put_pixels(pixels, channel=1)
    time.sleep(1)
