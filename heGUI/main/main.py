
from tkinter import Tk
from heGUI import heGUI


if __name__=="__main__":
    window = Tk()
    window.winfo_toplevel().title("MIBI Json creator")
    hegui = heGUI(window)
    window.mainloop()