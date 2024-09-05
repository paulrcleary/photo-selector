from tkinter import filedialog, scrolledtext, END, WORD, Text, Scrollbar
from tkinter import *
import customtkinter, os
from os import listdir
from os.path import isfile, join
from PIL import Image

current_index = 0

current_dir = os.curdir
files = ''

selected_images={}

current_image = customtkinter.CTkImage(light_image=Image.open("../../desktop/missing.jpg"), size=(256,256)) # WidthxHeight

app = customtkinter.CTk()    
app.title('Photo Picker')
app.geometry('650x550')
app.grid_columnconfigure((0, 1, 2), weight=1)


def select_directory():
    global current_dir, files, current_index # Update global variables
    app.current_dir =  filedialog.askdirectory(initialdir = "/",title = "Select Directory")
    current_dir = app.current_dir
    os.chdir(app.current_dir)
    files = [f for f in listdir(app.current_dir) if isfile(join(app.current_dir, f))]
    files.sort()
    print(f"Setting active directory to {current_dir}")
    # print(current_dir, files, f'{current_dir}/{files[0]}')

    current_index = max(0, current_index - 1) # Ensure it doesn't go below 0

    update_displayed_image()

    return current_dir, files

def prev_button_callback(event=None):
    global current_index # Update global index
    if files == '':
        print("Please select a directory first.")
    else:
        current_index = max(0, current_index - 1) # Ensure it doesn't go below 0
        check_var.set("off")  # Reset checkbox when changing image
        update_displayed_image()

def next_button_callback(event=None):
    global current_index # Update global index
    if files == '':
        print("Please select a directory first.")
    else:
        current_index = min(len(files) - 1, current_index + 1) # Ensure it doesn't go beyond the list
        check_var.set("off")  # Reset checkbox when changing image
        update_displayed_image()

def update_displayed_image():
    image_path = f"{current_dir}/{files[current_index]}"
    print(image_path)
    new_image = customtkinter.CTkImage(light_image=Image.open(image_path), size=(256,256))
    image.configure(image=new_image) # Update the displayed image

    # Set checkbox state based on selected_images
    if files[current_index] in selected_images:
        check_var.set("on")
    else:
        check_var.set("off") 

def checkbox_event():
    global check_var  # Declare check_var as global to modify it

    if files == '':
        print("Please select a directory first.")
        check_var.set("off")  # Use .set() to change the checkbox state
    else:
        # Add/remove the current image from selected_images based on checkbox state
        current_image_path = files[current_index]
        if check_var.get() == "on":
            selected_images[current_image_path] = True  # Add to dictionary
            print(f"Selected {files[current_index]}")

        else:
            selected_images.pop(current_image_path, None)  # Remove if present
            print(f"Deselected {files[current_index]}")


    print(selected_images)

def toggle_checkbox(event=None):
    global check_var

    # Toggle the checkbox state
    if check_var.get() == "on":
        check_var.set("off")
    else:
        check_var.set("on")

    # Update selected_images based on the new checkbox state
    current_image_path = files[current_index] 
    if check_var.get() == "on":
        selected_images[current_image_path] = True
        print(f"Selected {files[current_index]}")
    else:
        selected_images.pop(current_image_path, None)
        print(f"Deselected {files[current_index]}")


# Keyboard shortcuts
app.bind("<Left>", prev_button_callback)
app.bind("<Right>", next_button_callback)
app.bind("<space>", toggle_checkbox)


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


check_var = customtkinter.StringVar(value="off")
checkbox = customtkinter.CTkCheckBox(app, text="Selected", command=checkbox_event, variable=check_var, onvalue="on", offvalue="off")  # Use "on" and "off" as values
checkbox.grid(row=3, column=2, padx=20, pady=20)


app.mainloop()