import sys

status = {}

class Lights():

    @staticmethod
    def control(on, off):
        for stop in on:
            if stop[0] not in status:
                status[stop[0]] = [stop[1]]
            else:
                if stop[1] not in status[stop[0]]:
                    status[stop[0]].append(stop[1])
                else:
                    continue
        for stop in off:
            if stop[0] not in status:
                status[stop[0]] = []
            else:
                try:
                    status[stop[0]].remove(stop[1])
                except ValueError:
                    print status[stop[0]]
                    continue
        # Here's where the magic happens baby. Later add LED control via
        # the raspberry Pi.
        for stop in status.keys():
            if status[stop] == []:
                signal = "off"
            elif len(status[stop]) > 1:
                signal = Lights.color_blend(status[stop])
            else:
                signal = status[stop][0]
            print stop, signal

    @staticmethod
    def color_blend(color_array):
        return color_array

    @staticmethod
    def test():
        pass
        #client.put_pixels(pixels, channel=0)

    @staticmethod
    def run(stops, old_stops):
        client = Lights.TEST_CONNECT()
        print client
        off = []
        on = []
        for stop in stops:
            if stop not in old_stops:
                on.append(stop)
        for stop in old_stops:
            if stop not in stops:
                off.append(stop)
        #Lights.control(on, off)
