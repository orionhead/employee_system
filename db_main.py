import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
import pymysql
import os
import shutil
import db_config


def on_tab_selected(event):
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "All Records":
        print("All records tab selected")
    if tab_text == "Add New Record":
        print("Add new record tab selected")


def load_database_results():
    global rows
    global num_of_rows
    try:
        con = pymysql.connect(host=db_config.DB_SERVER,
                              user=db_config.DB_USER,
                              password=db_config.DB_PASS,
                              database=db_config.DB)
        sql = "SELECT * FROM emoloyee_table"
        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        num_of_rows = cursor.rowcount
        con.close()
        has_loaded_successfully = True
        messagebox.showinfo("Connection to Database!", "Connected")
    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)
    return has_loaded_successfully


def database_error(err):
    messagebox.showinfo("Error", err)
    return False


def image_path(file_path):
    # open_image = Image.open(file_path)
    # image = ImageTk.PhotoImage(open_image)
    return ImageTk.PhotoImage(Image.open(file_path))


def load_photo_tab_one(file_path):
    image = image_path(file_path)
    imgLabelTabOne.configure(image=image)
    imgLabelTabOne.image = image


def scroll_data():
    fName.set(rows[row_counter][1])
    fam.set(rows[row_counter][2])
    job.set(rows[row_counter][3])

    try:
        ph_path = db_config.PHOTO_DIRECTORY + rows[row_counter][4]
        load_photo_tab_one(ph_path)
    except FileNotFoundError:
        load_photo_tab_one(db_config.PHOTO_DIRECTORY + file_name)


def scroll_forward():
    global row_counter
    global num_of_rows

    if row_counter >= (num_of_rows - 1):
        messagebox.showinfo("Database Error", "End of Database")
    else:
        row_counter = row_counter + 1
        scroll_data()


def scroll_back():
    global row_counter
    if row_counter is 0:
        messagebox.showinfo("Database Error", "Start of Database")
    else:
        row_counter = row_counter - 1
        scroll_data()


def select_image():
    global image_selected
    global image_file_name
    global file_new_home
    global file_to_copy

    path_to_image = filedialog.askopenfilename(initialdir="/",
                                               title="Open File",
                                               filetypes=(("PNGs", "*.png"), ("GIFs", "*.gifs"),
                                                          ("All Files", "*.*")))
    try:
        if path_to_image:
            image_file_name = os.path.basename(path_to_image)
            file_new_home = db_config.PHOTO_DIRECTORY + image_file_name
            file_to_copy = path_to_image
            image_selected = True
            load_photo_tab_two(file_to_copy)
    except IOError as err:
        image_selected = False
        messagebox.showinfo("File Error", err)


def load_photo_tab_two(file_path):
    image = image_path(file_path)
    imageLabelTabTwo.configure(image=image)
    imageLabelTabTwo.image = image


def add_new_record():
    global blank_text_boxes_tab_two
    global file_new_home
    global file_to_copy

file_name = "default.png"
path = db_config.PHOTO_DIRECTORY + file_name
rows = None
num_of_rows = None
row_counter = 0
image_selected = False
image_file_name = None
file_new_home = None
file_to_copy = None
blank_text_boxes_tab_two = None

form = tk.Tk()
form.title('Database Form')
form.geometry('500x280')

tab_parent = ttk.Notebook(form)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)

tab_parent.bind("<<NotebookTabChanged>>", on_tab_selected)

tab_parent.add(tab1, text='All Records')
tab_parent.add(tab2, text='Add New Record')

# Set up StringVars
fName = tk.StringVar()
fam = tk.StringVar()
job = tk.StringVar()

fNameTabTwo = tk.StringVar()
famTabTwo = tk.StringVar()
jobTabTwo = tk.StringVar()

# ADDING WIDGET TO TAB ONE
firstLabelTabOne = tk.Label(tab1,
                            text='First name:')  # whats in the bracket is tab1 because it has to be shown on the tab
# not the form
familyLabelTabOne = tk.Label(tab1, text='Family Name:')
jobLabelTabOne = tk.Label(tab1, text='Job Title')

firstEntryTabOne = tk.Entry(tab1, textvariable=fName)
familyEntryTabOne = tk.Entry(tab1, textvariable=fam)
jobEntryTabOne = tk.Entry(tab1, textvariable=job)

# openImageTabOne = Image.open(path)
# imgTabOne = ImageTk.PhotoImage(openImageTabOne)
imgTabOne = image_path(path)
imgLabelTabOne = tk.Label(tab1, image=imgTabOne)

buttonForward = tk.Button(tab1, text='Forward', command=scroll_forward)
buttonBack = tk.Button(tab1, text='Back', command=scroll_back)

####ADD WIDGET TO GRID
firstLabelTabOne.grid(row=0, column=0, padx=15, pady=15)
firstEntryTabOne.grid(row=0, column=1, padx=15, pady=15)

familyLabelTabOne.grid(row=1, column=0, padx=15, pady=15)
familyEntryTabOne.grid(row=1, column=1, padx=15, pady=15)

jobLabelTabOne.grid(row=2, column=0, padx=15, pady=15)
jobEntryTabOne.grid(row=2, column=1, padx=15, pady=15)

imgLabelTabOne.grid(row=0, column=2, rowspan=3, pady=15)

buttonBack.grid(row=3, column=0, padx=15, pady=15)
buttonForward.grid(row=3, column=2, padx=15, pady=15)

# ADDING WIDGETS FOR TAB
firstLabelTabTwo = tk.Label(tab2, text='FirstName')
familyLabelTabTwo = tk.Label(tab2, text='Family Name')
jobLabelTabTwo = tk.Label(tab2, text='Job Title')

firstEntryTabTwo = tk.Entry(tab2, textvariable=fNameTabTwo)
familyEntryTabTwo = tk.Entry(tab2, textvariable=famTabTwo)
jobEntryTabTwo = tk.Entry(tab2, textvariable=jobTabTwo)

# openImageTabTwo = Image.open(path)
# imgTabTwo = ImageTk.PhotoImage(openImageTabOne)
imageTabTwo = image_path(path)
imageLabelTabTwo = tk.Label(tab2, image=imageTabTwo)

buttonCommit = tk.Button(tab2, text='Add Record To Database')
buttonAddImage = tk.Button(tab2, text='Add Image', command=select_image)

# ADD WIDGET ON TAB TWO
firstLabelTabTwo.grid(row=0, column=0, padx=15, pady=15)
firstEntryTabTwo.grid(row=0, column=1, padx=15, pady=15)

familyLabelTabTwo.grid(row=1, column=0, padx=15, pady=15)
familyEntryTabTwo.grid(row=1, column=1, padx=15, pady=15)

jobLabelTabTwo.grid(row=2, column=0, padx=15, pady=15)
jobEntryTabTwo.grid(row=2, column=1, padx=15, pady=15)

buttonCommit.grid(row=4, column=1, padx=15, pady=15)
buttonAddImage.grid(row=4, column=2, padx=15, pady=15)

imageLabelTabTwo.grid(row=0, column=2, rowspan=3, padx=15, pady=15)

success = load_database_results()
if success:
    fName.set(rows[0][1])
    fam.set(rows[0][2])
    job.set(rows[0][3])
    photo_path = db_config.PHOTO_DIRECTORY + rows[0][4]
    load_photo_tab_one(photo_path)

tab_parent.pack(expand=1, fill='both')

form.mainloop()
