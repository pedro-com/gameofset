from random import sample
from typing import Tuple

from .set_deck import SETDeck
from .game_settings import *

class IntersetGame(SETDeck):
    def __init__(self, n_attributes: int, n_attribute_values: int, interset_score: int = 400):
        super().__init__(n_attributes, n_attribute_values)
        self.interset_score = interset_score
        
    @property
    def max_score(self):
        return int(len(self.deck_cards) // (self.n_attribute_values - 1))*self.interset_score
    
    def check_table(self):
        '''Checks the table for intersets, returns True if there is at least one'''
        return len(self.table_cards) == 0 or len(self.all_intersets(self.table_cards)) >= 1

    def is_valid_selection(self, num_cards: int):
        return num_cards > self.n_attribute_values - 1 and num_cards % (self.n_attribute_values - 1) == 0

    def start_game(self):
        '''Start the game of Interset'''
        self.table_cards = frozenset(sample(tuple(self.deck_cards), self.table_size))
        self.rem_cards = self.deck_cards - self.table_cards
        if self.score:
            self.score.set(0)
        self.modify_game_state()
        
    def play_round(self, cards: Tuple[int]):
        '''
        Play a round of the Game of interset, where the cards must be either a single interset,
        or a double or a triple, with the same intersection card.
        '''
        intersets = self.all_intersets(cards) if cards <= self.table_cards else None
        if intersets is None or len(intersets) != 1:
            self.modify_game_state(message=NOT_INTERSET)
            self.add_score(- int(self.interset_score / 2))
            return None
        interset = intersets[0]
        self.add_score(len(interset[1])*self.interset_score)
        refill_cards = min(len(self.rem_cards), len(cards))
        new_cards = frozenset(sample(tuple(self.rem_cards), refill_cards))
        self.rem_cards = self.rem_cards - new_cards
        self.table_cards = self.table_cards.difference(cards) | new_cards
        self.modify_game_state(message=IS_INTERSET)
        return new_cards
    
    def is_game_end(self):
        return len(self.rem_cards) == 0 and not self.check_table()