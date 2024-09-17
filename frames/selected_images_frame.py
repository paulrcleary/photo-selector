import customtkinter
from PIL import Image

# --- Global Constants ---
PLACEHOLDER_IMAGE_PATH = "assets/missing.jpg"  # Path to the placeholder image

class SelectedImagesFrame(customtkinter.CTkFrame):
    """
    Frame for displaying the selected images.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # --- Missing Image Placeholder ---
        try:
            missing_image = customtkinter.CTkImage(light_image=Image.open(PLACEHOLDER_IMAGE_PATH), size=(200, 200))
        except FileNotFoundError:
            print(f"Warning: '{PLACEHOLDER_IMAGE_PATH}' not found. Using a blank label.")
            missing_image = None

        self.missing_image_label = customtkinter.CTkLabel(self, text="", image=missing_image)
        self.missing_image_label.grid(row=0, column=0, padx=20, pady=20)

        self.image_labels = []  # List to store references to the displayed image labels

    def load_selection(self):
        """Loads and displays the selected images in a grid."""
        # Clear any previously displayed images
        for label in self.image_labels:
            label.grid_forget()  # Remove old labels from the grid
        self.image_labels = []  # Reset the list of image labels

        if self.parent.selected_images:
            self.missing_image_label.grid_forget()  # Hide the "no images" placeholder

            row = 0
            column = 0
            for image_path in self.parent.selected_images:
                try:
                    # Create an image label and place it in the grid
                    image_label = customtkinter.CTkLabel(
                        self,
                        text="",
                        image=customtkinter.CTkImage(light_image=Image.open(f"{self.parent.current_dir}/{image_path}"),
                                                    size=(200, 200))
                    )
                    image_label.grid(row=row, column=column, padx=20, pady=20)
                    self.image_labels.append(image_label)  # Store the label for later cleanup

                    # Grid layout management
                    column += 1
                    if column == 3:
                        column = 0
                        row += 1
                except Exception as e:
                    self.parent.log_message(f"Error loading image {image_path}: {e}")
        else:
            self.missing_image_label.grid(row=0, column=0, padx=20, pady=20)  # Show the placeholder



