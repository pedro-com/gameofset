from typing import Dict, Tuple, List
# from asyncio import run
import customtkinter as ctk
from PIL import Image

from . import custom_widgets as cw
import set_components as sc
import card_draw as cd
from .app_options import Options, Modes
from settings import *

class StructureDrawPanel(ctk.CTkFrame):
    def __init__(self,
            master,
            instructions:str,
            options:Dict,
            bg_color: str | Tuple[str] = BACKGROUND_COLOR,
            fg_color: str | Tuple[str] | None = BACKGROUND_COLOR,
            info_panel_rel_width: float = 0.25,
        ):
        super().__init__(master, bg_color = bg_color, fg_color = fg_color)
        self.instructions = instructions
        self.options = options
        self.info_panel_rel_width = info_panel_rel_width
        self.painted_image = None
        self.card_picker_buttons = []
        self.generate_content_panel()
        self.generate_info_panel()
        self.start_draw()
    
    def init_game(self):
        self.game = sc.SETGame(
            n_attributes=self.options[Options.N_ATTR],
            n_attribute_values=self.options[Options.N_ATTR_V]
        )
        self.set_painter = cd.SETStructureDraw(
            card_resolution=self.options[Options.CARD_QL],
            n_attribute_values=self.options[Options.N_ATTR_V]
        )
    
    def create_structure(self):
        cards = [card_picker.get_card() for card_picker in self.card_picker_buttons if card_picker.get_card() is not None]
        # if len(cards) <= 1:
        #     return
        if self.painted_image:
            self.painted_image.destroy()
        self.painted_image = self.set_painter.generate_card_structure(self.content_panel, self.game.card_structure(cards), bg_color=BG_COLOR)
        self.painted_image.grid(row = 0, column = 0, sticky = 'nsew', padx = PADX, pady = PADY)
        self.download_button.configure(state = 'enabled')


    def start_draw(self):
        self.options.update(self.option_panel.curr_selection)
        self.download_button.configure(state = 'disabled')
        self.init_game()
        # Card Picker Buttons
        for card_picker_button in self.card_picker_buttons:
            card_picker_button.destroy()
        self.card_picker_buttons = []
        for k in range(self.game.n_attributes + 1):
            picker_button = self.set_painter.generate_picker_button(self.info_panel, self.game.n_attributes, update_size_type='fit', button_text=SETPICK, command=self.check_card_selection)
            picker_button.grid(row = k, column = 1, columnspan=2, sticky = 'nsew', pady = CARD_PICKER_PADY)
            self.card_picker_buttons.append(picker_button)

    
    def reset_buttons(self):
        self.download_button.configure(state = 'disabled')
        for card_picker_button in self.card_picker_buttons:
            card_picker_button.reset_button()

    def generate_content_panel(self):
        self.content_panel = ctk.CTkFrame(self, fg_color = BACKGROUND_COLOR)
        self.content_panel.rowconfigure(0, uniform = 'a', weight = 4)
        self.content_panel.rowconfigure(1, uniform = 'a', weight = 1)
        self.content_panel.columnconfigure(0, uniform = 'a', weight = 1)
        # Fonts
        font = ctk.CTkFont(family = GAME_BUTTON_FONT, size = GAME_BUTTON_TEXT_SIZE, weight = "bold")
        self.generate_button = cw.custom_button(self.content_panel, text=GENERATE, font=font, state='disabled', command=self.create_structure)
        self.generate_button.grid(row = 1, column = 0, sticky = 'nsew', padx = PADX, pady = PADY)
        self.content_panel.place(relx = 0, rely = 0, relwidth = 1 - self.info_panel_rel_width, relheight = 1)
    
    def _save_image(self, save_path:str):
        if self.painted_image and self.painted_image.image:
            self.painted_image.image.save(save_path)
    
    def check_card_selection(self):
        cards = {card_picker.get_card() for card_picker in self.card_picker_buttons if card_picker.get_card() is not None}
        if len(cards) <= 1:
            self.generate_button.configure(state='disabled')
        else:
            self.generate_button.configure(state='normal')


    def generate_info_panel(self):
        self.info_panel = ctk.CTkFrame(self, fg_color = SECONDARY_COLOR, corner_radius=0)
        self.info_panel.rowconfigure((0, 1, 2, 3, 4), weight = 5, uniform='a')
        self.info_panel.rowconfigure((5, 6, 7), weight = 2, uniform='a')
        self.info_panel.columnconfigure((0, 3), weight=1, uniform='a')
        self.info_panel.columnconfigure((1, 2), weight=2, uniform='a')

        # Fonts
        option_font = ctk.CTkFont(family = OPTION_FONT, size = OPTION_SELECTION_SIZE, weight = 'bold')
        button_font = ctk.CTkFont(family = INFO_BUTTON_FONT, size = INFO_BUTTON_TEXT_SIZE, weight = 'bold')
        label_font = ctk.CTkFont(family = EXPORT_FONT, size = EXPORT_SIZE, weight = 'bold')

        # Option Panel
        game_info_panel = cw.info_panel(self.info_panel, rel_start=(1, 0), rel_end=(0, 0), rel_width=1, rel_height=1, text=self.instructions, font=button_font)
        self.option_panel = cw.SelectionPanel(self.info_panel, rel_start=(1, 0), rel_end=(0, 0), rel_width=1, rel_height=1,
            selection_font=option_font, button_font=option_font,
            option_dictionary=Modes.get_selection_options(Modes.STRUCTURE_DRAW),
            accept_function=self.start_draw
        )
        self.export_panel = cw.ExportPanel(self.info_panel, rel_start=(1, 0), rel_end=(0, 0), rel_width=1, rel_height=1,
            entry_font=label_font,
            button_font = button_font,
            save_file = self._save_image
        )
        # Buttons
        reset_button = cw.custom_button(self.info_panel, text = RESET, font = button_font, command=self.reset_buttons)
        self.download_button = cw.custom_button(self.info_panel, text = DOWNLOAD, font = button_font, state='disabled', command=self.export_panel.move)
        how_to_use = cw.custom_button(self.info_panel, text = HOWTOUSE, font = button_font, command=game_info_panel.move)
        game_config = cw.custom_button(self.info_panel, text = OPTIONS, font = button_font, command=self.option_panel.move)
        # Grid place
        reset_button.grid(row = 5, column = 0, columnspan = 2, sticky = 'nsew', padx = PADX, pady = CARD_PICKER_PADY)
        self.download_button.grid(row = 5, column = 2, columnspan = 2, sticky = 'nsew', padx = PADX, pady = CARD_PICKER_PADY)
        how_to_use.grid(row = 6, column = 0, columnspan = 4, sticky = 'nsew', padx = PADX, pady = CARD_PICKER_PADY)
        game_config.grid(row = 7, column = 0, columnspan = 4, sticky = 'nsew', padx = PADX, pady = CARD_PICKER_PADY)
        self.info_panel.place(relx = 1 - self.info_panel_rel_width, rely = 0, relwidth = self.info_panel_rel_width, relheight = 1)

