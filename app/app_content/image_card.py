from typing import Literal
from tkinter import Canvas
from PIL import Image, ImageTk
from settings import *

CARD_IMAGES = {}
class ImageCard(Canvas):
    def __init__(self,
            master,
            image,
            card_id,
            bg_color: str = "blue",
            bd_color: str = None,
            bd_width: int = 0,
            relief: str = "flat",
            state: Literal['normal', 'disabled'] = "normal",
            selected: bool = False,
            is_button:bool = False,
            card_function = lambda card_id: ()
        ):
        super().__init__(master,
            bg = bg_color,
            highlightbackground = bd_color,
            highlightthickness = bd_width,
            relief = relief,
            state = state
        )
        if isinstance(image, str):
            self.image = Image.open(image)
        else:
            self.image = image
        self.image_ratio = self.image.width / self.image.height
        self.card_id = card_id
        self.selected = selected
        self.card_function = card_function
        # For autoupdating the size (commented due to heavy load times while resizing)
        self.bind('<Configure>', self.update_size)
        if is_button:
            self.bind('<Button>', self.select_card)
    
    @classmethod
    def blank_card(cls, master, bg_color: str = "blue", bd_color: str = None, bd_width: int = 0, relief: str = "flat"):
        return super().__init__(master, bg = bg_color, highlightbackground = bd_color, highlightthickness = bd_width, relief = relief, state = "disabled")
    
    def select_card(self, event):
        activated = self.card_function(self.card_id)
        if not activated:
            return
        self.change_selection()
    
    def change_selection(self):
        if self.selected:
            self.configure(highlightbackground = None, highlightthickness = 0)
        else:
            self.configure(highlightbackground = ACCENT_COLOR, highlightthickness = BD_WIDTH)
        self.selected = not self.selected
    
    def update_size(self, event):
        width = event.width
        height = event.height
        canvas_ratio = width / height
        if canvas_ratio > self.image_ratio:
            height = int(event.height)
            width = int(height * self.image_ratio)
        else:
            width = int(event.width)
            height = int(width / self.image_ratio)
        if not self.card_id in CARD_IMAGES:
            resized_image = self.image.resize((width, height))
            CARD_IMAGES[self.card_id] = ImageTk.PhotoImage(resized_image)
            resized_image.close()
        self.create_image(
            int(event.width / 2),
            int(event.height / 2),
            anchor = 'center',
            image = CARD_IMAGES[self.card_id]
        )