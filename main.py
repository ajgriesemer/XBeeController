import tkinter
from tkinter import ttk
from controllers import xbee

parameters_list = ttk.Treeview()


def main():
    xbee_controller = xbee.XBeeController()

    xbee_controller.subscribe(xbee.XBeeMessages.RXMessages.at_response, print_query_response)

    root = tkinter.Tk()
    root.title("XBee Controller")
    root.minsize(width=720, height=400)
    notebook = ttk.Notebook(root)

    page1 = tkinter.Frame(notebook)
    tkinter.Button(page1, text="Query XBee", command=xbee_controller.query_parameters).pack()
    # second page
    page2 = tkinter.Frame(notebook)

    notebook.add(page1, text='One')
    notebook.add(page2, text='Two')

    notebook.pack(expand=1, fill="both")

    root.mainloop()


def print_query_response(name, packet):
    print("%s - %s" % (name, packet))

if __name__ == '__main__':
    main()
