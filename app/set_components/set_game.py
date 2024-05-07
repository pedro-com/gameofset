from typing import Tuple, Iterable
from random import sample
from itertools import combinations

from .set_deck import SETDeck
from .game_settings import *


class SETGame(SETDeck):
    def __init__(
        self, n_attributes: int, n_attribute_values: int, set_score: int = 300
    ):
        super().__init__(n_attributes, n_attribute_values)
        self.set_score = set_score

    @property
    def max_score(self):
        return int(len(self.deck_cards) // self.n_attribute_values) * self.set_score

    def is_valid_selection(self, num_cards: int):
        return num_cards == self.n_attribute_values

    def start_game(self):
        """Start the game of SET"""
        # Include at least a SET in the random selection
        rand_set = self.random_set()
        remaining = self.deck_cards.copy() - rand_set
        rest_table = sample(tuple(remaining), self.table_size - len(rand_set))
        self.table_cards = rand_set.union(rest_table)
        self.rem_cards = remaining - self.table_cards
        if self.score:
            self.score.set(0)
        self.modify_game_state()

    def table_sets(self):
        """Function to return the SETs on the table"""
        # card_combinations = combinations(self.table_cards, self.n_attribute_values)
        # return [cards for cards in card_combinations if self.is_set(cards)]
        return self.all_sets(self.table_cards)

    def check_table(self):
        """Checks if the table has at least one SET"""
        # card_combinations = combinations(self.table_cards, self.n_attribute_values)
        # return any(self.is_set(cards) for cards in card_combinations)
        return any(True for _ in self.table_sets())

    def _refill_table(self):
        """
        Refill the cards in the table from the remaining cards in the deck. Checks if the cards in the table have
        at least one SET. If not, tries to complete at least one SET in the refill of the table.
        """
        to_refill = self.table_size - len(self.table_cards)
        if to_refill == 0:
            return frozenset()
        if len(self.rem_cards) <= to_refill:  # If there are not enough remaining cards
            refill_cards = self.rem_cards
            self.rem_cards = frozenset()
            self.table_cards = self.table_cards | refill_cards
            return refill_cards
        if self.check_table():  # If there is a SET already in the table
            refill_cards = frozenset(sample(tuple(self.rem_cards), to_refill))
            self.rem_cards = self.rem_cards - refill_cards
            self.table_cards = self.table_cards | refill_cards
            return refill_cards
        # If there are no SETs in the table
        available_cards = self.rem_cards | self.table_cards
        for c1, c2 in combinations(available_cards, 2):
            pos_set = self.complete_set(c1, c2).union((c1, c2))
            if pos_set <= available_cards:
                refill_cards = self.rem_cards & pos_set
                self.rem_cards = self.rem_cards - refill_cards
                break
        # Add rest of the draw
        refill_cards = refill_cards.union(
            sample(tuple(self.rem_cards), to_refill - len(refill_cards))
        )
        self.rem_cards = self.rem_cards - refill_cards
        self.table_cards = self.table_cards | refill_cards
        return refill_cards

    def play_round(self, cards: Iterable[Tuple[int]]):
        """
        Check if the selected cards are a SET and in the table. Returns the newly drawn cards.
        Returns None if the passed cards are not a SET
        """
        cards = frozenset(cards)
        if not self.is_set(cards) or not (cards <= self.table_cards):
            self.modify_game_state(message=NOT_SET)
            self.add_score(-int(self.set_score / 2))
            return None
        self.table_cards = self.table_cards - cards
        self.add_score(self.set_score)
        refill_cards = self._refill_table()
        self.modify_game_state(message=IS_SET)
        return refill_cards

    def is_game_end(self):
        return len(self.rem_cards) == 0 and not self.check_table()
