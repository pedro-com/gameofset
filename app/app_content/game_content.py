from typing import Dict, Tuple, FrozenSet
# from asyncio import run
from random import sample
from tkinter import StringVar
import customtkinter as ctk
from . import custom_widgets as cw
import set_components as sc
import card_draw as cd
from .app_options import Options, Modes
from settings import *


class GamePanel(ctk.CTkFrame):
    content_panel: ctk.CTkFrame = None
    info_panel: ctk.CTkFrame = None
    game: sc.SETDeck
    set_painter: cd.SETStructureDraw
    # Content variables
    content_rows: int
    content_columns: int
    set_button: ctk.CTkButton
    content_cards: Dict[Tuple[int], Tuple[Tuple[int], cd.ImageCard]]
    selected_cards: FrozenSet[Tuple[int]]
    # Info components
    score_meter: cw.ProgressTracker
    timer: cw.Timer

    def __init__(self,
            master,
            game_id:str,
            instructions:str,
            options:Dict,
            bg_color: str | Tuple[str] = BACKGROUND_COLOR,
            fg_color: str | Tuple[str] | None = BACKGROUND_COLOR,
            info_panel_rel_width: float = 0.25,
        ):
        super().__init__(master, bg_color = bg_color, fg_color = fg_color)
        self.game_id = game_id
        self.instructions = instructions
        self.options = options
        self.info_panel_rel_width = info_panel_rel_width
        self.content_cards = None
        self.generate_content_panel()
        self.generate_info_panel()
        self.start_game()

    def select_card(self, card: Tuple[int]):
        if self.timer.is_end.get():
            return
        if self.game.is_game_end():
            return False
        if card in self.selected_cards:
            self.selected_cards = self.selected_cards.difference((card,))
            if not self.game.is_valid_selection(len(self.selected_cards)):
                self.set_button.configure(state = "disabled")
            return True
        if self.game.is_valid_selection(len(self.selected_cards)) and self.game_id not in (Modes.INTERSET_GAME, Modes.SPC_GAME):
            return False
        self.selected_cards = self.selected_cards.union((card,))
        if self.game.is_valid_selection(len(self.selected_cards)):
            self.set_button.configure(state = "normal")
        else:
            self.set_button.configure(state = "disabled")
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
        cards = tuple(self.set_painter.generate_cards(self.content_panel, drawn_cards, card_function=self.select_card))
        for idx, pos in enumerate(card_pos):
            if idx >= len(cards):
                break
            card = cards[idx]
            self.content_cards[card[0]] = (pos, card[1])
            card[1].grid(row = pos[0], column = pos[1], padx = PADX, pady = PADY, sticky = 'nsew')
        if self.game.is_game_end():
            if self.game_id == Modes.END_GAME and self.game.hold_card_remaining():
                found_card = False
                card = None
                self.game.modify_game_state(message = GUESS_CARD)
                while not found_card:
                    picker_window = self.set_painter.generate_picker_window(self, self.game.n_attributes)
                    card = picker_window.show()[0]
                    found_card = card is not None and self.game.guess_hold_card(card)
                card_id, card_image = next(self.set_painter.generate_cards(self.content_panel, (card,), card_function=self.select_card))
                self.content_cards[card_id] = (card_pos[-1], card_image)
                card_image.grid(row = pos[0], column = pos[1], padx = PADX, pady = PADY, sticky = 'nsew')
                return
            self.timer.is_end.set(True)

    def init_game(self):
        if self.game_id == Modes.SET_GAME:
            self.game = sc.SETGame(
                n_attributes=self.options[Options.N_ATTR],
                n_attribute_values=self.options[Options.N_ATTR_V],
                set_score=self.options[Options.SET_SCORE]
            )
        elif self.game_id == Modes.END_GAME:
            self.game = sc.EndGame(
                n_attributes=self.options[Options.N_ATTR],
                n_attribute_values=self.options[Options.N_ATTR_V],
                set_score=self.options[Options.SET_SCORE],
                end_guess_score=self.options[Options.END_GUESS_SCORE]
            )
        elif self.game_id == Modes.INTERSET_GAME:
            self.game = sc.IntersetGame(
                n_attributes=self.options[Options.N_ATTR],
                n_attribute_values=self.options[Options.N_ATTR_V],
                interset_score=self.options[Options.INTERSET_SCORE]
            )
        elif self.game_id == Modes.SPC_GAME:
            self.game = sc.SETPlanetComet(
                n_attributes=self.options[Options.N_ATTR],
                n_attribute_values=self.options[Options.N_ATTR_V],
                set_score=self.options[Options.SET_SCORE],
                comet_score=self.options[Options.COMET_SCORE],
                planet_score=self.options[Options.PLANET_SCORE]
            )
        else:
            raise ValueError(f'Invalid game mode id: {self.game_id}')
        self.set_painter = cd.SETStructureDraw(
            card_resolution=self.options[Options.CARD_QL],
            n_attribute_values=self.options[Options.N_ATTR_V]
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
        cards = self.set_painter.generate_cards(self.content_panel, table_cards, card_function=self.select_card)
        for (card_id, card), pos in zip(cards, card_positions):
            self.content_cards[card_id] = (pos, card)
            card.grid(row = pos[0], column = pos[1], padx = PADX, pady = PADY, sticky = 'nsew')
        self.timer.start()
        if not self.timer.is_end.trace_info():
            self.timer.is_end.trace_add("write", lambda *args: self.game.modify_game_state(timer_end=self.timer.is_end.get()))
        self.set_button.configure(state="disabled")
    
    def generate_content_panel(self):
        if self.content_panel:
            self.content_panel.place_forget()
            self.content_panel.destroy()
        self.content_panel = ctk.CTkFrame(self, fg_color = BACKGROUND_COLOR)
        self.init_game()
        # Set content grid
        self.content_rows = self.game.n_attributes + 1 if self.game_id != Modes.SPC_GAME else self.game.n_attribute_values + 1
        self.content_columns = self.game.n_attribute_values
        self.content_panel.rowconfigure(tuple(range(self.content_rows)), uniform = 'a', weight = 1)
        self.content_panel.columnconfigure(tuple(range(self.content_columns)), uniform = 'a', weight = 1)
        # Main game button
        font = ctk.CTkFont(family = GAME_BUTTON_FONT, size = GAME_BUTTON_TEXT_SIZE, weight = "bold")
        text = INTERSET if self.game_id == Modes.INTERSET_GAME else SET
        self.set_button = cw.custom_button(self.content_panel, text=text, font=font, command=self.play_selection)
        # For the SetPlanetComet gamemode
        if self.game_id == Modes.SPC_GAME:
            self.game.set_spc_button(self.set_button)
        self.set_button.grid(row = self.content_rows - 1, column = 0, columnspan = self.content_columns, sticky = 'nsew', padx = PADX, pady = PADY)
        self.content_panel.place(relx = 0, rely = 0, relwidth = 1 - self.info_panel_rel_width, relheight = 1)
    
    def _update_options(self):
        self.options.update(self.option_panel.curr_selection)
        self.content_cards = {}
        self.generate_content_panel()
        self.score_meter.modify_max_value(self.game.max_score)
        self.timer.modify_max_value(self.options[Options.GAME_TM])
        self.start_game()

    def generate_info_panel(self):
        self.info_panel = ctk.CTkFrame(self, fg_color = SECONDARY_COLOR, corner_radius=0) #, border_width=2, border_color=ACCENT_COLOR)
        self.info_panel.columnconfigure(0, uniform = 'a', weight = 1)
        self.info_panel.rowconfigure((0, 1, 2), uniform = 'a', weight = 2)
        self.info_panel.rowconfigure((3, 4, 5), uniform = 'a', weight = 1)
        # Fonts
        label_font = ctk.CTkFont(family = OUTPUT_FONT, size = OUTPUT_TEXT_SIZE, weight = 'bold')
        button_font = ctk.CTkFont(family = INFO_BUTTON_FONT, size = INFO_BUTTON_TEXT_SIZE, weight = 'bold')
        option_font = ctk.CTkFont(family = OPTION_FONT, size = OPTION_SELECTION_SIZE, weight = 'bold')
        # Score and timer
        self.score_meter = cw.ProgressTracker(self.info_panel, self.game.max_score, text_format = SCORE, progress_color=SCORE_COLOR)
        self.timer = cw.Timer(self.info_panel, max_time=self.options[Options.GAME_TM], text_format = TIMER, progress_color=TIMER_COLOR)
        self.game_label = cw.TextOutput(self.info_panel, text = REM_CARDS % (0,), font = label_font)
        # Info panels
        game_info_panel = cw.info_panel(self.info_panel, rel_start=(1, 0), rel_end=(0, 0), rel_width=1, rel_height=1, text=self.instructions, font=button_font)
        self.option_panel = cw.SelectionPanel(self.info_panel, rel_start=(1, 0), rel_end=(0, 0), rel_width=1, rel_height=1,
            selection_font=option_font, button_font=option_font,
            option_dictionary=Modes.get_selection_options(self.game_id),
            accept_function=self._update_options
        )
        # Info buttons
        how_to_play = cw.custom_button(self.info_panel, text = HOWTO, font = button_font, command=game_info_panel.move)
        restart_game = cw.custom_button(self.info_panel, text = RESTART, font = button_font, command = self.start_game)
        game_config = cw.custom_button(self.info_panel, text = OPTIONS, font = button_font, command=self.option_panel.move)
        # Place the widgets
        self.score_meter.grid(row = 0, sticky = 'nsew', padx = PADX, pady = PADY)
        self.timer.grid(row = 1, sticky = 'nsew', padx = PADX, pady = PADY)
        self.game_label.grid(row = 2, sticky = 'nsew', padx = PADX, pady = PADY)
        how_to_play.grid(row = 3, sticky = 'nsew', padx = PADX, pady = PADY)
        restart_game.grid(row = 4, sticky = 'nsew', padx = PADX, pady = PADY)
        game_config.grid(row = 5, sticky = 'nsew', padx = PADX, pady = PADY)
        self.info_panel.place(relx = 1 - self.info_panel_rel_width, rely = 0, relwidth = self.info_panel_rel_width, relheight = 1)
