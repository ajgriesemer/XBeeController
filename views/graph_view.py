import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

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

        fig = matplotlib.pyplot.Figure()

        x = numpy.arange(0, 2 * numpy.pi, 0.01)  # x-array

        def animate(i):
            line.set_ydata(numpy.sin(x + i / 10.0))  # update the data
            return line,

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(column=0, row=1)

        ax = fig.add_subplot(111)
        line, = ax.plot(x, numpy.sin(x))
        ani = matplotlib.animation.FuncAnimation(fig, animate, numpy.arange(1, 200), blit=False)
