from set_components import SETGame, EndGame, SETDeck
from card_draw.set_structure_draw import SETStructureDraw
from settings import *


def auto_play(set_game: SETDeck):
    print(list(set_game.all_intersets(set_game.table_cards)))
    while set_game.check_table():
        print(f"SETs in the deck: {list(set_game.table_sets())}")
        print(f"Drawn cards: {set_game.play_round(next(set_game.table_sets()))}")
        print()

def linearize(elems):
    elem_out = []
    for elem in elems:
        elem_out.extend(elem)
    return elem_out

def show_intersets(draw: SETStructureDraw, intersets):
    interset_type_shown = set()
    for interset in intersets:
        if len(interset[1]) in interset_type_shown:
            continue
        interset_type_shown.add(len(interset[1]))
        draw.draw_element_structure(1, 1, (tuple(interset[0])[0],)).show()
        card_join = linearize(interset[1])
        draw.draw_element_structure(2, int(len(card_join) / 2), card_join).show()

n_attributes = 5
set_game = SETGame(4, n_attributes)
set_game.start_game()
# Draw table cards and SET
draw = SETStructureDraw(n_attribute_values=n_attributes, resolution=4, with_border=True)
draw.draw_card_list(((3, 0, 0, 4),), with_border=True)
a = 0
# Intro / Uncomment to see the structures
# draw.draw_element_structure(4, n_attributes, set_game.table_cards).show()
# draw.draw_element_structure(n_attributes, 1, set_game.table_sets()[0]).show()

# Conceptos
intersets = set_game.all_intersets(set_game.table_cards)
# show_intersets(draw, intersets)

# Magic Square
# draw.draw_elements(set_game.card_structure([(0, 0, 0, 0), (1, 0, 0, 1), (0, 1, 2, 0)])).show()

# Parallel SETs
set1 = [(0, 0, 0, 0), (2, 0, 1, 0)]
set2 = [(1, 1, 1, 1), (0, 1, 2, 1)]
parallel = [
    set_game.complete_set(set1[0], set1[1]).union(set1),
    set_game.complete_set(set2[0], set2[1]).union(set2)
]
# draw.draw_element_structure(n_attributes, 2, linearize(parallel)).show()

# draw.draw_element_structure(n_attributes, 1, [(0, 0, 0, 0), (2, 0, 1, 0), (1, 2, 2, 2)]).show()

set_test = [(2, 1, 2, 0), (1, 2, 0, 1)]
# draw.draw_element_structure(2, 1, set_test).show()
# draw.draw_element_structure(1, 1, tuple(set_game.complete_set(set_test[0], set_test[1]))).show()

# Card Structure
card_structure = set_game.card_structure([(0, 1, 2, 1), (0, 1, 0, 0), (0, 0, 0, 0), (0, 0, 1, 1), (1, 1, 1, 1)])

draw.draw_elements(card_structure).show()
# a.show()
# end_game = EndGame(4, 3)
# end_game.start_game()
# auto_play(end_game)
# print(end_game.is_game_end())
# a = 0
