import customtkinter, os
from tkinter import filedialog, scrolledtext, END, WORD, Text, Scrollbar, messagebox, Toplevel
from os import listdir
from os.path import isfile, join
from PIL import Image

current_index = 0

current_dir = os.curdir
desired_extension = ''
files = ''
popup = None
all_extensions = set() 


selected_images={}

current_image = customtkinter.CTkImage(light_image=Image.open("../../desktop/missing.jpg"), size=(256,256)) # WidthxHeight

app = customtkinter.CTk()    
app.title('Photo Picker')
app.geometry('650x650')
app.grid_columnconfigure((0, 1, 2), weight=1)


# ... (rest of your code)

# Declare checkbox_vars as a global variable
checkbox_vars = {}

# Function to apply the selected extensions and close the popup
def apply_and_close():
    global files, popup  # Declare popup as global

    if popup is None:  # Check if popup is valid
        return  # Or handle the error in a more user-friendly way

    selected_extensions = [ext for ext, var in checkbox_vars.items() if var.get() == "on"]
    files = [
        f
        for f in listdir(app.current_dir)
        if isfile(join(app.current_dir, f)) and
        os.path.splitext(f)[1][1:].lower() in selected_extensions and
        not f.startswith('.')
    ]
    files.sort()
    popup.destroy()
    update_displayed_image()

def select_directory():
    global current_dir, files, all_extensions, checkbox_vars, popup
    app.current_dir = filedialog.askdirectory(initialdir="/", title="Select Directory")
    current_dir = app.current_dir
    os.chdir(app.current_dir)

    # Get all file extensions in the directory, excluding empty extensions and handling case insensitivity
    all_extensions = {
        os.path.splitext(f)[1][1:].lower()
        for f in listdir(app.current_dir)
        if isfile(join(app.current_dir, f)) and os.path.splitext(f)[1]
    }

    if not all_extensions:
        messagebox.showwarning("No Extensions Found", "The selected directory contains no files with recognizable extensions.")
        return  # Or handle this case differently based on your requirements

    # Create the popup window
    global popup  # Declare popup as global within the function
    popup = Toplevel(app)
    popup.title("Select Extensions")

    # Create checkboxes for each extension
    checkbox_vars.clear()  # Clear the dictionary before populating it again
    for ext in all_extensions:
        var = customtkinter.StringVar(value="off") 
        checkbox = customtkinter.CTkCheckBox(popup, text=ext, variable=var, onvalue="on", offvalue="off")
        checkbox.pack(padx=20, pady=20)
        checkbox_vars[ext] = var

    # Create an Apply button
    apply_button = customtkinter.CTkButton(popup, text="Apply", command=apply_and_close)  # Remove the lambda
    apply_button.pack()
    
    print(current_dir)
    print("All extensions in the directory:", all_extensions)
    return current_dir

def show_popup():
    messagebox.showinfo("Popup Title", "This is the popup message!")

    # Create a button to trigger the popup (or call show_popup from elsewhere)
    popup_button = customtkinter.CTkButton(app, text="Show Popup", command=show_popup)
    popup_button.grid(row=7, column=2, padx=20, pady=20)  # Adjust row as needed

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

def load_selection():
    row = 0
    column = 0  # Start column at 0 for three columns

    for image_path in selected_images:  # Iterate over keys (image paths)
        try:
            image1 = customtkinter.CTkLabel(app, text="", image=customtkinter.CTkImage(light_image=Image.open(f"{current_dir}/{image_path}"), size=(200, 200)))  # Adjust size as needed
            image1.grid(row=row, column=column, padx=20, pady=20)

            column += 1
            if column == 3:  # Reset column to 0 after reaching 3
                column = 0
                row += 1
        except Exception as e:
            log_message(f"Error loading image {image_path}: {e}")

    done2_button = customtkinter.CTkButton(app, text="Done!")
    done2_button.grid(row=5, column=2, padx=20, pady=20)

    

def done1_button_callback():
    # Clear all widgets except the Done button
    for widget in app.winfo_children():
        widget.destroy()    
        load_selection()

# def done2_button_callback():
#     # Clear all widgets except the Done button
#     for widget in app.winfo_children():
#         widget.destroy()
    
#     global current_dir, files, all_extensions, checkbox_vars, popup

#     # Get all file extensions in the directory, excluding empty extensions and handling case insensitivity
#     all_extensions = {
#         os.path.splitext(f)[1][1:].lower()
#         for f in listdir(app.current_dir)
#         if isfile(join(app.current_dir, f)) and os.path.splitext(f)[1]
#     }

#     if not all_extensions:
#         messagebox.showwarning("No Extensions Found", "The selected directory contains no files with recognizable extensions.")
#         return  # Or handle this case differently based on your requirements

#     # Create the popup window
#     global popup  # Declare popup as global within the function
#     popup = Toplevel(app)
#     popup.title("Select Extensions")

#     # Create checkboxes for each extension
#     checkbox_vars.clear()  # Clear the dictionary before populating it again
#     for ext in all_extensions:
#         var = customtkinter.StringVar(value="off") 
#         checkbox = customtkinter.CTkCheckBox(popup, text=ext, variable=var, onvalue="on", offvalue="off")
#         checkbox.pack(padx=20, pady=20)
#         checkbox_vars[ext] = var

#     # Create an Apply button
#     apply_button = customtkinter.CTkButton(popup, text="Apply", command=apply_and_close)  # Remove the lambda
#     apply_button.pack()



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

done1_button = customtkinter.CTkButton(app, text="Done!", command=done1_button_callback)
done1_button.grid(row=5, column=3, padx=20, pady=20)


log_message("Application started")

app.mainloop()