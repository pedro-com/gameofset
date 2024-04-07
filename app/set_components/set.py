from dataclasses import dataclass, field
from typing import FrozenSet, Tuple
from set_components.mod_vector import *
from random import sample
ATTRIBUTE_TABLE = (
    (1, 2, 3, 4, 5), # Number of shapes
    ("red", "green", "blue", "yellow", "magenta"), # Available colors
    ("fill", "empty", "striped_v", "circle_p", "striped_h"),
    ("circle", "squiggle", "diamond", "square", "triangle") # Available shapes
)
def in_constraint(p, p_min, p_max, include_min = True, include_max = True):
    return (p > p_min  or (include_min and p == p_min)) and (p < p_max or (include_max and p == p_max))

@dataclass
class SETDeck:
    num_attributes: int
    num_attribute_values: int
    set_score: int = 300
    deck: FrozenSet[Tuple[int]] = field(init = False)
    table: Tuple[Tuple[int]] = field(init = False)
    table_size: Tuple[Tuple[int]]
    remaining: FrozenSet[Tuple[int]] = field(init = False)
    score:int = field(init = False)
    max_score:int = field(init = False)

    def __post_init__(self):
        if not in_constraint(self.num_attributes, 1, 4) or self.num_attribute_values in (2, 3, 5):
            raise ValueError(self.num_attributes, self.num_attribute_values)
        self.deck = self.generate_deck()
        self.table_size = 3*self.num_attribute_values
        self.max_score = int(len(self.deck) // 3) * self.set_score
        self.start_game()
    
    def generate_deck(self):
        all_points = affine_space_points(self.num_attributes, self.num_attribute_values)
        return frozenset(all_points)
    
    def start_game(self):
        # Include at least a SET in the random selection
        c1, c2 = sample(self.deck, 2)
        c3 = mod_add(c1, c2)
        remaining = self.deck.copy() - (c1, c2, c3)
        rest_table = sample(remaining, 6)