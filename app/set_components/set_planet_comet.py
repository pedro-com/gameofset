from random import sample
from typing import Tuple
from .set_deck import SETDeck
from settings import *

class SETPlanetComet(SETDeck):
    def __init__(self, n_attributes: int, n_attribute_values: int, set_score: int = 300, comet_score: int = 400, planet_score:int = 600):
        super().__init__(n_attributes, n_attribute_values)
        self.set_score = set_score
        self.comet_score = comet_score
        self.planet_score = planet_score
    
    @property
    def max_score(self):
        return int(len(self.deck_cards) // (self.n_attribute_values*self.n_attribute_values)) * self.planet_score
    
    @property
    def table_size(self):
        return self.n_attribute_values*self.n_attribute_values
    
    def start_game(self):
        self.table_cards = frozenset(sample(tuple(self.deck_cards), self.table_size))
        self.rem_cards = self.deck_cards - self.table_cards
        if self.score:
            self.score.set(0)
        self.modify_game_state()
    
    def play_round(self, cards: Tuple[int]):
        cards = frozenset(cards)
        if not (cards <= self.table_cards):
            self.add_score( - int(self.set_score / 2))
            return frozenset()
        is_set = len(cards) == self.n_attribute_values and self.is_set(cards)
        is_comet = len(cards) == 2*self.n_attribute_values - 2 and self.is_comet(cards)
        is_planet = len(cards) == self.n_attribute_values*self.n_attribute_values and self.is_magic_square(cards)
        if not (is_set or is_comet or is_planet):
            self.add_score( - int(self.set_score / 2))
            return frozenset()
        self.add_score(self.set_score if is_set else self.comet_score if is_comet else self.planet_score)
        self.modify_game_state(IS_SET if is_set else IS_COMET if is_comet else IS_PLANET)
        draw_cards = frozenset(sample(tuple(self.rem_cards), len(cards)))
        self.table_cards = (self.table_cards - cards) | draw_cards
        self.rem_cards = self.rem_cards - draw_cards
        return frozenset(draw_cards)

    def is_game_end(self):
        return len(self.rem_cards) == 0 and len(self.table_cards) == 0