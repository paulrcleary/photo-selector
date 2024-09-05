from tkinter import filedialog
from tkinter import *
import customtkinter, os
from os import listdir
from os.path import isfile, join
from PIL import Image

current_index = 0

current_dir = os.curdir
files = ''

current_image = customtkinter.CTkImage(light_image=Image.open("../../desktop/example-images/missing.jpg"), size=(256,256)) # WidthxHeight

app = customtkinter.CTk()    
app.title('Photo Picker')
app.geometry('650x500')
app.grid_columnconfigure((0, 1, 2), weight=1)


def select_directory():
    global current_dir, files
    app.current_dir =  filedialog.askdirectory(initialdir = "/",title = "Select Directory")
    current_dir = app.current_dir
    os.chdir(app.current_dir)
    files = [f for f in listdir(app.current_dir) if isfile(join(app.current_dir, f))]
    files.sort()
    print(current_dir, files, f'{current_dir}/{files[0]}')
    return current_dir, files

def prev_button_callback():
    global current_index # Update global index
    if files == '':
        print(files, current_dir)
        print("please choose an image directory")
    else:
        current_index = max(0, current_index - 1) # Ensure it doesn't go below 0
        update_displayed_image()

def next_button_callback():
    global current_index # Update global index
    if files == '':
        print(files, current_dir)
        print("please choose an image directory")
    else:
        current_index = min(len(files) - 1, current_index + 1) # Ensure it doesn't go beyond the list
        update_displayed_image()

def update_displayed_image():
    image_path = f"{current_dir}/{files[current_index]}"
    print(image_path)
    new_image = customtkinter.CTkImage(light_image=Image.open(image_path), size=(256,256))
    image.configure(image=new_image) # Update the displayed image



customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

directory_button = customtkinter.CTkButton(app, text="Choose Directory", command=select_directory)
directory_button.grid(row=0, column=2, padx=20, pady=20)

image = customtkinter.CTkLabel(app, text="", image=current_image)

image.grid(row=1, column=2, padx=20, pady=20)


prev_button = customtkinter.CTkButton(app, text="Previous Image", command=prev_button_callback)
prev_button.grid(row=3, column=1, padx=20, pady=20)

next_button = customtkinter.CTkButton(app, text="Next Image", command=next_button_callback)
next_button.grid(row=3, column=3, padx=20, pady=20)

entry = customtkinter.CTkEntry(app, placeholder_text="CTkEntry")
entry.grid(row=4, column=3, padx=20, pady=20)


app.mainloop()