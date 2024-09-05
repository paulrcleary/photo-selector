import customtkinter, os
from tkinter import filedialog, scrolledtext, END, WORD, Text, Scrollbar
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
app.geometry('650x650')
app.grid_columnconfigure((0, 1, 2), weight=1)


def select_directory():
    global current_dir, files, current_index # Update global variables
    app.current_dir =  filedialog.askdirectory(initialdir = "/",title = "Select Directory")
    current_dir = app.current_dir
    os.chdir(app.current_dir)
    files = [f for f in listdir(app.current_dir) if isfile(join(app.current_dir, f))]
    files.sort()
    log_message(f"Setting active directory to {current_dir}")
    # print(current_dir, files, f'{current_dir}/{files[0]}')

    current_index = max(0, current_index - 1) # Ensure it doesn't go below 0

    update_displayed_image()

    return current_dir, files

def prev_button_callback(event=None):
    global current_index # Update global index
    if files == '':
        log_message("Please select a directory first.")
    else:
        current_index = max(0, current_index - 1) # Ensure it doesn't go below 0
        check_var.set("off")  # Reset checkbox when changing image
        update_displayed_image()

def next_button_callback(event=None):
    global current_index # Update global index
    if files == '':
        log_message("Please select a directory first.")
    else:
        current_index = (current_index + 1) % len(files) # Ensure it doesn't go beyond the list
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
        log_message("Please select a directory first.")
        check_var.set("off")  # Use .set() to change the checkbox state
    else:
        # Add/remove the current image from selected_images based on checkbox state
        current_image_path = files[current_index]
        if check_var.get() == "on":
            selected_images[current_image_path] = True  # Add to dictionary
            log_message(f"Selected {files[current_index]}")

        else:
            selected_images.pop(current_image_path, None)  # Remove if present
            log_message(f"Deselected {files[current_index]}")


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
        log_message(f"Selected {files[current_index]}")
    else:
        selected_images.pop(current_image_path, None)
        log_message(f"Deselected {files[current_index]}")

def done_button():
    pass


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

# Create a ScrolledText widget for the log window
log_window = scrolledtext.ScrolledText(app, wrap=WORD, height=5) 
log_window.grid(row=4, column=1, columnspan=3, padx=20, pady=20, sticky="nsew")

scrollbar = log_window.vbar 
scrollbar.config(width=0)  # Correct option: state (without hyphen)

# Function to add messages to the log window
def log_message(message):
    log_window.insert(END, message + "\n")
    log_window.see(END)  # Scroll to the bottom to see the latest message

log_text = Text(app, wrap=WORD, height=5)
log_scrollbar = Scrollbar(app, command=log_text.yview,
                         background="lightgray",  # Scrollbar trough color
                         activebackground="gray",   # Active background color
                         troughcolor="white")       # Trough color

log_text.config(yscrollcommand=log_scrollbar.set)

done_button = customtkinter.CTkButton(app, text="Done!", command=done_button)
done_button.grid(row=5, column=3, padx=20, pady=20)


log_message("Application started")

app.mainloop()