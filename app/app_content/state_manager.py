from typing import Tuple
from tkinter import StringVar
import customtkinter as ctk
from .image_card import ImageCard
from .custom_widgets import game_button
from settings import *

class ContentManager(ctk.CTk):
    def __init__(self,
            fg_color: str | Tuple[str, str] | None = BG_COLOR,
            width:int = WINDOW_WIDTH,
            height:int = WINDOW_HEIGHT,
            update_size:bool = False,
            info_panel_width: float = 0.75,
            **kwargs
        ):
        super().__init__(fg_color, **kwargs)
        self.geometry(f'{width}x{height}')
        if not update_size:
            self.maxsize(width, height)
            self.minsize(width, height)
        
    
    def generate_header(self):
        header = ctk.CTkFrame(self, fg_color = PRIMARY_COLOR, corner_radius = 0, border_color=ACCENT_COLOR)
        header.rowconfigure(0, weight = 1)
        header.columnconfigure((0, 2), weight = 1, uniform = 'a')
        header.columnconfigure(1, weight = 4, uniform = 'a')
        title_font = ctk.CTkFont(family = TITLE_FONT, size = TITLE_TEXT_SIZE, weight = 'bold')
        icon = ImageCard(self, APP_ICON,
            bd_width = 3,
            card_id = "set_icon",
            bg_color = BACKGROUND_COLOR,
            bd_color = SECONDARY_COLOR,
            relief='flat'
        )
        self.title_text = StringVar(value = 0)
        self.page_title = ctk.CTkLabel(self,
            text = title_name,
            anchor = 'center',
            font = title_font,
            bg_color = PRIMARY_COLOR,
            text_color = TITLE_TEXT_COLOR
        )
        header.grid(row = 0, column = 0, sticky = 'nsew', padx = 10, pady = 20)


# header.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.15)
# content.place(relx = 0, rely = 0.15, relwidth = 1, relheight = 0.85)
class Header(ctk.CTkFrame):
    def __init__(self, master, title_name:str):
        super().__init__(master,
            fg_color = PRIMARY_COLOR,
            corner_radius = 0,
            border_color=ACCENT_COLOR
        )
        title_font = ctk.CTkFont(family = TITLE_FONT, size = TITLE_TEXT_SIZE, weight = 'bold')
        # Grid configure
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 2), weight = 1, uniform = 'a')
        self.columnconfigure(1, weight = 6, uniform = 'a')
        # Widgets
        self.icon = ImageCard(self,
            APP_ICON,
            bd_width = 3,
            card_id = "set_icon",
            bg_color = BACKGROUND_COLOR,
            bd_color = SECONDARY_COLOR,
            relief='flat'
        )
        self.page_title = ctk.CTkLabel(self,
            text = title_name,
            anchor = 'center',
            font = title_font,
            bg_color = PRIMARY_COLOR,
            text_color = TITLE_TEXT_COLOR
        )
        # menu_icon = ctk.CTkImage(
        #     light_image = Image.open(MENU_DARK_ICON),
        #     dark_image=Image.open(MENU_LIGHT_ICON),
        #     size = (80, 80)
        # )
        # self.menu_button = ctk.CTkButton(self,
        #     image = menu_icon,
        #     text = "",
        #     fg_color = ACCENT_COLOR
        # )
        # Place
        self.icon.grid(row = 0, column = 0, sticky = 'nsew', padx = 10, pady = 20)
        self.page_title.grid(row = 0, column = 1, sticky = 'nsew', padx = 10, pady = 20)
        # self.menu_button.grid(row = 0, column = 2, sticky = 'nsew', padx = 10, pady = 20)