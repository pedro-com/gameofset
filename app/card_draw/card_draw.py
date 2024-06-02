from typing import Tuple
from PIL import Image, ImageDraw

from .draw_settings import *


def get_value(card: Tuple[int], idx: int):
    """Get all the values for a card (the card can have less attributes than the max)"""
    if idx >= len(card):
        return 0
    return card[idx]


class CardImageDraw:
    """
    Class to draw card images with specified attributes.

    - resolution : The resolution multiplier for the card dimensions.
    - n_attribute_values : Number of different attribute values for the card.
    - card_bg: Background color of the card.
    - card_border: Color of the card border.
    """
    def __init__(
        self,
        resolution: int = 2,
        n_attribute_values: int = 3,
        card_bg: Tuple[int] = TRANSPARENT,
        card_border: Tuple[int] = BORDER_COLOR
    ):
        self.n_attribute_values = n_attribute_values
        self.fig_width = int(resolution * CARD_WIDTH)
        self.fig_height = int(resolution * CARD_HEIGHT)
        self.padx = int(resolution * CARD_PADX)
        self.pady = int(resolution * CARD_PADY)
        self.bd_width = int(resolution * BD_WIDTH)
        self.card_bg = card_bg
        self.card_border = card_border
        self.canvas_width = (self.fig_width + self.padx) * n_attribute_values
        self.canvas_height = self.fig_height + self.pady

    @property
    def canvas_center(self):
        """Center of the card to be painted (the canvas is all the card draw space)"""
        return (int(self.canvas_width // 2), int(self.canvas_height // 2))

    def _shape_centers(self, n_shapes: int):
        """Centers for all the shapes in the card. Takes into consideration the padding and the number of shapes"""
        step = self.fig_width + self.padx
        if n_shapes % 2 == 0:
            x_center = self.canvas_center[0] - int(step // 2)
            c0_x = x_center - (int(n_shapes // 2) - 1) * step
        else:
            x_center = self.canvas_center[0]
            c0_x = x_center - int(n_shapes // 2) * step
        return [(c0_x + k * step, self.canvas_center[1]) for k in range(n_shapes)]

    def _padding_centers(self, n_shapes: int):
        """Centers for padding in the card layout."""
        step = self.fig_width + self.padx
        n_center = n_shapes + 1
        if n_center % 2 == 0:
            x_center = self.canvas_center[0] - int(step // 2)
            c0_x = x_center - int(n_shapes // 2) * step
        else:
            x_center = self.canvas_center[0]
            c0_x = x_center - int(n_center // 2) * step
        return [c0_x + k * step for k in range(n_center)]

    def _draw_shape(
        self,
        card: Image,
        center: Tuple[int],
        shape_id: str,
        color: Tuple[int],
        fill: bool,
    ):
        """Function to draw the shape specified by shape_id, knowing its center, color and if it has to be filled"""
        w_half = self.fig_width // 2
        h_half = self.fig_height // 2
        x, y = center
        draw = ImageDraw.Draw(card, "RGBA")
        if shape_id == "diamond":
            draw.polygon(
                ((x - w_half, y), (x, y - h_half), (x + w_half, y), (x, y + h_half)),
                fill=color if fill else None,
                outline=color,
                width=self.bd_width,
            )
        elif shape_id == "circle":
            draw.ellipse(
                (x - w_half, y - h_half, x + w_half, y + h_half),
                fill=color if fill else None,
                outline=color,
                width=self.bd_width,
            )
        elif shape_id == "square":
            draw.rectangle(
                (x - w_half, y - h_half, x + w_half, y + h_half),
                fill=color if fill else None,
                outline=color,
                width=self.bd_width,
            )
        elif shape_id == "triangle":
            draw.polygon(
                ((x - w_half, y), (x + w_half, y - h_half), (x + w_half, y + h_half)),
                fill=color if fill else None,
                outline=color,
                width=self.bd_width,
            )
        elif shape_id == "squiggle":
            w_fourth = w_half // 2
            # TOP + Width correction
            draw.arc(
                (
                    x - 2 * w_half - w_fourth + self.bd_width - 1,
                    y - h_half,
                    x + w_fourth + self.bd_width - 1,
                    y + h_half,
                ),
                start=270,
                end=0,
                fill=color,
                width=self.bd_width,
            )
            draw.arc(
                (
                    x - w_half - w_fourth + self.bd_width - 1,
                    y - h_half,
                    x - w_fourth + self.bd_width - 1,
                    y + h_half,
                ),
                start=270,
                end=0,
                fill=color,
                width=self.bd_width,
            )
            # BOTTOM
            draw.arc(
                (x - w_fourth, y - h_half, x + 2 * w_half + w_fourth, y + h_half),
                start=90,
                end=180,
                fill=color,
                width=self.bd_width,
            )
            draw.arc(
                (x + w_fourth, y - h_half, x + w_half + w_fourth, y + h_half),
                start=90,
                end=180,
                fill=color,
                width=self.bd_width,
            )
            if fill:
                ImageDraw.floodfill(card, center, color)

    def _draw_shapes(
        self,
        card: Image,
        n_shapes: int,
        shape_id: str,
        color: Tuple[int],
        fill: bool = True,
    ):
        """Draw the specified shapes on the card."""
        shape_centers = self._shape_centers(n_shapes)
        for center in shape_centers:
            self._draw_shape(card, center, shape_id, color, fill)

    def _draw_strip_pattern(self, card: Image, pattern: str, color: Tuple[int]):
        """Draw a striped pattern on the card."""
        draw = ImageDraw.Draw(card, "RGBA")
        # Draw horizontal lines
        step = self.bd_width * 4
        if pattern == "stripped_h":
            for i in range(int(self.canvas_height / step)):
                draw.line(
                    ((0, step * i), (self.canvas_width, step * i)),
                    fill=color,
                    width=self.bd_width,
                )
        elif pattern == "stripped_v":
            for i in range(int(self.canvas_width / step)):
                draw.line(
                    ((step * i, 0), (step * i, self.canvas_height)),
                    fill=color,
                    width=self.bd_width,
                )

    def _draw_center_circles(self, card: Image, n_shapes, color: Tuple[int]):
        """Draw center circles on the card, for the circle pattern."""
        draw = ImageDraw.Draw(card, "RGBA")
        w_half = int(self.fig_width // 4)
        for x, y in self._shape_centers(n_shapes):
            draw.ellipse(
                (x - w_half, y - w_half, x + w_half, y + w_half + 1),
                fill=color,
                outline=color,
                width=self.bd_width,
            )

    def _draw_cleanup_strip_pattern(
        self, card: Image, n_shapes: int, pattern: str, color: Tuple[int]
    ):
        """Clean up the striped pattern in the card."""
        draw = ImageDraw.Draw(card, "RGBA")
        if pattern == "stripped_h":
            for c_xi in self._padding_centers(n_shapes):
                draw.line(
                    ((c_xi, 0), (c_xi, self.canvas_height)),
                    fill=color,
                    width=self.bd_width,
                )
        elif pattern == "stripped_v":
            draw.line(((0, 0), (self.canvas_width, 0)), fill=color, width=self.bd_width)
            draw.line(
                ((0, self.canvas_height), (self.canvas_width, self.canvas_height)),
                fill=color,
                width=self.bd_width,
            )
    
    def _draw_border(self, card_image:Image):
        """Draw the border around the card."""
        draw = ImageDraw.Draw(card_image, "RGBA")
        draw.rounded_rectangle(
            (0, 0, self.canvas_width, self.canvas_height),
            outline=self.card_border,
            width=int(0.75*self.bd_width),
            radius=45
        )

    @staticmethod
    def card_attributes(card: Tuple[int]):
        """Get the attributes of the card."""
        return {
            att_id: ATTRIBUTE_VALUES[idx][get_value(card, idx)]
            for idx, att_id in enumerate(ATTRIBUTE_ORDER)
        }

    def draw_card(self, card: Tuple[int], card_bg: Tuple[int] = None, with_border: bool = False):
        """Draw the given card, with the passed card background color and with or without a border."""
        attributes = self.card_attributes(card)
        card_image = Image.new(
            "RGBA",
            size=(self.canvas_width, self.canvas_height),
            color=card_bg or self.card_bg,
        )
        if attributes["shape_fill"] in ("fill", "empty"):
            fill = attributes["shape_fill"] == "fill"
        elif attributes["shape_fill"] in ("stripped_h", "stripped_v"):
            self._draw_strip_pattern(
                card_image, pattern=attributes["shape_fill"], color=attributes["color"]
            )
            self._draw_cleanup_strip_pattern(
                card_image,
                n_shapes=attributes["n_shapes"],
                pattern=attributes["shape_fill"],
                color=attributes["color"],
            )
            self._draw_shapes(
                card_image,
                n_shapes=attributes["n_shapes"],
                shape_id=attributes["shape"],
                color=(255, 255, 255, 255),
                fill=False,
            )
            ImageDraw.floodfill(card_image, (0, 0), card_bg or TRANSPARENT)
            fill = False
        elif attributes["shape_fill"] in ("circle_p"):
            self._draw_center_circles(
                card_image, n_shapes=attributes["n_shapes"], color=attributes["color"]
            )
            fill = False
        self._draw_shapes(
            card_image,
            n_shapes=attributes["n_shapes"],
            shape_id=attributes["shape"],
            color=attributes["color"],
            fill=fill,
        )
        if with_border:
            self._draw_border(card_image)
        return card_image

    async def adraw_card(self, card: Tuple[int], card_bg: Tuple[int] = None, with_border:bool = False):
        return self.draw_card(card, card_bg, with_border)


if __name__ == "__main__":
    set_images = CardImageDraw(resolution=2, n_attribute_values=5)
    card_image = set_images.draw_card((0, 3, 3, 4), (255, 255, 255, 255))
    card_image.show()
