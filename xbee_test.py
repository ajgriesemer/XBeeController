import serial
import time
from xbee import XBee
import xbee as xb
import time

serial_port = serial.Serial('/dev/ttyS0', 9600)

def print_data(data):
    """
    This method is called whenever data is received
    from the associated XBee device. Its first and
    only argument is the data contained within the
    frame.
    """
    print(data)

xbee = XBee(serial_port, callback=print_data,escaped=True)
time.sleep(1)
xbee.send("at", frame_id=b'\x01', command=b'MY')
xbee.send("at", frame_id=b'\x01', command=b'SH')
xbee.send("at", frame_id=b'\x01', command=b'SL')
time.sleep(1)

while True:
    try:
        time.sleep(0.001)
    except KeyboardInterrupt:
        break

xbee.halt()
serial_port.close()