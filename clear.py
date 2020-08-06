import opc

if __name__ == '__main__':
    client = opc.Client('localhost:7890')
    pixels = [ (0,0,0) ] * 443
    client.put_pixels(pixels)
