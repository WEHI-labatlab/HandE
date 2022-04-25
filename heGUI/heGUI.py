"""
The purpose of this project is to create a user friendly way of transfering
annotations made on H&E slides in QuPath or CaseViewer onto the optical image
which will be used in the scanning in MIBI. 

@Author: Nina Tubau & Kenta Yokote
"""

from tkinter import filedialog as fd
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

import he_script

import os
import json

import napari
from skimage import io
import numpy as np

from skimage import img_as_ubyte
import napari.layers
from dotenv import load_dotenv
from he_script import get_fovs

class heGUI:

    def __init__(self, window):
        self.window = window
        self.treeview_row = 0

        col_0 = 0
        col_1 = 1
        col_2 = 2
        self.row = 0 

        self.message_box = Message(window)
        
        # File naming convention
        self.file_naming_convention_label = Label(window, text="File naming convention")
        self.file_naming_convention_label.grid(column=col_0, row = self.row)

        self.file_naming_convention_entry = Entry(window)
        self.file_naming_convention_entry.configure(background="white")
        self.file_naming_convention_entry.config(background="white")
        self.file_naming_convention_entry.grid(column=col_1, row = self.row, columnspan=2)

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

        # FOV
        self.fov_label = Label(window, text = "Select FOV")
        self.fov_label.grid(column=col_0, row = self.row)

        self.fov_combobox = Combobox(window, values=["400 \u03BCm", "800 \u03BCm"])
        self.fov_combobox.grid(column=col_1, row = self.row, columnspan=2)

        self.row = self.row + 1


        # Separator
        sep0 = Separator(window,orient=HORIZONTAL).grid(row=self.row, column=col_0,  columnspan=5, sticky='we')

        self.row = self.row + 1

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
        self.he_image_entryText.trace
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

        self.dat_file_button = Button(window, text= "Select", command=lambda : self.select_file(self.dat_file_entryText, "DAT"))
        self.dat_file_button.grid(column=col_2, row=self.row)

        self.row = self.row + 1

        # HE Image Entry
        self.output_label = Label(window, text = "Output folder")
        self.output_label.grid(column=col_0, row=self.row)

        self.output_entryText = StringVar()
        self.output_entry = Entry(window, state='disabled', textvariable=self.output_entryText)
        self.output_entry.grid(column=col_1, row=self.row)

        self.output_button = Button(window, text= "Select", command=lambda : self.select_folder(self.output_entryText))
        self.output_button.grid(column=col_2, row=self.row)

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


        # Run Napari
        self.napari_optical_button = Button(window, text = "Place landmarks on optical and H&E", width = 30, command=lambda : self.place_landmarks())
        self.napari_optical_button.grid(column = col_0, columnspan=3, row = self.row)

        self.row = self.row + 1

        self.napari_annotations_button = Button(window, text = "Check Annotations", width = 30, command=lambda : self.check_annotation())
        self.napari_annotations_button.grid(column=col_0, columnspan=3, row = self.row)

        self.row = self.row + 1

        self.fov_button = Button(window, text = "Check number of FOVS", width = 30, command=lambda : self.get_fovs())
        self.fov_button.grid(column=col_0, columnspan=3, row = self.row)
        self.row = self.row + 1

        sep5 = Separator(window,orient=HORIZONTAL).grid(row=self.row, column=col_0,  columnspan=5, sticky='we')
        self.row = self.row + 1

        
        self.generate_json_button = Button(window, text = "Save JSON", width = 30, command = lambda : self.save_json())
        self.generate_json_button.grid(column=col_0, columnspan=3, row = self.row)
        self.row = self.row + 1

        self.optical_placed = False
        self.he_placed = False
        self.checked = False
        self.options = None

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

    def select_file(self, entry: StringVar, filetype = "Image"):
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir=os.getcwd())
        entry.set(filename)
        return

    def select_folder(self, entry: StringVar):

        foldername = fd.askdirectory(title='Open a file',
            initialdir=os.getcwd())
        entry.set(foldername)
        return
    
    def place_landmarks(self):
        if len(self.optical_image_entry.get())==0:
            messagebox.showerror(title="Transformibi [source]", message="No optical image file selected")
            return
        if len(self.he_image_entry.get())==0:
            messagebox.showerror(title="Transformibi [target]", message="No H&E image file selected")
            return

        self.source_image = io.imread(self.optical_image_entry.get())
        self.target_image = io.imread(self.he_image_entry.get())
        self.target_image = he_script.resize_(self.source_image, self.target_image)
        
        self.source_viewer = napari.Viewer(title='Transformibi [source]')
        self.target_viewer = napari.Viewer(title='Transformibi [target]')
        self.source_viewer.add_image(self.source_image)
        self.target_viewer.add_image(self.target_image)
        #self.target_viewer.window.add_dock_widget(my_widget, area='right')
        #my_widget()
        self.target_points = self.target_viewer.add_points()
        self.source_points = self.source_viewer.add_points()
        napari.run()


        self.optical_placed = True
        self.he_placed = True
        
        return
    
    def check_annotation(self):
         ## SECOND STEP: PERFORM ALIGNMENT
        pts_ref = np.flip(self.target_points.data, axis=1)
        pts_mov = np.flip(self.source_points.data, axis=1)
        transformed_target = img_as_ubyte(he_script.align_images(self.target_image, pts_ref, pts_mov))

        i = len(self.patient_order_treeview.get_children())
            
        
        ## THIRD STEP: get coordinates from he annotations
        contours, binary_rect = he_script.get_annotation_coords(transformed_target)
        coord = he_script.get_corners(contours, i)

        #coord = coord[coord[:, 0].argsort()]
        pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
        unpad = lambda x: x[:, :-1]
        
        self.A, res, rank, s = he_script.transformation(pad(self.get_optical_coord()), pad(self.get_sed_coord()))

        ## FOURTH STEP: plot coordinates and adjust if needed

        self.test_viewer = napari.Viewer(title='Test coordinates')
        self.test_viewer.add_image(transformed_target, name='Transformed H&E')
        self.test_viewer.add_image(binary_rect, name='Annotations')
        self.test_viewer.add_image(self.source_image, name='MIBI optical image')
        self.test_points_min = self.test_viewer.add_points(coord[:, :2])
        self.test_points_max = self.test_viewer.add_points(coord[:, 2:])
        napari.run()

        self.checked = True


    def get_optical_coord(self):
        if (len(self.point_one_x_entry.get())==0 | len(self.point_one_y_entry.get())==0 |
            len(self.point_two_x_entry.get())==0 | len(self.point_one_y_entry.get())==0 |
            len(self.point_three_x_entry.get())==0 | len(self.point_one_y_entry.get())==0):
            messagebox.showerror(title="Optical coordinates", message="One or more of the optical coordinates are not filled")
            return
        
        return np.array([
                [int(self.point_one_x_entry.get()), int(self.point_one_y_entry.get())],
                [int(self.point_two_x_entry.get()), int(self.point_two_y_entry.get())], 
                [int(self.point_three_x_entry.get()), int(self.point_three_y_entry.get())]])

    def get_sed_coord(self):
        if (len(self.point_one_x_sed_entry.get())==0 | len(self.point_one_y_sed_entry.get())==0 |
            len(self.point_two_x_sed_entry.get())==0 | len(self.point_one_y_sed_entry.get())==0 |
            len(self.point_three_x_sed_entry.get())==0 | len(self.point_one_y_sed_entry.get())==0):
            messagebox.showerror(title="Optical coordinates", message="One or more of the optical coordinates are not filled")
            return
        
        return np.array([
                [int(self.point_one_x_sed_entry.get()), int(self.point_one_y_sed_entry.get())],
                [int(self.point_two_x_sed_entry.get()), int(self.point_two_y_sed_entry.get())], 
                [int(self.point_three_x_sed_entry.get()), int(self.point_three_y_sed_entry.get())]])



    def get_output_file_name(self):
        output_file = os.path.join(self.output_entry.get(), 
                    self.file_naming_convention_entry.get() + "_" + f"slide{self.slide_num_entry.get()}" + "_" + self.fov_combobox.get() + ".json"
        )
        return output_file

    def get_fovs(self):
        pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
        unpad = lambda x: x[:, :-1]
        if not self.checked:
            messagebox.showerror(title="Check FOVs", message="Annotation not checked")
            return
        if not self.he_placed:
            messagebox.showerror(title="Check FOVs", message="H&E landmarks not placed")
            return
        if not self.optical_placed:
            messagebox.showerror(title="Check FOVs", message="Optical landmarks not placed")
            return
        if len(self.output_entry.get()) == 0:
            messagebox.showerror(title="Check FOVs", message="No output folder selected")
            return 
        if len(self.file_naming_convention_entry.get()) == 0:
            messagebox.showerror(title="Check FOVs", message="No file naming convention provided")
            return 
        if len(self.fov_combobox.get()) == 0:
            messagebox.showerror(title="Check FOVs", message="No FOV selected")
            return 

        ## Concatenate coordinates and sort again in case it has been adjusted
        result = np.concatenate((self.test_points_min.data, self.test_points_max.data), axis=1)
        result = result[result[:, 0].argsort()]

        ## FITH STEP: Transform coordinates to the stage space
        transformed_FOV_min = pad(np.flip(result[:,:2], axis=1))@self.A
        transformed_FOV_max = pad(np.flip(result[:,2:], axis=1))@self.A

        ## SEVENTH STEP: SAVE JSON FILE WITH ALL THE FOVS
        if self.fov_combobox.get() == "400 \u03BCm":
            fov_size = 400
        else:
            fov_size = 800
        i=0
        patient_order = {}
        for child in self.patient_order_treeview.get_children():
            patient_order[i] = self.patient_order_treeview.item(child)['values'][0]
            i = i + 1

        FOV_grid = np.abs(transformed_FOV_max-transformed_FOV_min)//(fov_size*0.9)

        fname_login = self.dat_file_entry.get()
        load_dotenv(fname_login)

        email = os.getenv('MIBITRACKER_PUBLIC_EMAIL')
        password = os.getenv('MIBITRACKER_PUBLIC_PASSWORD')
        BACKEND_URL = os.getenv('MIBITRACKER_PUBLIC_URL')

        login_details = {"email": email, "password":password, "BACKEND_URL":BACKEND_URL}

        mibi_tracker_ID = int(self.mibi_tracker_ID_entry.get())

        try:
            patient_info = he_script.def_slide(mibi_tracker_ID, login_details, patient_order)
        except Exception as e:
            messagebox.showerror(title="Check FOVs", message=e.args)
            return
        
        final_x, final_y, self.options = get_fovs(transformed_FOV_min, patient_info, fov_size, FOV_grid)

        ## EIGTH STEP: PLOT THE COORDINATES OF ALL FOVS
        fovs_coord_optical = pad(np.concatenate((np.expand_dims(final_x, axis=1), np.expand_dims(final_y, axis=1)), axis=1))
        fovs_coord_sed = fovs_coord_optical@np.linalg.inv(self.A)
        fovs_coord_viewer = napari.Viewer(title='Testing')
        fovs_coord_viewer.add_image(self.source_image, name='MIBI optical image')
        fovs_coord_viewer.add_points(np.flip(fovs_coord_sed[:, :2], axis=1))
        napari.run()

        return 

    def save_json(self):
        if self.options == None:
            messagebox.showerror(title="Save JSON", message="FOVS not checked")
            return

        with open(self.get_output_file_name(), 'w') as f:
            json.dump(self.options.get_fov_list_dict(), f, indent=4)
        messagebox.showinfo(title="Save JSON", message="Saved")
        return

    


window = Tk()
window.winfo_toplevel().title("MIBI Json creator")
hegui = heGUI(window)
window.mainloop()