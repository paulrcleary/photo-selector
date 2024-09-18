import customtkinter, os
from tkinter import filedialog, messagebox
from PIL import Image
from os import listdir, chdir
from os.path import isfile, join

# --- Global Constants ---
PLACEHOLDER_IMAGE_PATH = "assets/missing.jpg"  # Path to the placeholder image

class ImageSelectionFrame(customtkinter.CTkFrame):
    """
    Frame for displaying and selecting images.
    """
    

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.current_index = 0  # Initialize current_index here

        self.grid_columnconfigure((0, 1, 2), weight=1)

        # --- Directory Selection Button ---
        self.directory_button = customtkinter.CTkButton(self, text="Choose Directory",
                                                        command=self.select_directory)
        self.directory_button.grid(row=0, column=2, padx=20, pady=20)

        # --- Image Display ---
        try:
            self.placeholder_image = customtkinter.CTkImage(light_image=Image.open(PLACEHOLDER_IMAGE_PATH),
                                                            size=(256, 256))
        except FileNotFoundError:
            print(f"Warning: '{PLACEHOLDER_IMAGE_PATH}' not found. Using a blank label.")
            self.placeholder_image = None

        self.current_image_label = customtkinter.CTkLabel(self, text="", image=self.placeholder_image)
        self.current_image_label.grid(row=1, column=2, padx=20, pady=20)

        # --- Navigation Buttons ---
        self.prev_button = customtkinter.CTkButton(self, text="Previous Image", command=self.prev_button_callback)
        self.prev_button.grid(row=3, column=1, padx=20, pady=20)

        self.next_button = customtkinter.CTkButton(self, text="Next Image", command=self.next_button_callback)
        self.next_button.grid(row=3, column=3, padx=20, pady=20)

        # --- Selection Checkbox ---
        self.check_var = customtkinter.StringVar(value="off")
        self.checkbox = customtkinter.CTkCheckBox(
            self, text="Selected", command=self.checkbox_event, variable=self.check_var, onvalue="on", offvalue="off"
        )
        self.checkbox.grid(row=3, column=2, padx=20, pady=20)

    # --- Navigation and Selection Callbacks ---
    def prev_button_callback(self, event=None):
        """Handles moving to the previous image."""
        if self.parent.files:
            self.current_index = max(0, self.current_index - 1)  # Access directly
            self.update_image_and_checkbox()
        else:
            self.parent.log_message("Please select a directory first.")

    def next_button_callback(self, event=None):
        """Handles moving to the next image."""
        if self.parent.files:
            self.current_index = (self.current_index + 1) % len(self.parent.files)  # Access directly
            self.update_image_and_checkbox()
        else:
            self.parent.log_message("Please select a directory first.")

    def update_image_and_checkbox(self):
        """Updates the displayed image and checkbox state."""
        if self.parent.files:
            self.update_displayed_image()
            self.update_checkbox_state()
        else:
            self.current_image_label.configure(image=self.placeholder_image)
            self.parent.log_message("Please select a directory first.")

    def update_displayed_image(self):
        """Updates the displayed image based on the current index."""
        image_path = f"{self.parent.current_dir}/{self.parent.files[self.current_index]}"  # Access directly
        try:
            new_image = customtkinter.CTkImage(light_image=Image.open(image_path), size=(256, 256))
            self.current_image_label.configure(image=new_image)
        except Exception as e:
            self.parent.log_message(f"Error loading image {image_path}: {e}")

    def update_checkbox_state(self):
        """Updates the checkbox state based on whether the image is selected."""
        if self.parent.files[self.current_index] in self.parent.selected_images:
            self.check_var.set("on")
        else:
            self.check_var.set("off")

    def checkbox_event(self):
        """Handles checkbox state changes, updating the selected images dictionary."""
        if self.parent.files:
            current_image_path = self.parent.files[self.current_index]
            if self.check_var.get() == "on":
                print(current_image_path)
                self.parent.selected_images[current_image_path] = True  # Add to dictionary
                self.parent.log_message(f"Selected {current_image_path}")
            else:
                if current_image_path in self.parent.selected_images:
                    self.parent.selected_images.pop(current_image_path)  # Remove from dictionary
                    self.parent.log_message(f"Deselected {current_image_path}")
        else:
            self.parent.log_message("Please select a directory first.")
            self.check_var.set("off") 
            
    def toggle_checkbox(self, event=None):
        """Toggles the state of the selection checkbox."""
        if self.check_var.get() == "on":
            self.check_var.set("off")
        else:
            self.check_var.set("on")
        self.checkbox_event()  # Trigger the checkbox event to handle selection logic

    def select_directory(self):
        """Opens a directory selection dialog and updates the current directory."""
        selected_dir = filedialog.askdirectory(initialdir="/", title="Select Directory")
        if selected_dir:  # Check if a directory was actually selected
            chdir(selected_dir)
            self.parent.current_dir = selected_dir
            print(selected_dir)
            self.load_files_from_directory()

    def load_files_from_directory(self):
        """
        Loads image files from the selected directory, filtering by extension.
        Displays a popup to let the user choose which extensions to include.
        """
        all_extensions = self.get_unique_file_extensions()

        if not all_extensions:
            messagebox.showwarning("No Extensions Found",
                                "The selected directory contains no files with recognizable extensions.")
            return

        self.show_extension_popup(all_extensions)

    def get_unique_file_extensions(self):
        """Returns a set of unique file extensions in the current directory."""
        return {
            os.path.splitext(f)[1][1:].lower()
            for f in listdir(self.parent.current_dir)
            if isfile(join(self.parent.current_dir, f)) and os.path.splitext(f)[1]
        }

    def show_extension_popup(self, all_extensions):
        """
        Displays a popup window to let the user select desired file extensions.
        """
        popup = customtkinter.CTkToplevel(self)
        popup.title("Select Extensions")

        checkbox_vars = {}  # Store checkbox variables to retrieve selections
        for ext in all_extensions:
            var = customtkinter.StringVar(value="off")  # Variable to hold checkbox state
            checkbox = customtkinter.CTkCheckBox(popup, text=ext, variable=var, onvalue="on", offvalue="off")
            checkbox.pack(padx=20, pady=20)
            checkbox_vars[ext] = var

        def apply_extensions():
            """
            Callback for the "Apply" button in the extension selection popup.
            Filters files based on selected extensions and updates the displayed image.
            """
            selected_extensions = [ext for ext, var in checkbox_vars.items() if var.get() == "on"]
            self.parent.files = [
                f
                for f in listdir(self.parent.current_dir)
                if isfile(join(self.parent.current_dir, f)) and
                os.path.splitext(f)[1][1:].lower() in selected_extensions and
                not f.startswith('.')  # Exclude hidden files
            ]
            self.parent.files.sort()  # Sort files for consistent order
            popup.destroy()  # Close the popup
            self.update_image_and_checkbox()

        apply_button = customtkinter.CTkButton(popup, text="Apply", command=apply_extensions)
        apply_button.pack()

