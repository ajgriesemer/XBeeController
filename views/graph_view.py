import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot
import matplotlib.animation
import numpy
import tkinter
from controllers import xbee


class GraphFrame(tkinter.Frame):
    def __init__(self, parent, xbee_controller, max_t=2, delta_t = 0.1):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.xbee_controller = xbee_controller
        self.xbee_controller.subscribe(xbee.RXMessages.rx_io_data, self.callback)

        self.fig = matplotlib.pyplot.Figure(figsize=(8.5, 4.5), dpi=80, facecolor='w', edgecolor='k')
        self.fig.patch.set_alpha(0)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.get_tk_widget().grid(column=0, row=1)

        self.t_data = [0]
        self.y_data = [0]
        self.max_t = max_t
        self.delta_t = delta_t

        self.ax = self.fig.add_subplot(111)
        self.ax.patch.set_alpha(0)

        self.line, = self.ax.plot(self.t_data, self.y_data, 'r-')

    def callback(self, name, packet):
        i = 0
        adc = []
        while True:
            if 'adc-' + str(i) in packet['samples'][0]:
                adc.append(packet['samples'][0]['adc-' + str(i)])
                i = i + 1
            else:
                break

        if adc[0] is not None:
            last_t = self.t_data[-1] # Set last_t to the last value in the t_data array
            if last_t > (self.t_data[0] + self.max_t):
                self.t_data = self.t_data[1:]
                self.y_data = self.y_data[1:]
            self.t_data.append(self.t_data[-1] + self.delta_t)
            self.y_data.append(adc[0])
            self.line.set_xdata(self.t_data)
            self.line.set_ydata(self.y_data)
            self.ax.set_xlim(numpy.amin(self.t_data), numpy.amax(self.t_data))
            self.ax.set_ylim(numpy.amin(self.y_data)-1, numpy.amax(self.y_data)+1)
            self.fig.tight_layout()
            self.fig.canvas.draw()
        print("Graph %s - %s" % (name, packet))