import subprocess, opc

pixels = []

for i in range(512):
	pixels.append((255,255,255))

#subprocess.Popen(["sudo", "fcserver", "/usr/local/bin/fcserver.json"])
while True:
	client = opc.Client('localhost:7890')
	client.put_pixels(pixels, channel=0)
