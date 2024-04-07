import os
os.chdir('app')
import tkinter as tk
import customtkinter as ctk
from app_content.parts import Header, Content
from settings import *

window = tk.Tk()
window.geometry('800x600')
# self.maxsize(width, height)
# self.minsize(width, height)
window.title('The Game of SET')
window.columnconfigure(0, weight = 1, uniform = 'a')
window.configure(background = BACKGROUND_COLOR)
header = Header(window, title_name='The Game of SET')
content = Content(window)
# relleno1 = ctk.CTkLabel(window, text = 'Relleno', bg_color = 'red')
# relleno2 = ctk.CTkLabel(window, text = 'Relleno', bg_color = 'blue')
header.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.2)
content.place(relx = 0, rely = 0.2, relwidth = 1, relheight = 0.9)
# header.set_menu_button('assets/MenuButton.png')
# relleno1.place(relx = 0, rely = 0.2, relwidth = 0.7, relheight =0.8)
# relleno2.place(relx = 0.7, rely = 0.2, relwidth = 0.3, relheight =0.8)
# header.grid(row = 0, column = 0, sticky = 'nswe')
# relleno.grid(row = 1, column = 0, sticky = 'nswe')
window.mainloop()