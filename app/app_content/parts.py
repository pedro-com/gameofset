from abc import ABC, abstractmethod
import customtkinter as ctk
from app_content.image_card import ImageCard
from settings import *
from PIL import Image

class Header(ctk.CTkFrame):
    def __init__(self, master, title_name:str):
        super().__init__(master,
            fg_color = PRIMARY_COLOR,
            corner_radius = 10,
            border_color=ACCENT_COLOR
        )
        title_font = ctk.CTkFont(family = FONT, size = TITLE_TEXT_SIZE, weight = 'bold')
        # Grid configure
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 2), weight = 1, uniform = 'a')
        self.columnconfigure(1, weight = 6, uniform = 'a')
        # Widgets
        self.icon = ImageCard(self,
            APP_ICON,
            bd_width = 3,
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
        menu_icon = ctk.CTkImage(
            light_image = Image.open(MENU_DARK_ICON),
            dark_image=Image.open(MENU_LIGHT_ICON),
            size = (80, 80)
        )
        self.menu_button = ctk.CTkButton(self,
            image = menu_icon,
            text = "",
            fg_color = ACCENT_COLOR
        )
        # Place
        self.icon.grid(row = 0, column = 0, sticky = 'nsew', padx = 10, pady = 20)
        self.page_title.grid(row = 0, column = 1, sticky = 'nsew', padx = 10, pady = 20)
        self.menu_button.grid(row = 0, column = 2, sticky = 'nsew', padx = 10, pady = 20)

class Content(ctk.CTkFrame, ABC):
    def __init__(self, master):
        super().__init__(master)
        self.content_panel = ctk.CTkFrame(self, fg_color = BACKGROUND_COLOR, bg_color=BACKGROUND_COLOR)
        self.tool_panel = ctk.CTkFrame(self, fg_color = SECONDARY_COLOR, bg_color=BACKGROUND_COLOR)
        self.content_panel.place(relx = 0, rely = 0, relwidth = 0.75, relheight = 1)
        self.tool_panel.place(relx = 0.75, rely = 0, relwidth = 0.25, relheight = 1)
    
    @abstractmethod
    def create_content_panel(self):
        pass

    @abstractmethod
    def create_tool_panel(self):
        pass
