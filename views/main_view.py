import tkinter
from tkinter import ttk

class MainView():
    def __init__(self, window, xbee):
        self.xbee = xbee
        self.page = tkinter.Frame(window)
        self.query_button = tkinter.Button(self.page, text="Query XBee", command=self.xbee.query_parameters)
        self.parameters_list = ttk.Treeview(self.page)

        self.query_button.pack()
        self.parameters_list.pack()

    def add_parameter(self):
        self.parameters_list.insert("",0,"test")