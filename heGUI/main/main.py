from tkinter import filedialog as fd
from tkinter import *
from tkinter.ttk import *

window = Tk()



col_0 = 0
col_1 = 1
col_2 = 2
row = 0 


def select_file(entry: StringVar):
    filetypes = (
        ('PNG', '*.png'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    entry.set(filename)
    return

# Optical Image Entry
optical_image_label = Label(window, text = "Select optical image")
optical_image_label.grid(column=col_0, row=row)

optical_image_entryText = StringVar()
optical_image_entry = Entry(window, state='disabled', textvariable=optical_image_entryText)
optical_image_entry.grid(column=col_1, row=row)

optical_image_button = Button(window, text= "Select", command=lambda : select_file(optical_image_entryText))
optical_image_button.grid(column=col_2, row=row)
row = row + 1

# HE Image Entry
he_image_label = Label(window, text = "Select H&E image")
he_image_label.grid(column=col_0, row=row)

he_image_entryText = StringVar()
he_image_entry = Entry(window, state='disabled', textvariable=he_image_entryText)
he_image_entry.grid(column=col_1, row=row)

he_image_button = Button(window, text= "Select", command=lambda : select_file(he_image_entryText))
he_image_button.grid(column=col_2, row=row)

row = row + 1

# Separator
sep = Separator(window,orient=HORIZONTAL).grid(row=row, column=col_0,  columnspan=5, sticky='we')

row = row + 1


# FOV
fov_label = Label(window, text = "Select FOV")
fov_label.grid(column=col_0, row = row)

fov_combobox = Combobox(window, values=["400 \u03BCm", "800 \u03BCm"])
fov_combobox.grid(column=col_1, row = row, columnspan=2)

row = row + 1


# Slide num
slide_num_label = Label(window, text="Slide number")
slide_num_label.grid(column=col_0, row = row)

slide_num_entry = Entry(window)
slide_num_entry.grid(column=col_1, row = row, columnspan=2)

row = row + 1

# MIBI tracker ID
mibi_tracker_ID_label = Label(window, text="MIBI tracker ID")
mibi_tracker_ID_label.grid(column=col_0, row = row)

mibi_tracker_ID_entry = Entry(window)
mibi_tracker_ID_entry.grid(column=col_1, row = row, columnspan=2)

row = row + 1


# Separator
sep = Separator(window,orient=HORIZONTAL).grid(row=row, column=col_0,  columnspan=5, sticky='we')

row = row + 1

# Patient Order
patient_order_label = Label(window, text="Patient order in slide")
patient_order_label.grid(row = row, column=col_0, columnspan=3)

row = row + 1 

# Insert new patient
patient_order_name_label = Label(window, text="Name of patient")
patient_order_name_label.grid(column=col_0, row = row)

patient_order_entry = Entry(window)
patient_order_entry.grid(column=col_1, row=row)

patient_order_button = Button(window, text="Insert")
patient_order_button.grid(column=col_2, row=row)

row = row + 1

# Patient order tree view
patient_order_treeview = Treeview(window, columns=2)
patient_order_treeview.grid(column=col_0, columnspan=3)

patient_order_treeview.heading('#0', text='Order')
patient_order_treeview.heading('#1', text='Name')


window.mainloop()