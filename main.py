from tkinter import *
import customtkinter
from PIL import Image

customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

#app = Tk()
app = customtkinter.CTk()
app.title('Photo Picker')
app.geometry('650x400')


current_image = customtkinter.CTkImage(light_image=Image.open('../../Pictures/headshot.png'), size=(256,256)) # WidthxHeight

my_label = customtkinter.CTkLabel(app, text="", image=current_image)

my_label.grid(row=1, column=2, padx=20, pady=20)

def prev_button_callback():
    print("button pressed")

def next_button_callback():
    print("button pressed")

prev_button = customtkinter.CTkButton(app, text="Previous Image", command=prev_button_callback)
prev_button.grid(row=2, column=1, padx=20, pady=20)

next_button = customtkinter.CTkButton(app, text="Next Image", command=next_button_callback)
next_button.grid(row=2, column=3, padx=20, pady=20)


app.mainloop()