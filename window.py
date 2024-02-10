from customtkinter import *
from PIL import ImageTk, Image

import time_counter

app = CTk()
app.geometry("500x500")
app.title("The bois")

set_appearance_mode(mode_string='dark')
set_default_color_theme("Sweetkind.json")

frame = CTkFrame(master=app, width=300, height=400, fg_color='#ffffff')
frame.pack_propagate(0)
frame.pack(expand=True, side='left')

btn = CTkButton(master=frame, text='Click me', fg_color="transparent", 
                hover_color='#4158D0', border_color='#FFCC70',
                border_width=2)

entry = CTkEntry(master=frame, placeholder_text="Select path", width=200, fg_color="transparent",
                 border_color="#601E88", border_width=1, text_color='#000000').pack(anchor='w', padx=(50, 50), pady=(25, 0))





app.mainloop()

