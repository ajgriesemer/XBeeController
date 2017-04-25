"""https://github.com/liwp/python-xbee-demo/blob/master/xbee-demo.py"""

from xbee import XBee
from xbee.helpers.dispatch import Dispatch
import serial
import struct
import time
import os

HUB_ADDR = struct.pack('>Q', 0)  # 64-bit 0s
BCAST_ADDR = '\xFF\xFE'

IS_HUB = bool(os.getenv('IS_HUB'))


def default_handler(name, packet):
    print("%s - %s" % (name, packet))


def at_response_handler(name, packet):
    print(packet)


def rx_handler(name, packet):
    print("RX - %s" % packet)
    time.sleep(1)
    data = "PONG" if IS_HUB else "PING"
    xbee.tx(dest_addr_long=packet['source_addr_long'], dest_addr=packet['source_addr'], data=data)


ser = serial.Serial('/dev/ttyS0', 9600)
dispatch = Dispatch()
dispatch.register('rx', rx_handler, lambda p: p['id'] == 'rx')
dispatch.register('rx_explicit', default_handler, lambda p: p['id'] == 'rx_explicit')
dispatch.register('rx_io_data_long_addr', default_handler, lambda p: p['id'] == 'rx_io_data_long_addr')
dispatch.register('rx_io_data', default_handler, lambda p: p['id'] == 'rx_io_data')
dispatch.register('tx_status', default_handler, lambda p: p['id'] == 'tx_status')
dispatch.register('status', default_handler, lambda p: p['id'] == 'status')
dispatch.register('at_response', at_response_handler, lambda p: p['id'] == 'at_response')
dispatch.register('remote_at_response', default_handler, lambda p: p['id'] == 'remote_at_response')
dispatch.register('node_id_indicator', default_handler, lambda p: p['id'] == 'node_id_indicator')

xbee = XBee(ser, callback=dispatch.dispatch, escaped=True)
dispatch.xbee = xbee

print("run...")
print("")
print("current status:")
xbee.send('at', command=b'ID', frame_id=b'\x01')
xbee.send('at', command=b'SH', frame_id=b'\x01')
xbee.send('at', command=b'SL', frame_id=b'\x01')
xbee.send('at', command=b'MY', frame_id=b'\x01')
print("")

time.sleep(1)

print("")
while True:
    try:
        time.sleep(2)
    except KeyboardInterrupt:
        break

xbee.halt()

ser.close()