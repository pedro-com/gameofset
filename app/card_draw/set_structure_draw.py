from typing import Tuple, List, Iterable, Callable, Any
from PIL import Image
from asyncio import TaskGroup

from .draw_settings import *
from .card_draw import CardImageDraw
from .image_card import ImageCard, CardPicker, PickerWindow, PickerButton
from settings import GUESS_CARD


class SETStructureDraw:
    """
    General class to generate card images (lists of card images), card structures (magic squares,
    hyperplanes...), and UI card elements such as PickerWindows or PickerButtons
    """

    def __init__(
        self,
        card_resolution: int = 2,
        resolution: int = 2,
        card_bg: Tuple[int] = WHITE,
        def_card_bg: Tuple[int] = TRANSPARENT,
        n_attribute_values=3,
        canvas_bg=TRANSPARENT,
        with_border:bool=False
    ):
        self.el_width = int(resolution * ELEMENT_WIDTH)
        self.el_height = int(resolution * ELEMENT_HEIGHT)
        self.padx = int(resolution * ELEMENT_PADX)
        self.pady = int(resolution * ELEMENT_PADY)
        # self.bd_width = int(resolution * BD_WIDTH)
        self.card_image_draw = CardImageDraw(
            resolution=card_resolution,
            n_attribute_values=n_attribute_values,
            card_bg=def_card_bg,
        )
        self.with_border = with_border
        self.card_bg = card_bg
        self.canvas_bg = canvas_bg
        self.canvas_width = self._canvas_width(self.card_image_draw.n_attribute_values)
        self.canvas_height_line = self.el_height + self.pady
        self.canvas_height_col = self._canvas_height(
            self.card_image_draw.n_attribute_values
        )

    def _canvas_width(self, n_cols: int):
        """Obtains the width of the canvas, given the maximum number of columns"""
        return (self.el_width + self.padx) * n_cols

    def _canvas_height(self, n_lines: int):
        """Obtains the height of the canvas, given the maximumn number of lines"""
        return self.canvas_height_line * n_lines

    def _line_points(self, n_cols: int):
        """Top left points for the function draw_element_line (line canvas)"""
        y_0 = int(self.pady // 2)
        x_0 = int(self.padx // 2)
        step = self.padx + self.el_width
        return [(x_0 + k * step, y_0) for k in range(n_cols)]

    def _column_points(self, n_lines: int):
        """Top left points for the function draw_element_column (column canvas)"""
        return [(0, k * self.canvas_height_line) for k in range(n_lines)]

    @property
    def line_points(self):
        """Top left points for the default line canvas (n_attribute_values)"""
        return self._line_points(self.card_image_draw.n_attribute_values)

    @property
    def column_points(self):
        """Top left points for the default column canvas (n_attribute_values)"""
        return self._column_points(self.card_image_draw.n_attribute_values)

    def draw_card_list(self, cards: Tuple[int], card_bg: Tuple[int] = None, with_border:bool = False):
        return [self.card_image_draw.draw_card(card, card_bg or self.card_bg, with_border) for card in cards]

    def _draw_element_line(self, image_elems: List[Image.Image]):
        """Draws a line canvas of column elements"""
        image_canvas = Image.new(
            "RGBA", (self.canvas_width, self.canvas_height_line), color=self.canvas_bg
        )
        for image_elem, point in zip(image_elems, self.line_points):
            image_elem = image_elem.resize((self.el_width, self.el_height))
            image_canvas.paste(image_elem, point)
            image_elem.close()
        return image_canvas

    def _draw_element_column(self, image_elems: List[Image.Image]):
        """Draws a column canvas of line elements"""
        image_canvas = Image.new(
            "RGBA", (self.canvas_width, self.canvas_height_col), color=self.canvas_bg
        )
        for image_elem, point in zip(image_elems, self.column_points):
            image_elem = image_elem.resize(
                (self.canvas_width, self.el_height + self.pady)
            )
            image_canvas.paste(image_elem, point)
            image_elem.close()
        return image_canvas

    def _draw_card_line(self, cards: Iterable, n_cols: int = None):
        """
        Draws a card line in the canvas. Useful for drawing SETs or any other SET structure.
        This is the base case in the recursion
        """
        # card_images = [self.card_image_draw.draw_card(card, self.card_bg) for card in cards]
        card_images = self.draw_card_list(cards, self.card_bg, with_border=self.with_border)
        if n_cols is None or n_cols <= 0:
            canvas_size = (self.canvas_width, self.canvas_height_line)
            line_points = self.line_points
        else:
            canvas_size = (self._canvas_width(n_cols), self.canvas_height_line)
            line_points = self._line_points(n_cols)
            card_images = card_images[:min(len(card_images), n_cols)]
        image_canvas = Image.new("RGBA", size=canvas_size, color=self.canvas_bg)
        for card_image, l_point in zip(card_images, line_points):
            card_image = card_image.resize((self.el_width, self.el_height))
            image_canvas.paste(card_image, l_point)
            card_image.close()
        return image_canvas

    def _draw_elements(self, elements):
        if not isinstance(elements[0], list):
            return ("line", self._draw_card_line(elements))
        elem_images = [self._draw_elements(el) for el in elements]
        dir = elem_images[0][0]
        same_dir = all(dir == el_dir for el_dir, _ in elem_images[1:])
        image_elems = [image_elem for _, image_elem in elem_images]
        if same_dir and dir == "line":
            return ("column", self._draw_element_column(image_elems))
        elif same_dir:
            return ("line", self._draw_element_line(image_elems))

    def draw_elements(self, elements):
        """
        Elements should either be a list of Lists or a List of cards.
        """
        if all(isinstance(el, list) for el in elements):  # Case List of Lists
            _, elem_images = self._draw_elements(elements)
            return elem_images
        return self._draw_card_line(elements)

    def draw_element_structure(self, n_cols: int, n_lines: int, cards: Iterable[Tuple[int]]):
        """Draw an element structure with the specified number of lines and columns"""
        cards = list(cards)
        canvas_size = (
            self._canvas_width(n_cols),
            self._canvas_height(n_lines),
        )
        image_canvas = Image.new("RGBA", size=canvas_size, color=self.canvas_bg)
        num_cards = len(cards)
        canvas_image_lines = [
            self._draw_card_line(cards[k : min(k + n_cols, num_cards)], n_cols)
            for k in range(0, num_cards, n_cols)
        ]
        column_points = self._column_points(n_lines)
        for idy, image_line in enumerate(canvas_image_lines):
            image_line = image_line.resize((canvas_size[0], self.el_height + self.pady))
            image_canvas.paste(image_line, column_points[idy])
            image_line.close()
        return image_canvas

    async def _adraw_card_line(self, cards: Iterable[Tuple[int]], with_border:bool = False):
        async with TaskGroup() as tg:
            card_tgs = [
                tg.create_task(self.card_image_draw.adraw_card(card, self.card_bg, with_border))
                for card in cards
            ]
        image_canvas = Image.new(
            "RGBA", (self.canvas_width, self.canvas_height_line), color=self.canvas_bg
        )
        for card_tg, point in zip(card_tgs, self.line_points):
            card_image = card_tg.result()
            card_image = card_image.resize((self.el_width, self.el_height))
            image_canvas.paste(card_image, point)
            card_image.close()
        return image_canvas

    async def _adraw_elements(self, elements):
        if not isinstance(elements[0], list):
            return ("line", await self._adraw_card_line(elements))
        async with TaskGroup() as tg:
            elem_tasks = [tg.create_task(self._adraw_elements(el)) for el in elements]
        elem_images = [elem_task.result() for elem_task in elem_tasks]
        dir = elem_images[0][0]
        same_dir = all(dir == el_dir for el_dir, _ in elem_images[1:])
        image_elems = [image_elem for _, image_elem in elem_images]
        if same_dir and dir == "line":
            return ("column", self._draw_element_column(image_elems))
        elif same_dir:
            return ("line", self._draw_element_line(image_elems))

    async def adraw_elements(self, elements):
        if all(isinstance(el, list) for el in elements):  # Case List of Lists
            _, elem_images = await self._adraw_elements(elements)
            return elem_images
        return await self._adraw_card_line(elements)

    async def adraw_card_list(self, cards: Tuple[int], card_bg: Tuple[int] = None, with_border:bool=False):
        async with TaskGroup() as tg:
            task_images = [
                tg.create_task(self.card_image_draw.adraw_card(card, card_bg, with_border))
                for card in cards
            ]
        return [task_image.result() for task_image in task_images]

    def generate_cards(
        self,
        master,
        cards: Iterable[Tuple[int]],
        bg_color: Any = "white",
        is_button: bool = True,
        card_function: Callable[[Any], None] = lambda card: (),
        update_size_type="ratio",
    ):
        card_images = self.draw_card_list(cards)
        return [
            (
                card,
                ImageCard(
                    master,
                    image=card_image,
                    bg_color=bg_color,
                    is_button=is_button,
                    valid_selection=lambda card=card: card_function(card),
                    update_size_type=update_size_type,
                ),
            )
            for card, card_image in zip(cards, card_images)
        ]

    def generate_card_structure(
        self, master, elements, bg_color: Any = "white", update_size_type="ratio",
    ):
        return ImageCard(
            master,
            image=self.draw_elements(elements),
            bg_color=bg_color,
            update_size_type=update_size_type,
        )

    def _generate_card(
        self, master, card, bg_color=TRANSPARENT, update_size_type="ratio"
    ):
        return (ImageCard(master)
            if card is None
            else self.generate_cards(
                    master,
                    (card,),
                    bg_color=bg_color,
                    update_size_type=update_size_type,
                )[0][1]
        )

    def generate_card_picker(self, master, n_attributes: int, bg_color="white"):
        return CardPicker(
            master,
            n_attributes=n_attributes,
            n_attribute_values=self.card_image_draw.n_attribute_values,
            card_generator=lambda master, card: self._generate_card(
                master, card, bg_color=bg_color
            ),
        )

    def generate_picker_window(
        self,
        master,
        n_attributes: int,
        bg_color="white",
        update_size_type="ratio",
        button_text=GUESS_CARD,
    ):
        return PickerWindow(
            master,
            n_attributes=n_attributes,
            n_attribute_values=self.card_image_draw.n_attribute_values,
            card_generator=lambda master, card: self._generate_card(
                master, card, bg_color=bg_color, update_size_type=update_size_type
            ),
            button_text=button_text,
        )

    def generate_picker_button(
        self,
        master,
        n_attributes: int,
        bg_color: str = "white",
        bd_color: str = None,
        bd_width: int = 0,
        update_size_type="ratio",
        button_text=GUESS_CARD,
        command: Callable[[None], None] = lambda: (),
    ):
        return PickerButton(
            master,
            picker_window_generator=lambda: self.generate_picker_window(
                master,
                n_attributes,
                update_size_type=update_size_type,
                button_text=button_text,
            ),
            bg_color=bg_color,
            bd_color=bd_color,
            bd_width=bd_width,
            command=command,
        )


if __name__ == "__main__":
    n_attribute_values = 3
    struct = SETStructureDraw(card_resolution=1, n_attribute_values=n_attribute_values)
    # points = generate_affine_space([(0, 0, 0, 0), (0, 0, 2, 0), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1)], n_attribute_values)
    # a = struct.draw_elements(points)
    # a = run(struct.adraw_elements(points))
    # print(a.width, a.height)
    # a.show()
    # a.resize((800, 800)).show()
    # a.show()
