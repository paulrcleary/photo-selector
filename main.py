from tkinter import filedialog
from tkinter import *
import customtkinter, os
from os import listdir
from os.path import isfile, join
from PIL import Image

image = "../../desktop/example-images/missing.jpg"

current_index = 0

files = ''

#app = Tk()
app = customtkinter.CTk()
app.title('Photo Picker')
app.geometry('650x500')

def select_directory():
    app.current_dir =  filedialog.askdirectory(initialdir = "/",title = "Select Directory")
    print (app.current_dir)
    os.chdir(app.current_dir)
    files = [f for f in listdir(app.current_dir) if isfile(join(app.current_dir, f))]
    files.sort()
    return files

def prev_button_callback():
    if files == '':
        print("please choose an image directory")

def next_button_callback():
    if files == '':
        print("please choose an image directory")


customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

directory_button = customtkinter.CTkButton(app, text="Choose Directory", command=select_directory)
directory_button.grid(row=0, column=2, padx=20, pady=20)

current_image = customtkinter.CTkImage(light_image=Image.open(image), size=(256,256)) # WidthxHeight

my_label = customtkinter.CTkLabel(app, text="", image=current_image)

my_label.grid(row=1, column=2, padx=20, pady=20)


prev_button = customtkinter.CTkButton(app, text="Previous Image", command=prev_button_callback)
prev_button.grid(row=3, column=1, padx=20, pady=20)

next_button = customtkinter.CTkButton(app, text="Next Image", command=next_button_callback)
next_button.grid(row=3, column=3, padx=20, pady=20)


app.mainloop()