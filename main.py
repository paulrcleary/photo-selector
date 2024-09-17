import customtkinter, os
from tkinter import filedialog, scrolledtext, END, WORD, messagebox
from os import listdir
from os.path import isfile, join
from PIL import Image
from frames.instructions_frame import InstructionsFrame
from frames.image_selection_frame import ImageSelectionFrame
from frames.selected_images_frame import SelectedImagesFrame

# --- Global Constants ---
PLACEHOLDER_IMAGE_PATH = "assets/missing.jpg"  # Path to the placeholder image

class App(customtkinter.CTk):
    """
    Main application class.
    Manages frames, navigation, and global state.
    """

    def __init__(self):
        super().__init__()

        self.title('Photo Picker')
        self.geometry('650x650')
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # --- Initialize Application State ---
        self.current_dir = os.curdir  # Start in the current working directory
        self.files = []  # List to store the filtered image files
        self.selected_images = {}  # Dictionary to store selected image paths (key = path, value = True)
        self.current_index = 0  # Index of the currently displayed image

        # --- Frame Management ---
        self.frames = []  # List to hold all the frames of the application
        self.current_frame_index = 0  # Index of the currently active frame

        # --- Grid Configuration ---
        self.grid_rowconfigure(0, weight=1)  # Make the first row (frame row) expand
        self.grid_rowconfigure(1, weight=0)  # Second row (button row) doesn't expand
        self.grid_rowconfigure(2, weight=0)  # Third row (log window) doesn't expand
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # 1. Instructions Frame
        self.frames.append(InstructionsFrame(self))

        # 2. Image Selection Frame
        self.frames.append(ImageSelectionFrame(self, 1))  # Pass index 1

        # 3. Selected Images Frame
        self.frames.append(SelectedImagesFrame(self))

        # Add more frames here (e.g., for filtering, editing, etc.)
        #    self.frames.append(YourFrameClass(self)) 

        # Place the first frame
        self.frames[0].grid(row=0, column=0, sticky="nsew")

        # --- Keyboard Shortcuts ---
        self.bind("<Left>", self.handle_left_key)
        self.bind("<Right>", self.handle_right_key)
        self.bind("<space>", self.handle_space_key)

        # Display the initial frame
        self.show_current_frame()

        # --- Next Frame Button (created in App class) ---
        self.next_frame_button = customtkinter.CTkButton(self, text="Next", command=self.show_selected_images_frame)
        self.next_frame_button.grid(row=1, column=0, columnspan=3, pady=(20, 20), sticky="e", padx=(20, 20))

        # --- Log Window ---
        self.log_window = scrolledtext.ScrolledText(self, wrap=WORD, height=5)
        self.log_window.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

    # --- Keyboard Shortcut Handlers ---
    def handle_left_key(self, event=None):
        """Handles left arrow key press for navigation."""
        if isinstance(self.frames[self.current_frame_index], ImageSelectionFrame):
            self.frames[self.current_frame_index].prev_button_callback()

    def handle_right_key(self, event=None):
        """Handles right arrow key press for navigation."""
        if isinstance(self.frames[self.current_frame_index], ImageSelectionFrame):
            self.frames[self.current_frame_index].next_button_callback()

    def handle_space_key(self, event=None):
        """Handles spacebar key press for image selection."""
        if isinstance(self.frames[self.current_frame_index], ImageSelectionFrame):
            self.frames[self.current_frame_index].toggle_checkbox()

    # --- Frame Navigation Methods ---
    def show_current_frame(self):
        """Brings the current frame to the front."""
        frame = self.frames[self.current_frame_index]
        frame.tkraise()
        print("Showing frame:", frame)

    def go_to_next_frame(self):
        """
        Navigates to the next frame in the application.
        If moving to the Selected Images Frame, it triggers the loading of selected images.
        """
        # Allow moving to the next frame regardless of the current frame type
        if self.current_frame_index < len(self.frames) - 1:
            self.current_frame_index += 1
            self.show_current_frame()
            # Check if we are now on the SelectedImagesFrame
            if isinstance(self.frames[self.current_frame_index], SelectedImagesFrame):
                self.frames[self.current_frame_index].load_selection() 

    # --- Directory and File Handling ---
    def select_directory(self):
        """Opens a directory selection dialog and updates the current directory."""
        self.current_dir = filedialog.askdirectory(initialdir="/", title="Select Directory")
        if self.current_dir:  # Check if a directory was actually selected
            os.chdir(self.current_dir)
            self.load_files_from_directory()

    def load_files_from_directory(self):
        """
        Loads image files from the selected directory, filtering by extension.
        Displays a popup to let the user choose which extensions to include.
        """
        # Get all unique file extensions in the directory
        all_extensions = {
            os.path.splitext(f)[1][1:].lower()  # Extract extension, remove '.', and lowercase
            for f in listdir(self.current_dir)
            if isfile(join(self.current_dir, f)) and os.path.splitext(f)[1]  # Only consider files with extensions
        }

        if not all_extensions:
            messagebox.showwarning("No Extensions Found",
                                   "The selected directory contains no files with recognizable extensions.")
            return

        self.show_extension_popup(all_extensions)

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
            self.files = [
                f
                for f in listdir(self.current_dir)
                if isfile(join(self.current_dir, f)) and
                os.path.splitext(f)[1][1:].lower() in selected_extensions and
                not f.startswith('.')  # Exclude hidden files
            ]
            self.files.sort()  # Sort files for consistent order
            popup.destroy()  # Close the popup
            if isinstance(self.frames[self.current_frame_index], ImageSelectionFrame):
                self.frames[self.current_frame_index].update_displayed_image()

        apply_button = customtkinter.CTkButton(popup, text="Apply", command=apply_extensions)
        apply_button.pack()

    def show_selected_images_frame(self):
        """Destroys the current frame and displays the SelectedImagesFrame."""
        self.frames[self.current_frame_index].destroy()  # Destroy the current frame
        self.current_frame_index += 1  # Move to the next frame (ImageSelectionFrame)
        self.frames[self.current_frame_index].grid(row=0, column=0, sticky="nsew")
        self.show_current_frame()

        # Check if we are now on the SelectedImagesFrame
        if isinstance(self.frames[self.current_frame_index], SelectedImagesFrame):
            self.frames[self.current_frame_index].load_selection()

        # Re-grid the Next button to be below the new frame
        self.next_frame_button.grid(row=1, column=0, columnspan=3, pady=(10, 20)) 

    # --- Logging ---
    def log_message(self, message):
        """Adds a message to the log window."""
        self.log_window.insert(END, message + "\n")
        self.log_window.see(END)  # Scroll to the end

if __name__ == "__main__":
    app = App()
    app.mainloop()
