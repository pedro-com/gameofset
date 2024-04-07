from typing import Literal
from tkinter import Canvas
from PIL import Image, ImageTk

class ImageCard(Canvas):
    def __init__(self,
            master,
            image,
            bg_color: str = "blue",
            bd_color: str = None,
            bd_width: int = 0,
            relief: str = "flat",
            state: Literal['normal', 'disabled'] = "normal"
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
        self.bind('<Configure>', self.update_size)
    
    def update_size(self, event):
        global resized_tk
        width = event.width
        height = event.height
        canvas_ratio = width / height
        if canvas_ratio > self.image_ratio:
            height = int(event.height)
            width = int(height * self.image_ratio)
        else:
            width = int(event.width)
            height = int(width / self.image_ratio)
        resized_image = self.image.resize((width, height))
        resized_tk = ImageTk.PhotoImage(resized_image)
        self.create_image(
            int(event.width / 2),
            int(event.height / 2),
            anchor = 'center',
            image = resized_tk
        )