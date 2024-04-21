from typing import Dict, Tuple, FrozenSet
# from asyncio import run
from random import sample
import customtkinter as ctk
from PIL import Image

from .image_card import ImageCard
from .my_widgets import ProgressTracker, TextOutput, Timer
from set_components.set_game import SETGame
from card_draw.draw_set_structure import SETStructureDraw
from settings import *

GAME_SETTINGS = {
    "n_attributes": 4,
    "n_attribute_values": 3,
    "set_score": 300,
    "card_quality": 2,
    "game_time": 270
}

# PADX = 10
# PADY = 10
class GamePanel(ctk.CTkFrame):
    content_panel: ctk.CTkFrame = None
    info_panel: ctk.CTkFrame = None
    game: SETGame
    set_painter: SETStructureDraw
    # Content variables
    content_rows: int
    content_columns: int
    set_button: ctk.CTkButton
    content_cards: Dict[Tuple[int], Tuple[Tuple[int], ImageCard]]
    selected_cards: FrozenSet[Tuple[int]]
    # Info components
    score_meter: ProgressTracker
    timer: Timer

    def __init__(self, master, bg_color: str | Tuple[str] = BACKGROUND_COLOR, fg_color: str | Tuple[str] | None = BACKGROUND_COLOR):
        super().__init__(master, bg_color = bg_color, fg_color = fg_color)
        self.content_cards = None
        self.generate_content_panel()
        self.generate_info_panel()
        self.start_game()
    
    @staticmethod
    def game_button(master, text:str, command = lambda: (), text_color:str=BG_COLOR, state:str="normal", font:ctk.CTkFont = None, border_width=BD_WIDTH):
        return ctk.CTkButton(master,
            fg_color=BUTTON_COLOR,
            hover_color=ACCENT_COLOR,
            border_width=border_width,
            border_color=ACCENT_COLOR,
            font=font,
            state=state,
            text=text,
            text_color=text_color,
            command=command
        )
    
    def generate_card(self, master, card_image: Image, card_id: Tuple[int]):
        return ImageCard(master, image=card_image, card_id=card_id, bg_color="white", is_button=True, card_function=self.select_card)
    
    def select_card(self, card: Tuple[int]):
        if self.timer.is_end.get():
            return
        if self.game.is_game_end():
            return False
        if card in self.selected_cards:
            self.set_button.configure(state = "disabled")
            self.selected_cards = self.selected_cards.difference((card,))
            return True
        if self.game.is_valid_selection(len(self.selected_cards)):
            return False
        self.selected_cards = self.selected_cards.union((card,))
        if self.game.is_valid_selection(len(self.selected_cards)):
            self.set_button.configure(state = "normal")
        return True
    
    def destroy_cards(self, card_ids:Tuple[int]):
        available_pos = []
        for card_id in card_ids:
            prev_pos, prev_card = self.content_cards[card_id]
            del self.content_cards[card_id]
            prev_card.grid_forget()
            prev_card.destroy()
            available_pos.append(prev_pos)
        return available_pos

    def play_selection(self):
        self.set_button.configure(state = "disabled")
        if self.timer.is_end.get():
            return
        drawn_cards = self.game.play_round(self.selected_cards)
        if drawn_cards is None:
            for card_id in self.selected_cards:
                self.content_cards[card_id][1].change_selection()
            self.selected_cards = frozenset()
            return
        card_pos = self.destroy_cards(self.selected_cards)
        self.selected_cards = frozenset()
        drawn_cards = tuple(drawn_cards)
        card_images = self.set_painter.draw_card_list(drawn_cards)
        for idx, pos in enumerate(card_pos):
            if idx >= len(drawn_cards):
                break
            card = self.generate_card(self.content_panel, card_images[idx], drawn_cards[idx])
            self.content_cards[drawn_cards[idx]] = (pos, card)
            card.grid(row = pos[0], column = pos[1], padx = PADX, pady = PADY, sticky = 'nsew')
        if self.game.is_game_end():
            self.timer.is_end.set(True)

    def init_game(self):
        self.game = SETGame(
            n_attributes=GAME_SETTINGS["n_attributes"],
            n_attribute_values=GAME_SETTINGS["n_attribute_values"],
            set_score=GAME_SETTINGS["set_score"]
        )
        self.set_painter = SETStructureDraw(
            card_resolution=GAME_SETTINGS["card_quality"],
            n_attribute_values=GAME_SETTINGS["n_attribute_values"]
        )
    
    def start_game(self):
        # Start the set game
        self.game.set_score_tracker(self.score_meter.actual_value)
        self.game.set_game_state(self.game_label.text)
        self.timer.reset()
        if self.content_cards:
            self.destroy_cards(list(self.content_cards.keys()))
        self.game.start_game()
        # Create the available card positions
        self.content_cards = {}
        card_positions = ((row, col) for row in range(self.content_rows - 1) for col in range(self.content_columns))
        # Initialize game variables
        self.selected_cards = frozenset()
        table_cards = sample(tuple(self.game.table_cards), self.game.table_size)
        # card_images = run(self.set_painter.adraw_card_list(table_cards))
        card_images = self.set_painter.draw_card_list(table_cards)
        for idx, pos in enumerate(card_positions):
            card = self.generate_card(self.content_panel, card_images[idx], table_cards[idx])
            self.content_cards[table_cards[idx]] = (pos, card)
            card.grid(row = pos[0], column = pos[1], padx = PADX, pady = PADY, sticky = 'nsew')
        self.timer.start()
        if not self.timer.is_end.trace_info():
            self.timer.is_end.trace_add("write", lambda *args: self.game.modify_game_state(timer_end=self.timer.is_end.get()))
        # self.game.play_round(next(self.game.table_sets()))
        self.set_button.configure(state="disabled")
    
    def generate_content_panel(self):
        if self.content_panel:
            self.content_panel.place_forget()
        self.content_panel = ctk.CTkFrame(self, fg_color = BACKGROUND_COLOR)
        self.init_game()
        # Set content grid
        self.content_rows = self.game.n_attributes + 1
        self.content_columns = self.game.n_attribute_values
        self.content_panel.rowconfigure(tuple(range(self.content_rows)), uniform = 'a', weight = 1)
        self.content_panel.columnconfigure(tuple(range(self.content_columns)), uniform = 'a', weight = 1)
        # SET! button
        font = ctk.CTkFont(family = GAME_BUTTON_FONT, size = GAME_BUTTON_TEXT_SIZE, weight = "bold")
        self.set_button = self.game_button(self.content_panel, text = SET, font = font, command = self.play_selection)
        self.set_button.grid(row = self.content_rows - 1, column = 0, columnspan = self.content_columns, sticky = 'nsew', padx = PADX, pady = PADY)
        self.content_panel.place(relx = 0, rely = 0, relwidth = 0.75, relheight = 1)
    
    def generate_info_panel(self):
        self.info_panel = ctk.CTkFrame(self, fg_color = SECONDARY_COLOR, corner_radius=0) #, border_width=2, border_color=ACCENT_COLOR)
        self.info_panel.columnconfigure(0, uniform = 'a', weight = 1)
        self.info_panel.rowconfigure((0, 1, 2), uniform = 'a', weight = 2)
        self.info_panel.rowconfigure((3, 4, 5), uniform = 'a', weight = 1)
        # Score and timer
        self.score_meter = ProgressTracker(self.info_panel, self.game.max_score, text_format = SCORE, progress_color=SCORE_COLOR)
        self.timer = Timer(self.info_panel, max_time=GAME_SETTINGS["game_time"], text_format = TIMER, progress_color=TIMER_COLOR)
        self.game_label = TextOutput(self.info_panel, text = REM_CARDS % (0,))
        # Info buttons
        button_font = ctk.CTkFont(family = INFO_BUTTON_FONT, size = INFO_BUTTON_TEXT_SIZE, weight = 'bold')
        how_to_play = self.game_button(self.info_panel, text = HOWTO, font = button_font)
        restart_game = self.game_button(self.info_panel, text = RESTART, font = button_font, command = self.start_game)
        game_config =  self.game_button(self.info_panel, text = OPTIONS, font = button_font)
        # Place the widgets
        self.score_meter.grid(row = 0, sticky = 'nsew', padx = PADX, pady = PADY)
        self.timer.grid(row = 1, sticky = 'nsew', padx = PADX, pady = PADY)
        self.game_label.grid(row = 2, sticky = 'nsew', padx = PADX, pady = PADY)
        how_to_play.grid(row = 3, sticky = 'nsew', padx = PADX, pady = PADY)
        restart_game.grid(row = 4, sticky = 'nsew', padx = PADX, pady = PADY)
        game_config.grid(row = 5, sticky = 'nsew', padx = PADX, pady = PADY)
        self.info_panel.place(relx = 0.75, rely = 0, relwidth = 0.25, relheight = 1)
