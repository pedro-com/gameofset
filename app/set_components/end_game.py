from typing import Tuple
from .set_game import SETGame

from settings import *
class EndGame(SETGame):
    def __init__(self, n_attributes: int, n_attribute_values: int, set_score: int = 300, end_guess_score:int = 500):
        super().__init__(n_attributes, n_attribute_values, set_score)
        self.end_guess_score = end_guess_score
        self.hold_card = None
    
    @property
    def max_score(self):
        return super().max_score() + self.end_guess_score
    
    def start_game(self):
        '''Start the game of SET and hold one card'''
        super().start_game()
        self.hold_card = next(card for card in self.rem_cards)
        self.rem_cards = self.rem_cards.difference((self.hold_card,))
        self.modify_game_state()
    
    def is_game_end(self):
        return super().is_game_end() and not self.hold_card
    
    def guess_hold_card(self, card_guess:Tuple[int]):
        if not super().is_game_end() or card_guess != self.hold_card: # Check its the game end state from the game of SET
            self.add_score(-int(self.end_guess_score / 2))
            self.modify_game_state(message=NOT_HOLD)
            return False
        self.modify_game_state(message=IS_HOLD)
        self.add_score(self.end_guess_score)
        self.hold_card = None
        return True

    