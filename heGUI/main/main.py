from tkinter import filedialog as fd
from tkinter import *
from tkinter.ttk import *



class heGUI:

    def __init__(self, window):
        self.window = window
        self.treeview_row = 0



        col_0 = 0
        col_1 = 1
        col_2 = 2
        self.row = 0 

        # Optical Image Entry
        self.optical_image_label = Label(window, text = "Select optical image")
        self.optical_image_label.grid(column=col_0, row=self.row)

        self.optical_image_entryText = StringVar()
        self.optical_image_entry = Entry(window, state='disabled', textvariable=self.optical_image_entryText)
        self.optical_image_entry.grid(column=col_1, row=self.row)

        self.optical_image_button = Button(window, text= "Select", command=lambda : self.select_file(self.optical_image_entryText))
        self.optical_image_button.grid(column=col_2, row=self.row)
        self.row = self.row + 1

        # HE Image Entry
        self.he_image_label = Label(window, text = "Select H&E image")
        self.he_image_label.grid(column=col_0, row=self.row)

        self.he_image_entryText = StringVar()
        self.he_image_entry = Entry(window, state='disabled', textvariable=self.he_image_entryText)
        self.he_image_entry.grid(column=col_1, row=self.row)

        self.he_image_button = Button(window, text= "Select", command=lambda : self.select_file(self.he_image_entryText))
        self.he_image_button.grid(column=col_2, row=self.row)

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

        # Separator
        sep = Separator(window,orient=HORIZONTAL).grid(row=self.row, column=col_0,  columnspan=5, sticky='we')

        self.row = self.row + 1


        # FOV
        self.fov_label = Label(window, text = "Select FOV")
        self.fov_label.grid(column=col_0, row = self.row)

        self.fov_combobox = Combobox(window, values=["400 \u03BCm", "800 \u03BCm"])
        self.fov_combobox.grid(column=col_1, row = self.row, columnspan=2)

        self.row = self.row + 1


        # Slide num
        self.slide_num_label = Label(window, text="Slide number")
        self.slide_num_label.grid(column=col_0, row = self.row)

        self.slide_num_entry = Entry(window)
        self.slide_num_entry.grid(column=col_1, row = self.row, columnspan=2)

        self.row = self.row + 1

        # MIBI tracker ID
        self.mibi_tracker_ID_label = Label(window, text="MIBI tracker ID")
        self.mibi_tracker_ID_label.grid(column=col_0, row = self.row)

        self.mibi_tracker_ID_entry = Entry(window)
        self.mibi_tracker_ID_entry.grid(column=col_1, row = self.row, columnspan=2)

        self.row = self.row + 1


        # Separator
        sep = Separator(window,orient=HORIZONTAL).grid(row=self.row, column=col_0,  columnspan=5, sticky='we')

        self.row = self.row + 1

        # Patient Order
        self.patient_order_label = Label(window, text="Patient order in slide")
        self.patient_order_label.grid(row = self.row, column=col_0, columnspan=3)

        self.row = self.row + 1 

        # Insert new patient
        self.patient_order_name_label = Label(window, text="Name of patient")
        self.patient_order_name_label.grid(column=col_0, row = self.row)

        self.patient_order_entry = Entry(window)
        self.patient_order_entry.grid(column=col_1, row=self.row)

        self.patient_order_button = Button(window, text="Insert", command = lambda : self.insert_row())
        self.patient_order_button.grid(column=col_2, row=self.row)

        self.row = self.row + 1

        # Patient order tree view
        self.patient_order_treeview = Treeview(window, columns=2)
        self.patient_order_treeview.grid(column=col_0, columnspan=3)

        self.patient_order_treeview.heading('#0', text='Order')
        self.patient_order_treeview.heading('#1', text='Name')

        self.row = self.row + 1
        
        self.patient_order_remove_button = Button(window, text="Remove selected row", command = lambda : self.remove_item())
        self.patient_order_remove_button.grid(column=col_0, row=self.row, columnspan=3)
        self.row = self.row + 1


        # Separator
        sep3 = Separator(window,orient=HORIZONTAL).grid(row=self.row, column=col_0,  columnspan=5, sticky='we')
        self.row = self.row + 1

        # Coordinates Frame
        frame = Frame(window)
        frame.grid(column=0, row= self.row, columnspan=3)
        # frame.pack(pady=20)

        
        self.optical_coor_entry = Label(frame, text="Optical Coordinates (x,y)")
        self.optical_coor_entry.grid(column=2, row=self.row, columnspan=2)

        self.sed_entry = Label(frame, text="SED Coordinates (x,y)")
        self.sed_entry.grid(column=5, row=self.row, columnspan=2)

        self.row = self.row + 1

        # self.point_separator = Separator(frame,orient='vertical')
        # self.point_separator.grid(column=1, row=self.row, rowspan=3, sticky='ns')

        self.point_separator_2 = Separator(frame,orient='vertical')
        self.point_separator_2.grid(column=4, row=self.row, rowspan=3, sticky='ns')


        self.point_one_label = Label(frame, text="Point 1")
        self.point_one_label.grid(column=0, row=self.row)

        self.point_one_x_entry = Entry(frame, width = 7)
        self.point_one_x_entry.grid(column=2, row=self.row)

        self.point_one_y_entry = Entry(frame, width = 7)
        self.point_one_y_entry.grid(column=3, row=self.row)

        self.point_one_x_sed_entry = Entry(frame, width = 7)
        self.point_one_x_sed_entry.grid(column=5, row=self.row)

        self.point_one_y_sed_entry = Entry(frame, width = 7)
        self.point_one_y_sed_entry.grid(column=6, row=self.row)


        self.row = self.row + 1

        self.point_two_label = Label(frame, text="Point 2")
        self.point_two_label.grid(column=0, row=self.row)
        self.point_two_x_entry = Entry(frame, width = 7)
        self.point_two_x_entry.grid(column=2, row=self.row)

        self.point_two_y_entry = Entry(frame, width = 7)
        self.point_two_y_entry.grid(column=3, row=self.row)

        self.point_two_x_sed_entry = Entry(frame, width = 7)
        self.point_two_x_sed_entry.grid(column=5, row=self.row)

        self.point_two_y_sed_entry = Entry(frame, width = 7)
        self.point_two_y_sed_entry.grid(column=6, row=self.row)
        self.row = self.row + 1

        self.point_three_label = Label(frame, text="Point 3")
        self.point_three_label.grid(column=0, row=self.row)
        self.point_three_x_entry = Entry(frame, width = 7)
        self.point_three_x_entry.grid(column=2, row=self.row)

        self.point_three_y_entry = Entry(frame, width = 7)
        self.point_three_y_entry.grid(column=3, row=self.row)

        self.point_three_x_sed_entry = Entry(frame, width = 7)
        self.point_three_x_sed_entry.grid(column=5, row=self.row)

        self.point_three_y_sed_entry = Entry(frame, width = 7)
        self.point_three_y_sed_entry.grid(column=6, row=self.row)
        self.row = self.row + 1

        # Separator
        sep4 = Separator(window,orient=HORIZONTAL).grid(row=self.row, column=col_0,  columnspan=5, sticky='we')
        self.row = self.row + 1


    def insert_row(self):
        self.patient_order_treeview.insert("", END, text=self.treeview_row, values= (self.patient_order_entry.get()))
        self.treeview_row = self.treeview_row + 1


    def remove_item(self):
        selected_items = self.patient_order_treeview.selection()        
        for selected_item in selected_items:          
            self.patient_order_treeview.delete(selected_item)
        
        i=0
        for child in self.patient_order_treeview.get_children():
            self.patient_order_treeview.item(child, text=i, values=self.patient_order_treeview.item(child)['values'])
            i = i + 1
        
        self.treeview_row = self.treeview_row - 1

    def select_file(self, entry: StringVar):
        filetypes = (
            ('PNG', '*.png'),
            ('JPEG', '*.jpg'),
            ('TIFF', '*.tif'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        entry.set(filename)
        return


window = Tk()
window.winfo_toplevel().title("MIBI Json creator")
hegui = heGUI(window)
window.mainloop()