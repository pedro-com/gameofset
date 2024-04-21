from abc import ABC, abstractmethod
from enum import StrEnum

import customtkinter as ctk
from PIL import Image

from app_content.image_card import ImageCard
from settings import *

class ContentButtons(StrEnum):
    SET_BUTTON = "SET"

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