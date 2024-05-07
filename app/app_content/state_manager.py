from typing import Tuple, Callable
import customtkinter as ctk

from .app_options import Modes
from card_draw import ImageCard
from . import custom_widgets as cw
from settings import *
from .game_content import GamePanel
from .set_structure_painter import StructureDrawPanel
class AppModePanel(cw.SlidingFrame):
    def __init__(self,
            master,
            rel_start: Tuple[float] = (1, 0.15),
            rel_end: Tuple[float] = (0.75, 0.15),
            rel_width: float = 0.25,
            rel_height: float = 0.85,
            change_mode: Callable[[str], None] = lambda app_mode: (),
            corner_radius: int | str | None = 10,
            border_width: int | str | None = BD_WIDTH,
            fg_color: str | Tuple[str] | None = PRIMARY_COLOR,
            border_color: str | Tuple[str] | None = ACCENT_COLOR,
            animation_steps: int = 10,
            anchor: str = 'nw'
        ):
        super().__init__(master, rel_start, rel_end, rel_width, rel_height, corner_radius, border_width, fg_color, border_color, animation_steps, anchor)
        if change_mode is None:
            self.change_mode = lambda app_mode: ()
        else:
            self.change_mode = change_mode
        font = ctk.CTkFont(family=MENU_BUTTON_FONT, size = MENU_BUTTON_SIZE, weight = 'bold')        
        for app_mode, app_values in Modes.APP_MODES.items():
            button_option = cw.custom_button(self,
                text = app_values["name"],
                font = font,
                command = lambda app_mode=app_mode: self.select_button(app_mode)
            )
            button_option.pack(fill = 'both', expand = True, pady = 10, padx = 10)

    def select_button(self, app_mode:str):
        self.quick_move()
        self.change_mode(app_mode)

# <https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture>
class App(ctk.CTk):
    def __init__(self,
            fg_color: str | Tuple[str, str] | None = BG_COLOR,
            width:int = WINDOW_WIDTH,
            height:int = WINDOW_HEIGHT,
            is_min_size:bool = False,
            info_panel_width: float = 0.25,
            header_height: float = 0.15,
            init_app_option: str = Modes.SET_GAME
        ):
        super().__init__(fg_color)
        self.info_panel_width = info_panel_width
        self.header_height = header_height
        self.geometry(f'{width}x{height}')
        self.title('SET Application')
        if is_min_size:
            self.minsize(width, height)
        self.mode_panel = AppModePanel(self,
            rel_start = (1, self.header_height),
            rel_end= (1 - self.info_panel_width, self.header_height),
            rel_width= self.info_panel_width,
            rel_height = 1 - self.header_height,
            change_mode = self.place_content
        )
        self.content_panel = None
        self.generate_header()
        self.place_content(init_app_option)
    
    def generate_header(self):
        header = ctk.CTkFrame(self, fg_color = PRIMARY_COLOR, corner_radius = 0, border_color=ACCENT_COLOR)
        header.rowconfigure(0, weight = 1)
        header.columnconfigure((0, 2), weight = 1, uniform = 'a')
        header.columnconfigure(1, weight = 4, uniform = 'a')
        title_font = ctk.CTkFont(family = TITLE_FONT, size = TITLE_TEXT_SIZE, weight = 'bold')
        icon = ImageCard(header, APP_ICON,
            bd_width = 3,
            image_id = "set_icon",
            bg_color = BACKGROUND_COLOR,
            bd_color = SECONDARY_COLOR,
            relief='flat'
        )
        self.page_title = ctk.CTkLabel(header,
            anchor = 'center',
            font = title_font,
            bg_color = PRIMARY_COLOR,
            text_color = TITLE_TEXT_COLOR
        )
        # font = ctk.CTkFont(family=MENU_BUTTON_FONT, size=MENU_BUTTON_SIZE, weight='bold')
        menu_button = cw.custom_button(header,
            text = MENU,
            font = title_font,
            command = self.mode_panel.move
        )
        icon.grid(row = 0, column = 0, sticky = 'nsew', padx = 10, pady = 20)
        self.page_title.grid(row = 0, column = 1, sticky = 'nsew', padx = 10, pady = 20)
        menu_button.grid(row = 0, column = 2, sticky = 'nsew', padx = 10, pady = 20)
        header.place(relx = 0, rely = 0, relwidth = 1, relheight = self.header_height)
    
    def place_content(self, app_mode:str):
        if self.content_panel is not None:
            self.content_panel.destroy()
        app_mode_values = Modes.APP_MODES[app_mode]
        self.page_title.configure(text = app_mode_values["name"])
        if app_mode != Modes.STRUCTURE_DRAW:
            self.content_panel = GamePanel(self,
                game_id=app_mode,
                instructions=app_mode_values["instructions"],
                options=app_mode_values["options"],
                info_panel_rel_width=self.info_panel_width
            )
        else:
            self.content_panel = StructureDrawPanel(self,
                instructions=app_mode_values["instructions"],
                options=app_mode_values["options"],
                info_panel_rel_width=self.info_panel_width
            )
        self.content_panel.place(relx = 0, rely = self.header_height, relwidth = 1, relheight = 1 - self.header_height)
