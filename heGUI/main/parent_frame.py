from tkinter import filedialog as fd
from tkinter import *
from tkinter.ttk import *

class MainWindow():


    def __init__(self, window):
        
        col_0 = 0
        col_1 = 1
        col_2 = 2
        col_3 = 3 

        self.row = 0

        self.file_naming_convention_label = Label(window, text = "File naming convention")
        self.file_naming_convention_label.grid(column=col_0, row = self.row)

        self.file_naming_convention_entry = Entry(window)
        self.file_naming_convention_entry.grid(column=col_1, row = self.row)

        self.row = self.row + 1

        # Dat file
        self.dat_file_label = Label(window, text = "Select DAT file")
        self.dat_file_label.grid(column=col_0, row=self.row)

        self.dat_file_entryText = StringVar()
        self.dat_file_entry = Entry(window, state='disabled', textvariable=self.dat_file_entryText)
        self.dat_file_entry.grid(column=col_1, row=self.row)

        self.dat_file_button = Button(window, text= "Select", command=lambda : self.select_file(self.dat_file_entryText))
        self.dat_file_button.grid(column=col_2, row=self.row)

        self.row = self.row + 1

        self.vert_separator = Separator(window,orient=VERTICAL).grid(row=self.row, column=col_1,  rowspan=5, sticky='we')




window = Tk()
window.winfo_toplevel().title("MIBI Json creator")
hegui = MainWindow(window)
window.mainloop()