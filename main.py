import tkinter
from tkinter import ttk
from controllers import xbee
from views import main_view

def main():
    root = tkinter.Tk()
    root.wm_title("XBee Controller")
    root.minsize(width=720, height=400)

    xbee_controller = xbee.XBeeController()

    notebook = ttk.Notebook(root)

    main_frame = main_view.MainFrame(notebook, xbee_controller=xbee_controller)

    # second page
    page2 = tkinter.Frame(notebook)

    notebook.add(main_frame, text='Main')
    notebook.add(page2, text='Two')

    notebook.pack(expand=1, fill="both")

    root.mainloop()
    root.destroy()


def main_print(name, packet):
    print("%s - %s" % (name, packet))


if __name__ == '__main__':
    main()
