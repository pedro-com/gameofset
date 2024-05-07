from set_components.set_game import SETGame
from set_components.end_game import EndGame
from set_components.set_deck import SETDeck
from set_components.set_deck import combination_pairs
import set_components.mod_vector as mv
from card_draw.draw_set_structure import SETStructureDraw
from app.settings import *
def auto_play(set_game: SETDeck):
    print(list(set_game.all_intersets(set_game.table_cards)))
    while set_game.check_table():
        print(f'SETs in the deck: {list(set_game.table_sets())}')
        print(f'Drawn cards: {set_game.play_round(next(set_game.table_sets()))}')
        print()

n_attributes = 5
set_game = SETGame(4, n_attributes)
# print(set_game.all_intersets2([(0, 0, 0, 0), (1, 0, 0, 0), (2, 1, 0, 0), (2, 2, 0, 0)]))
# set_game.is_interset([(0, 0, 0, 0), (1, 0, 0, 0), (2, 1, 0, 0), (2, 2, 0, 0)])
# set_game.is_magic_square(mv.generate_mod_affine_space((0, 0, 0, 0), [(1, 0, 0, 0), (0, 1, 0, 0)], 3))
set_game.start_game()
# auto_play(set_game)
print(set_game.is_game_end())

# Draw table cards and SET
draw = SETStructureDraw(n_attribute_values=n_attributes, canvas_bg=(245, 235, 223, 255))
draw.custom_structure_draw(4, n_attributes, set_game.table_cards).show()
draw.custom_structure_draw(n_attributes, 1, next(set_game.table_sets())).show()

def linearize(elems):
    elem_out = []
    for elem in elems:
        elem_out.extend(elem)
    return elem_out
intersets = set_game.all_intersets(set_game.table_cards)
# for interset in intersets:
#     draw.custom_structure_draw(1, 1, (tuple(interset[0])[0],)).show()
#     card_join = linearize(interset[1])
#     draw.custom_structure_draw(2, int(len(card_join) / 2), card_join).show()

# draw.draw_elements(set_game.card_structure([(0, 0, 0, 0), (1, 0, 0, 1), (0, 1, 2, 0)])).show()
a = 0



# b = set_game.card_structure([(0, 0, 0, 0), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)])
# a = draw.draw_elements(b)
# a.show()
# end_game = EndGame(4, 3)
# end_game.start_game()
# auto_play(end_game)
# print(end_game.is_game_end())
# a = 0
