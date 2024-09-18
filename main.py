import customtkinter
from tkinter import filedialog, scrolledtext, END, WORD
from PIL import Image, ImageTk
import os
from frames.instructions_frame import InstructionsFrame
from frames.image_selection_frame import ImageSelectionFrame
from frames.selected_images_frame import SelectedImagesFrame

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Photo Selector")
        self.geometry('650x650')

        # Frame Management
        self.frames = {}
        self.current_frame = None

        # Main Frame to hold and center content
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)  # Allow vertical expansion
        self.main_frame.grid_columnconfigure(0, weight=1)  # Allow horizontal expansion

        # Application Data
        self.current_directory = None
        self.image_files = []
        self.selected_images = {}

        # Create Frames 
        self.create_instructions_frame()
        self.create_image_selection_frame()
        self.create_selected_images_frame()

        # Show Initial Frame
        self.show_frame("InstructionsFrame")

        # --- Navigation Buttons ---
        self.button_frame = customtkinter.CTkFrame(self)  # Frame for buttons
        self.button_frame.grid(row=1, column=0, sticky="ew")  # Place below main frame

        self.next_button = customtkinter.CTkButton(self.button_frame, text="Next", command=self.next_frame)
        self.next_button.pack(side="right", pady=(20, 20), padx=(20, 20))

        self.back_button = customtkinter.CTkButton(self.button_frame, text="Back", command=self.previous_frame)
        self.back_button.pack(side="left", pady=(20, 20), padx=(20, 20))

        # --- Log Window --- 
        self.log_window = scrolledtext.ScrolledText(self, wrap=WORD, height=5)
        self.log_window.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        # Configure grid weights for the main window
        self.grid_rowconfigure(0, weight=1)  # Main frame expands vertically
        self.grid_columnconfigure(0, weight=1)  # Main frame expands horizontally
        self.grid_rowconfigure(2, weight=0)  # Log window doesn't expand

    def create_instructions_frame(self):
        self.frames["InstructionsFrame"] = InstructionsFrame(self)
        self.frames["InstructionsFrame"].grid(row=0, column=0, sticky="nsew")

    def create_image_selection_frame(self):
        self.frames["ImageSelectionFrame"] = ImageSelectionFrame(self)
        self.frames["ImageSelectionFrame"].grid(row=0, column=0, sticky="nsew")

    def create_selected_images_frame(self):
        self.frames["SelectedImagesFrame"] = SelectedImagesFrame(self)
        self.frames["SelectedImagesFrame"].grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.grid_forget()
        self.current_frame = self.frames[frame_name]
        self.current_frame.tkraise()

    def next_frame(self):
        if self.current_frame == self.frames["InstructionsFrame"]:
            self.show_frame("ImageSelectionFrame")
        elif self.current_frame == self.frames["ImageSelectionFrame"]:
            self.show_frame("SelectedImagesFrame")
            self.frames["SelectedImagesFrame"].load_selection()  # Load images when shown
        else:
            self.log_message("No next frame available.")

    def previous_frame(self):
        if self.current_frame == self.frames["SelectedImagesFrame"]:
            self.show_frame("ImageSelectionFrame")
        elif self.current_frame == self.frames["ImageSelectionFrame"]:
            self.show_frame("InstructionsFrame")
        else:
            self.log_message("No previous frame available.")

    # --- Logging ---
    def log_message(self, message):
        """Adds a message to the log window."""
        self.log_window.insert(END, message + "\n")
        self.log_window.see(END)  # Scroll to the end

if __name__ == "__main__":
    app = App()
    app.mainloop()