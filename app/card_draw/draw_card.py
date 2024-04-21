from typing import Tuple
from PIL import Image, ImageDraw

ATTRIBUTE_TABLE = (
    (1, 2, 3, 4, 5), # Number of shapes
    ((255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (0, 255, 255, 255), (255, 0, 255, 255)), # Available colors
    ("circle", "squiggle", "diamond", "square", "triangle"), # Available shapes
    ("fill", "empty", "stripped_v", "circle_p", "stripped_h"), # Available patterns
)
TRANSPARENT = (0, 0, 0, 0)
CARD_WIDTH = 100
CARD_HEIGHT = 300
CARD_PADX = 20
CARD_PADY = 40
BD_WIDTH = 5

def get_value(card:Tuple[int], idx:int):
    '''Get all the values for a card (the card can have less attributes than the max)'''
    if idx >= len(card):
        return 0
    return card[idx]

class CardImageDraw:
    def __init__(self,
            resolution:int = 2,
            n_attribute_values:int = 3,
            card_bg:Tuple[int] = TRANSPARENT
        ):
        self.n_attribute_values = n_attribute_values
        self.fig_width = int(resolution*CARD_WIDTH)
        self.fig_height = int(resolution*CARD_HEIGHT)
        self.padx = int(resolution*CARD_PADX)
        self.pady = int(resolution*CARD_PADY)
        self.bd_width = int(resolution*BD_WIDTH)
        self.def_card_bg = card_bg
        self.canvas_width = (self.fig_width + self.padx) * self.n_attribute_values
        self.canvas_height = self.fig_height + self.pady
    
    @property
    def canvas_center(self):
        '''Center of the card to be painted (the canvas is all the card draw space)'''
        return (int(self.canvas_width // 2), int(self.canvas_height // 2))
    
    @staticmethod
    def card_attributes(card: Tuple[int]):
        return {
            "n_figures": ATTRIBUTE_TABLE[0][get_value(card, 0)],
            "color": ATTRIBUTE_TABLE[1][get_value(card, 1)],
            "shape": ATTRIBUTE_TABLE[2][get_value(card, 2)],
            "pattern": ATTRIBUTE_TABLE[3][get_value(card, 3)]
        }
    
    def _shape_centers(self, n_shapes:int):
        '''Centers for all the shapes in the card. Takes into consideration the padding and the number of shapes'''
        step = self.fig_width + self.padx
        if n_shapes % 2 == 0:
            x_center = self.canvas_center[0] - int(step // 2)
            c0_x = x_center - (int(n_shapes // 2) - 1)*step
        else:
            x_center = self.canvas_center[0]
            c0_x = x_center - int(n_shapes // 2)*step
        return [(c0_x + k*step, self.canvas_center[1]) for k in range(n_shapes)]
    
    def _draw_shape(self, card:Image, center:Tuple[int], shape_id:str, color:Tuple[int], fill:bool):
        '''Function to draw the shape specified by shape_id, knowing its center, color and if it has to be filled'''
        w_half = self.fig_width // 2
        h_half = self.fig_height // 2
        x, y = center
        draw = ImageDraw.Draw(card, 'RGBA')
        if shape_id == 'diamond':
            draw.polygon(
                ((x - w_half, y), (x, y - h_half), (x + w_half, y), (x, y + h_half)),
                fill = color if fill else None,
                outline = color,
                width = self.bd_width
            )
        elif shape_id == 'circle':
            draw.ellipse(
                (x - w_half, y - h_half, x + w_half, y + h_half),
                fill = color if fill else None,
                outline = color,
                width = self.bd_width
            )
        elif shape_id == 'square':
            draw.rectangle(
                (x - w_half, y - h_half, x + w_half, y + h_half),
                fill = color if fill else None,
                outline = color,
                width = self.bd_width
            )
        elif shape_id == 'triangle':
            draw.polygon(
                ((x - w_half, y), (x + w_half, y - h_half), (x + w_half, y + h_half)),
                fill = color if fill else None,
                outline = color,
                width = self.bd_width
            )
        elif shape_id == 'squiggle':
            w_fourth = w_half // 2
            # TOP + Width correction
            draw.arc(
                (x - 2*w_half - w_fourth + self.bd_width - 1, y - h_half, x + w_fourth + self.bd_width - 1, y + h_half),
                start = 270,
                end = 0,
                fill = color,
                width = self.bd_width
            )
            draw.arc(
                (x - w_half - w_fourth + self.bd_width - 1, y - h_half, x - w_fourth + self.bd_width- 1, y + h_half),
                start = 270,
                end = 0,
                fill = color,
                width = self.bd_width
            )
            # BOTTOM
            draw.arc(
                (x - w_fourth, y - h_half, x + 2*w_half + w_fourth, y + h_half),
                start = 90,
                end = 180,
                fill = color,
                width = self.bd_width
            )
            draw.arc(
                (x + w_fourth, y - h_half, x + w_half + w_fourth, y + h_half),
                start = 90,
                end = 180,
                fill = color,
                width = self.bd_width
            )
            if fill:
                ImageDraw.floodfill(card, center, color)
    
    def _draw_shapes(self, card:Image, n_shapes:int, shape_id:str, color:Tuple[int], fill:bool = True):
        shape_centers = self._shape_centers(n_shapes)
        for center in shape_centers:
            self._draw_shape(card, center, shape_id, color, fill)
    
    def _draw_strip_pattern(self, card: Image, pattern:str, color:Tuple[int]):
        draw = ImageDraw.Draw(card, 'RGBA')
        # Draw horizontal lines
        step = self.bd_width*4
        if pattern == 'stripped_h':
            for i in range(int(self.canvas_height/step)):
                draw.line(
                    ((0, step*i), (self.canvas_width, step*i)),
                    fill = color,
                    width = self.bd_width
                )
        elif pattern == 'stripped_v':
            for i in range(int(self.canvas_width/step)):
                draw.line(
                    ((step*i, 0), (step*i, self.canvas_height)),
                    fill = color,
                    width = self.bd_width
                )
    
    def _padding_centers(self, n_shapes:int):
        step = self.fig_width + self.padx
        n_center = n_shapes + 1
        if n_center % 2 == 0:
            x_center = self.canvas_center[0] - int(step // 2)
            c0_x = x_center - int(n_shapes // 2)*step
        else:
            x_center = self.canvas_center[0]
            c0_x = x_center - int(n_center // 2)*step
        return [c0_x + k*step for k in range(n_center)]

    def _draw_cleanup_strip_pattern(self, card: Image, n_shapes:int, pattern:str, color:Tuple[int]):
        draw = ImageDraw.Draw(card, 'RGBA')
        if pattern == 'stripped_h':
            for c_xi in self._padding_centers(n_shapes):
                draw.line(
                    ((c_xi, 0), (c_xi, self.canvas_height)),
                    fill = color,
                    width = self.bd_width
                )
        elif pattern == 'stripped_v':
            draw.line(
                ((0, 0), (self.canvas_width, 0)),
                fill = color,
                width = self.bd_width
            )
            draw.line(
                ((0, self.canvas_height), (self.canvas_width, self.canvas_height)),
                fill = color,
                width = self.bd_width
            )

    def _draw_center_circles(self, card:Image, n_shapes, color:Tuple[int]):
        draw = ImageDraw.Draw(card, 'RGBA')
        w_half = int(self.fig_width // 4)
        for x, y in self._shape_centers(n_shapes):
            draw.ellipse(
                (x - w_half, y - w_half, x + w_half, y + w_half + 1),
                fill = color,
                outline = color,
                width = self.bd_width
            )

    def draw_card(self, card:Tuple[int], card_bg:Tuple[int] = None):
        attributes = self.card_attributes(card)
        card_image = Image.new('RGBA',
            size = (self.canvas_width, self.canvas_height),
            color = card_bg or self.def_card_bg
        )
        if attributes["pattern"] in ("fill", "empty"):
            fill = attributes["pattern"] == "fill"
        elif attributes["pattern"] in ("stripped_h", "stripped_v"):
            self._draw_strip_pattern(card_image,
                pattern = attributes["pattern"],
                color = attributes["color"]
            )
            self._draw_cleanup_strip_pattern(card_image,
                n_shapes = attributes["n_figures"],
                pattern = attributes["pattern"],
                color = attributes["color"]
            )
            self._draw_shapes(card_image,
                n_shapes=attributes["n_figures"],
                shape_id=attributes["shape"],
                color=(255, 255, 255, 255),
                fill=False
            )
            ImageDraw.floodfill(card_image, (0, 0), card_bg or TRANSPARENT)
            fill = False
        elif attributes["pattern"] in ("circle_p"):
            self._draw_center_circles(card_image,
                n_shapes = attributes["n_figures"],
                color=attributes["color"]
            )
            fill = False
        self._draw_shapes(card_image,
            n_shapes=attributes["n_figures"],
            shape_id=attributes["shape"],
            color=attributes["color"],
            fill=fill
        )
        return card_image
    
    async def adraw_card(self, card:Tuple[int], card_bg:Tuple[int] = None):
        return self.draw_card(card, card_bg)

if __name__ == '__main__':
    set_images = CardImageDraw(resolution = 2, n_attribute_values = 5)
    card_image = set_images.draw_card((0, 3, 3, 4), (255, 255, 255, 255))
    card_image.show()
