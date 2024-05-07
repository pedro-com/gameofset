from random import sample
from typing import Tuple
from tkinter import StringVar
from .set_deck import SETDeck
from .game_settings import *


class SETPlanetComet(SETDeck):
    def __init__(
        self,
        n_attributes: int,
        n_attribute_values: int,
        set_score: int = 300,
        planet_score: int = 400,
        comet_score: int = 600,
    ):
        super().__init__(n_attributes, n_attribute_values)
        self.set_score = set_score
        self.comet_score = comet_score
        self.planet_score = planet_score
        self.spc_button = None

    @property
    def max_score(self):
        max_sets = (
            int(len(self.deck_cards) // (self.n_attribute_values)) * self.set_score
        )
        max_planets = (
            int(len(self.deck_cards) // ((self.n_attribute_values - 1) * 2))
            * self.planet_score
        )
        max_comets = int(len(self.deck_cards) // self.table_size) * self.comet_score
        return max(max_sets, max(max_planets, max_comets))

    @property
    def table_size(self):
        return self.n_attribute_values * self.n_attribute_values

    def is_valid_selection(self, num_cards: int):
        is_set = num_cards == self.n_attribute_values
        is_planet = num_cards == 2 * (self.n_attribute_values - 1)
        is_comet = num_cards == len(self.table_cards)
        if self.spc_button:
            self.spc_button.configure(
                text=COMET if is_comet else PLANET if is_planet else SET
            )
        return is_set or is_planet or is_comet

    def set_spc_button(self, spc_button: StringVar):
        self.spc_button = spc_button

    def start_game(self):
        self.table_cards = frozenset(sample(tuple(self.deck_cards), self.table_size))
        self.rem_cards = self.deck_cards - self.table_cards
        if self.score:
            self.score.set(0)
        self.modify_game_state()

    def play_round(self, cards: Tuple[int]):
        cards = frozenset(cards)
        if not (cards <= self.table_cards):
            self.add_score(-int(self.set_score / 2))
            return None
        is_set = self.is_set(cards)
        is_planet = self.is_planet(cards)
        is_comet = self.is_comet(cards)
        if not (is_set or is_planet or is_comet):
            self.add_score(-int(self.set_score / 2))
            return None
        self.add_score(
            self.set_score
            if is_set
            else self.comet_score if is_comet else self.planet_score
        )
        refill_cards = min(len(self.rem_cards), len(cards))
        draw_cards = frozenset(sample(tuple(self.rem_cards), refill_cards))
        self.table_cards = (self.table_cards - cards) | draw_cards
        self.rem_cards = self.rem_cards - draw_cards
        self.modify_game_state(
            IS_SET if is_set else IS_COMET if is_comet else IS_PLANET
        )
        return frozenset(draw_cards)

    def is_game_end(self):
        return len(self.rem_cards) == 0 and len(self.table_cards) == 0
