import customtkinter
from tkinter import scrolledtext, END, WORD
from PIL import Image

# --- Global Constants ---
PLACEHOLDER_IMAGE_PATH = "assets/missing.jpg"  # Path to the placeholder image

class ImageSelectionFrame(customtkinter.CTkFrame):
    """
    Frame for displaying and selecting images.
    """

    def __init__(self, parent, frame_index):  # Add frame_index as a parameter
        super().__init__(parent)
        self.parent = parent
        self.frame_index = frame_index  # Store the frame index

        self.grid_columnconfigure((0, 1, 2), weight=1)

        # --- Directory Selection Button ---
        self.directory_button = customtkinter.CTkButton(self, text="Choose Directory",
                                                        command=self.parent.select_directory)
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

        # --- Keyboard Shortcuts ---
        self.bind("<Left>", self.prev_button_callback)
        self.bind("<Right>", self.next_button_callback)
        self.bind("<space>", self.toggle_checkbox)

        # self.log_message("Application started")

    # --- Navigation and Selection Callbacks ---
    def prev_button_callback(self, event=None):
        """Handles moving to the previous image."""
        if self.parent.files:
            self.parent.current_index = max(0, self.parent.current_index - 1)
            self.check_var.set("off")  # Uncheck the checkbox when moving to a new image
            self.update_displayed_image()
        else:
            self.log_message("Please select a directory first.")

    def next_button_callback(self, event=None):
        """Handles moving to the next image."""
        if self.parent.files:
            self.parent.current_index = (self.parent.current_index + 1) % len(self.parent.files)
            self.check_var.set("off")  # Uncheck the checkbox when moving to a new image
            self.update_displayed_image()
        else:
            self.log_message("Please select a directory first.")

    def update_displayed_image(self):
        """Updates the displayed image and checkbox state based on the current index."""
        if self.parent.files:
            image_path = f"{self.parent.current_dir}/{self.parent.files[self.parent.current_index]}"
            try:
                new_image = customtkinter.CTkImage(light_image=Image.open(image_path), size=(256, 256))
                self.current_image_label.configure(image=new_image)

                # Set checkbox state based on whether the image is selected
                if self.parent.files[self.parent.current_index] in self.parent.selected_images:
                    self.check_var.set("on")
                else:
                    self.check_var.set("off")
            except Exception as e:
                self.log_message(f"Error loading image {image_path}: {e}")
        else:
            self.current_image_label.configure(image=self.placeholder_image)
            self.log_message("Please select a directory first.")

    def checkbox_event(self):
        """Handles checkbox state changes, updating the selected images dictionary."""
        if self.parent.files:
            current_image_path = self.parent.files[self.parent.current_index]
            if self.check_var.get() == "on":
                self.parent.selected_images[current_image_path] = True
                self.log_message(f"Selected {current_image_path}")
            else:
                self.parent.selected_images.pop(current_image_path, None)
                self.log_message(f"Deselected {current_image_path}")
        else:
            self.log_message("Please select a directory first.")
            self.check_var.set("off")

    def toggle_checkbox(self, event=None):
        """Toggles the state of the selection checkbox."""
        if self.check_var.get() == "on":
            self.check_var.set("off")
        else:
            self.check_var.set("on")
        self.checkbox_event()  # Trigger the checkbox event to handle selection logic

    # --- Done Button ---
    def next_frame_button_callback(self):
        """Handles the "Next" button click and replaces this frame."""
        self.parent.show_selected_images_frame()