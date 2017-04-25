import tkinter
from tkinter import ttk

def main():
    root = tkinter.Tk()
    root.title("XBee Controller")
    root.minsize(width=720, height=400)
    notebook = ttk.Notebook(root)

    # adding Frames as pages for the ttk.Notebook
    # first page, which would get widgets gridded into it
    page1 = tkinter.Frame(notebook)

    ttk.Treeview(page1)

    # second page
    page2 = tkinter.Frame(notebook)

    notebook.add(page1, text='One')
    notebook.add(page2, text='Two')

    notebook.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == '__main__':
    main()
