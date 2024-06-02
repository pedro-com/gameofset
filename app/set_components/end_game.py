from typing import Tuple
from .set_game import SETGame

from .game_settings import *


class EndGame(SETGame):
    """
    SETGame implements the logic for a solitary game of SET.
    - end_guess_score: The score gained if the hold card is guessed.
    - hold_card
    """
    def __init__(
        self,
        n_attributes: int,
        n_attribute_values: int,
        set_score: int = 300,
        end_guess_score: int = 500,
    ):
        super().__init__(n_attributes, n_attribute_values, set_score)
        self.end_guess_score = end_guess_score
        self.hold_card = None

    @property
    def max_score(self):
        return super().max_score + self.end_guess_score

    def start_game(self):
        """Start the game of SET and hold one card"""
        super().start_game()
        self.hold_card = next(card for card in self.rem_cards)
        self.rem_cards = self.rem_cards.difference((self.hold_card,))
        self.modify_game_state()

    def hold_card_remaining(self):
        return self.hold_card is not None

    def guess_hold_card(self, card_guess: Tuple[int]):
        if (
            not super().is_game_end() or card_guess != self.hold_card
        ):  # Check its the game end state from the game of SET
            self.add_score(-int(self.end_guess_score / 2))
            self.modify_game_state(message=NOT_HOLD)
            return False
        self.modify_game_state(message=IS_HOLD)
        self.add_score(self.end_guess_score)
        hold_card = self.hold_card
        self.table_cards = self.table_cards.union((hold_card,))
        self.hold_card = None
        return True
