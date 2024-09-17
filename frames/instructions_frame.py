import customtkinter
import tkinterweb
import markdown2

import customtkinter
import tkinterweb
import markdown2

class InstructionsFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # --- Web Browser Widget ---
        self.browser = tkinterweb.HtmlFrame(self, messages_enabled=False)
        self.browser.pack(pady=20, padx=20)

        # Convert Markdown to HTML (correct indentation)
        markdown_text = """
# Welcome to the Photo Selector App!

### This is an app I designed to assist me in selecting photos I want to edit. 
#### Many modern cameras can produce multiple files per photo, usually a JPG and a raw file. This app is designed to assist in the selection process by filtering to just the jpgs, then allowing the user to select the photos they want to move forward with. Once selected, the program will copy the corisponding raw files to a new directory.

## Instructions:

1. **Click "Next" to begin.**
2. Choose a directory containing your images, then select the file extension you want to use.
3. Select the images you want to proseed with, then click "Next"
"""
        html_text = markdown2.markdown(markdown_text)  # Convert Markdown to HTML

        # --- Add CSS for background and text color ---
        html_text = f"""
        <style>
            body {{
                background-color: #353535;
                color: lightgray;
                font-family: Arial, sans-serif; /* Try different font families */
                font-size: 12pt; /* Adjust font size */
            }}
        </style>
        {html_text}
        """

        # Load HTML into the browser widget
        self.browser.load_html(html_text)
