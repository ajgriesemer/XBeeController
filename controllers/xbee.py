
from xbee import XBee
from xbee.helpers.dispatch import Dispatch
from controllers import XBeeMessages
import serial
import struct
import time
import os


class XBeeController:

    def __init__(self):
        self.serial = serial.Serial('/dev/ttyS0', 9600)

        self.xbee = XBee(self.serial, callback=self.dispatch, escaped=True)
        self.callbacks = list()

    def dispatch(self, packet):
        subscriptions = [subscription for subscription in self.callbacks if subscription['message'] == packet['id'] and subscription['callback'] is not None]
        for subscription in subscriptions:
            if subscription['caller'] == None:
                subscription['callback'](subscription['message'], packet)
            else:
                subscription['callback'](subscription['caller'], subscription['message'], packet)

    def subscribe(self, message, callback, caller=None):
        if {'message': message, 'callback': callback} not in self.callbacks:
            self.callbacks.append({'message': message, 'callback': callback, 'caller': caller})

    def unsubscribe(self, message, callback, caller=None):
        subscriptions = [subscription for subscription in self.callbacks if subscription['message'] == message and subscription['callback'] == callback and subscription['caller'] == caller]
        for subscription in subscriptions:
            self.callbacks.remove(subscription)

    def query_parameters(self):
        self.subscribe(XBeeMessages.RXMessages.at_response, self.print_query_response, self)
        self.xbee.send('at', command=b'ID', frame_id=b'\x01')
        self.xbee.send('at', command=b'SH', frame_id=b'\x01')
        self.xbee.send('at', command=b'SL', frame_id=b'\x01')
        self.xbee.send('at', command=b'MY', frame_id=b'\x01')

    def close(self):
        self.xbee.halt()
        self.serial.close()

    def print_query_response(self, name, packet):
        print("%s - %s" % (name, packet))