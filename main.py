import tkinter
from tkinter import ttk
from controllers import xbee
from views import main_view, graph_view

def main():
    root = tkinter.Tk()
    root.wm_title("XBee Controller")
    root.minsize(width=720, height=400)

    xbee_controller = xbee.XBeeController()

    notebook = ttk.Notebook(root)

    main_frame = main_view.MainFrame(notebook, xbee_controller=xbee_controller)
    graph_frame = graph_view.GraphFrame(notebook, xbee_controller=xbee_controller)


    notebook.add(main_frame, text='Main')
    notebook.add(graph_frame, text='Two')

    notebook.pack(expand=1, fill="both")

    root.mainloop()
    root.destroy()


def main_print(name, packet):
    print("%s - %s" % (name, packet))


if __name__ == '__main__':
    main()
