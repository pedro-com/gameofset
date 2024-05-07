# Attribute values
# Table to transform number values to their card representation
ATTRIBUTE_ORDER = ("n_shapes", "color", "shape", "shape_fill")
ATTRIBUTE_VALUES = (
    (1, 2, 3, 4, 5), # Number of shapes
    ((255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (0, 255, 255, 255), (255, 0, 255, 255)), # Available colors
    ("circle", "squiggle", "diamond", "square", "triangle"), # Available shapes
    ("fill", "empty", "stripped_v", "circle_p", "stripped_h"), # Available patterns
)

# Option selection for the card Picker
POS_VALUES = (0, 1, 2, 3, 4)
CARD_OPTIONS = {
    "n_shapes": ("Nº Shapes", ("One", "Two", "Three", "Four", "Five"), POS_VALUES, 0),
    "color": ("Color", ("Red", "Green", "Blue", "Cian", "Magenta"), POS_VALUES, 0),
    "shape": ("Shape", ("Circle", "Squiggle", "Diamond", "Square", "Triangle"), POS_VALUES, 0),
    "shape_fill": ("Fill", ("Fill", "Empty", "Vertical Strip", "Dotted", "Horizontal Strip"), POS_VALUES, 0)
}

# Card draw settings
TRANSPARENT = (0, 0, 0, 0)
CARD_WIDTH = 100
CARD_HEIGHT = 300
CARD_PADX = 20
CARD_PADY = 40
BD_WIDTH = 5

# Card Structure
WHITE = (255, 255, 255, 255)
ELEMENT_WIDTH = 300
ELEMENT_HEIGHT = 200
ELEMENT_PADX = 20
ELEMENT_PADY = 20
BD_WIDTH = 5
