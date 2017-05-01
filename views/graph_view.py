import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

from matplotlib.figure import Figure
import matplotlib.pyplot
import matplotlib.animation

from controllers import graph
import numpy

import tkinter
from tkinter import ttk
from controllers import xbee
import sys

class GraphFrame(tkinter.Frame):
    def __init__(self, parent, xbee_controller):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.xbee_controller = xbee_controller

        fig, ax = matplotlib.pyplot.subplots()
        scope = graph.Scope(ax)

        # pass a generator in "emitter" to produce data for the update func
        ani = matplotlib.animation.FuncAnimation(fig, scope.update, self.emitter, interval=10,
                                      blit=True)
        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def emitter(self, probability=0.03):
        'return a random value with probability p, else 0'
        while True:
            yield 1.0
