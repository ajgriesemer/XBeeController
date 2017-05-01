from xbee import XBee
import serial

class XBeeController:

    """
    Initialize the XBeeController.
    This method is called implicitly when a new XBeeController is created
    """
    def __init__(self):
        # Iniitalize a new serial port communicating on block device /dev/ttyS0 (GPIO serial on the RPi 3)
        self.serial = serial.Serial('/dev/ttyS0', 9600)

        # Initialize an XBee object from the XBee library
        #   Pass the serial object to the XBee object
        #   Assign the dispatch method to be called when a new frame is received
        #   Configure the XBee library to escape characters to match the AP setting in the XBee
        self.xbee = XBee(self.serial, callback=self.dispatch, escaped=True)

        # Initialize an internal list to store all of the callback objects to be called when data is received
        self.callbacks = list()

    """
    This method is called when new data is received on the XBee
    @param packet: a parsed XBee API frame
    """
    def dispatch(self, packet):
        # Create a list of subscription objects that is a subset of the callbacks list
        #   All subscriptions in the subset should have a message field that matches the id of the received frame
        #   and a callback method
        subscriptions = [subscription for subscription in self.callbacks if subscription['message'] == packet['id'] and subscription['callback'] is not None]

        # Iterate through the subscription objects
        for subscription in subscriptions:
            # We need to handle bound methods different than regular functions
            # Bound methods will require an extra 'caller' value when they are subscribed
            # A regular function just needs the parameters we want to pass to the callback
            subscription['callback'](subscription['message'], packet)

    """
    Subscribe a function or bound method to a received XBee message
    @param message: The XBee message to subscribe to, from the class RXMessages
    @param callback: The function or method to call when the message is received
    @param caller: If the callback is a bound method pass the object to which it is bound
    """
    def subscribe(self, message, callback, caller=None):
        # Check that the same combination of message, callback and caller is not already in the callbacks list
        if {'message': message, 'callback': callback, 'caller': caller} not in self.callbacks: # TODO: Verify that this check works
            # Add a new subscription with the passed data
            self.callbacks.append({'message': message, 'callback': callback, 'caller': caller})

    """
    Remove a subscription 
    @param message: The XBee message subscribed to by the subscription
    @param callback: The function or method called when the message was received
    @param caller: The method to which the callback for the subscription was bound
    """
    def unsubscribe(self, message, callback, caller=None):
        # Create a list that is a subset of the callbacks list where message, callback and caller match
        subscriptions = [subscription for subscription in self.callbacks if subscription['message'] == message and subscription['callback'] == callback and subscription['caller'] == caller]

        # Iterate through the subset list which should only have one element
        for subscription in subscriptions:
            # Remove the subscription
            self.callbacks.remove(subscription)

    """
    Read basic configuration data from the connected XBee
    """
    def query_parameters(self):
        self.xbee.send('at', command=b'ID', frame_id=b'\x01')
        self.xbee.send('at', command=b'SH', frame_id=b'\x01')
        self.xbee.send('at', command=b'SL', frame_id=b'\x01')
        self.xbee.send('at', command=b'MY', frame_id=b'\x01')

    """
    Close the connection the XBee and free up the serial port
    """
    def close(self):
        self.xbee.halt()
        self.serial.close()

    def print_query_response(self, name, packet):
        print("XBee %s - %s" % (name, packet))

"""
RXMessages stores the possible API message frames that can be received from an XBee
"""
class RXMessages:
    rx = 'rx'
    rx_explicit = 'rx_explicit'
    rx_io_data_long_addr = 'rx_io_data_long_addr'
    rx_io_data = 'rx_io_data'
    tx_status = 'tx_status'
    status = 'status'
    at_response = 'at_response'
    remote_at_response = 'remote_at_response'
    node_id_indicator = 'node_id_indicator'
