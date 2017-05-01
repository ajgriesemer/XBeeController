import tkinter
from tkinter import ttk
from controllers import xbee

class MainFrame(tkinter.Frame):
    def __init__(self, parent, xbee_controller):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.xbee_controller = xbee_controller
        self.query_button = tkinter.Button(self, text="Query XBee", command=self.xbee_controller.query_parameters)
        self.xbee_controller.subscribe( xbee.RXMessages.at_response, self.add_parameter, self)
        self.parameters_list = ttk.Treeview(self, columns='Value')
        self.parameters_list.heading('#0', text='Parameter')
        self.parameters_list.heading('#1', text='Value')
        self.parameters_list.column('#0', stretch=tkinter.YES)
        self.parameters_list.column('#1', stretch=tkinter.YES)
        self.bind("<Map>", self.on_view_appearing)

        self.query_button.pack()
        self.parameters_list.pack()

    def add_parameter(self, name, packet):
        self.parameters_list.insert('','end',text=packet['command'].decode('utf-8'), values=(''.join('{:02x}'.format(x) for x in packet['parameter'])))
        print("Main %s - %s" % (name, packet))

    def on_view_appearing(self, event):
        print("Main Frame Opened %s", event)