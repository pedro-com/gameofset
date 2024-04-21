from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import FrozenSet, Tuple, Iterable
from itertools import combinations
from random import sample

from tkinter import IntVar, StringVar

from settings import *
from . import mod_vector as mv

def in_constraint(p, p_min, p_max, include_min = True, include_max = True):
    return (p > p_min  or (include_min and p == p_min)) and (p < p_max or (include_max and p == p_max))

def combination_pairs(elems:Iterable[int], n:int):
    elems = frozenset(elems)
    return frozenset(frozenset((c, tuple(elems.difference(c))))
        for c in combinations(elems, n)
    )

@dataclass
class SETDeck(ABC):
    '''
    SETDeck is a deck of cards for a game of SET. Each SET is represented via a vector, such that each dimension
    is one attribute and their value is the number, color, shade and shape of the card.
        - n_attributes: Number of attributes of each card (1 <= n <= 4)
        - n_attribute_values: Number of attribute values, can only be prime numbers (3, 5 are the only ones implemented)
        - set_score: The score per SET
        - deck_cards: The whole SET deck
        - table_cards: The cards on the table
        - rem_cards: The cards remaining in the deck
        - table_size: Max number of cards in the table
        - score: Actual score
        - max_score: Maximum possible score
    '''
    n_attributes: int
    n_attribute_values: int
    # Game attributes
    deck_cards: FrozenSet[Tuple[int]] = field(init = False)
    table_cards: FrozenSet[Tuple[int]] = field(init = False)
    rem_cards: FrozenSet[Tuple[int]] = field(init = False)
    # Game state
    score: IntVar = field(init = False)
    game_state: StringVar = field(init = False)
    def __post_init__(self):
        if not in_constraint(self.n_attributes, 1, 4) or self.n_attribute_values not in (3, 5):
            raise ValueError(self.n_attributes, self.n_attribute_values)
        # Deck variables init
        self.deck_cards = self.generate_deck()
        self.table_cards = frozenset()
        self.rem_cards = frozenset()
        # Game state variables
        self.score = None
        self.game_state = None
    
    @property
    def table_state(self):
        '''Represents the number of cards remaining on the table and the deck.'''
        total_cards = len(self.deck_cards)
        return f'{total_cards - len(self.rem_cards | self.table_cards)}/{total_cards}'
    
    def generate_deck(self):
        '''Generate the whole deck'''
        all_points = mv.simple_affine_space_gen(self.n_attributes, self.n_attribute_values)
        return frozenset(all_points)
    
    def set_score_tracker(self, score: IntVar):
        self.score = score
    
    def set_game_state(self, game_state: StringVar):
        self.game_state = game_state
    
    def add_score(self, score_to_add: int):
        if self.score:
            self.score.set(self.score.get() + score_to_add)
    
    def modify_game_state(self, message:str= None, timer_end:bool = False):
        if not self.game_state:
            return
        if timer_end:
            self.game_state.set(WIN_GAME if self.is_game_end() else LOSE_GAME)
            return
        if self.is_game_end(): # Just in Case
            self.game_state.set(WIN_GAME)
            return
        total_cards = len(self.deck_cards)
        message_out = message + CARDS_REMAINING if message else CARDS_REMAINING
        self.game_state.set(message_out % (total_cards - len(self.rem_cards | self.table_cards), total_cards))
    
    def complete_set(self, c1: Tuple[int], c2:Tuple[int]):
        '''Function to obtain the remaining cards to complete a SET from 2 cards'''
        v = mv.mod_sub(c2, c1, self.n_attribute_values)
        vk = (mv.mod_prod(v, k, self.n_attribute_values) for k in range(1, self.n_attribute_values - 1))
        return frozenset(mv.mod_add(c2, vi, self.n_attribute_values) for vi in vk)

    def random_set(self):
        '''Obtains a random SET from the deck'''
        c1, c2 = sample(tuple(self.deck_cards), 2)
        return self.complete_set(c1, c2).union((c1, c2))
    
    def is_set(self, cards: Iterable[Tuple[int]]):
        '''Check if a list of cards is a set''' # TODO checks this works
        if len(cards) != self.n_attribute_values or not mv.is_zero(mv.mod_add_mult(cards, self.n_attribute_values)):
            return False
        c1, c2 = tuple(cards)[0:2]
        check_cards = self.complete_set(c1, c2).union((c1, c2))
        return check_cards == frozenset(cards)
    
    def is_interset(self, cards: Iterable[Tuple[int]]):
        '''Check if a list of cards is an interset (2 intersecting SETs without the intersection card)'''
        if not len(cards) == self.n_attribute_values*2 - 2:
            return False
        return any(self.complete_set(*cards1) == self.complete_set(*cards2)
            for cards1, cards2 in combination_pairs(cards, 2)
        )
    
    def is_comet(self, cards:Iterable[Tuple[int]]):
        if not len(cards) == self.n_attribute_values*2 - 2:
            return False
        contains_set = any(self.is_set(card_comb) for card_comb in combinations(cards, 3))
        return contains_set or self.is_interset(cards)
    
    def is_magic_square(self, cards:Iterable[Tuple[int]]):
        '''Also known as is_planet, checks if a list of cards is a plane (also known as a magic square)'''
        if not len(cards) == self.n_attribute_values * self.n_attribute_values:
            return False
        cards = frozenset(cards)
        test_cards = sample(tuple(cards), 2)
        vector1 = mv.mod_sub(test_cards[0], test_cards[1], self.n_attribute_values)
        gen_plane = None
        for p in cards.difference(test_cards):
            vector2 = mv.mod_sub(test_cards[0], p, self.n_attribute_values)
            if mv.is_linear_indepent((vector1, vector2)):
                gen_plane = mv.generate_mod_affine_space(test_cards[0], (vector1, vector2), self.n_attribute_values)
                break
        return gen_plane and frozenset(gen_plane) == cards
    
    def all_sets(self, cards:Iterable[Tuple[int]]):
        card_combinations = combinations(cards, self.n_attribute_values)
        return (cards for cards in card_combinations if self.is_set(cards))
    
    def _possible_intersets(self, cards:Iterable[Tuple[int]]):
        cards = frozenset(cards)
        for card_comb in combinations(cards, 2):
            card_set = self.complete_set(*card_comb).union(card_comb)
            card_interset = cards & card_set
            if len(card_interset) == self.n_attribute_values - 1:
                yield (card_set - card_interset, card_interset)
    
    def all_intersets(self, cards:Iterable[Tuple[int]]):
        intersets = {}
        for int_card, interset in self._possible_intersets(cards):
            if int_card not in intersets:
                intersets[int_card] = [interset]
            else:
                intersets[int_card].append(interset)
        return ((int_card, interset_l) for int_card, interset_l in intersets.items() if len(interset_l) > 1)
    
    def card_structure(self, cards:Iterable[Tuple[int]]):
        '''
        Returns the subyacent card structure in a list of cards (cards in this case is an affine reference).
        This function is meant to be used with the package card_draw, to draw set structures.
        '''
        return mv.generate_affine_space_structure(cards, self.n_attribute_values)
    
    @abstractmethod
    def is_valid_selection(self, num_cards:int):
        '''Returns whether the number of cards passed is valid for a round of the game'''

    @abstractmethod
    def start_game(self):
        '''Start or restart the game that the class represents.'''
    
    @abstractmethod
    def play_round(self, cards:Tuple[int]):
        '''
        Play a round of the game. Returns the cards that are drawn from the deck if successfull,
        else returns an empty set
        '''
    
    @abstractmethod
    def is_game_end(self):
        '''Check if the game has ended. Each game has a different game end condition'''
    
'''
    Variation of all intersets (DEPRECATED)
    def all_intersets(self, cards:Iterable[Tuple[int]]):
        cards = frozenset(cards)
        card_sets = (self.complete_set(*card_comb).union(card_comb)
            for card_comb in combinations(cards, 2)
        )
        set_intersets = ((card_set, card_set & cards) for card_set in card_sets)
        
        valid_sets = [(card_set - set_interset, set_interset)
            for card_set, set_interset in set_intersets if len(set_interset) == self.n_attribute_values - 1
        ]
        
        intersets = {}
        for set1, set2 in combinations(valid_sets, 2):
            set_intersection = set1 & set2
            if len(set_intersection) != 1:
                continue
            to_add = (set1 - set_intersection, set2 - set_intersection)
            if set_intersection not in intersets:
                intersets[set_intersection] = frozenset(to_add)
            else:
                intersets[set_intersection] = intersets[set_intersection].union(to_add)
        return intersets
'''