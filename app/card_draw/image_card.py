from typing import Literal, Callable, Tuple
from random import choices
from string import ascii_letters, digits
from tkinter import Canvas
from PIL import Image, ImageTk
import customtkinter as ctk

from app_content.custom_widgets import SelectionPanel, custom_button
from .draw_settings import *
from settings import *

CARD_IMAGES = {}
# ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
LETTER_CHOICES = ascii_letters + digits
N = 8

def random_id(k: int):
    return "".join(choices(LETTER_CHOICES, k=k))

class ImageCard(Canvas):
    def __init__(
        self,
        master,
        image=None,
        image_id: str = None,
        bg_color: str = "white",
        bd_color: str = None,
        bd_width: int = 0,
        relief: str = "flat",
        state: Literal["normal", "disabled"] = "normal",
        is_button: bool = False,
        update_size_type: Literal["fit", "ratio"] = "ratio",
        valid_selection: Callable[[None], bool] = lambda: True,
    ):
        super().__init__(
            master,
            bg=bg_color,
            highlightbackground=bd_color,
            highlightthickness=bd_width,
            relief=relief,
            state=state,
        )
        self.image = self._get_image(image)
        self.image_tk = None
        self.image_id = image_id or random_id(N)
        self.update_size_type = update_size_type
        self.selected = False
        self.valid_selection = valid_selection
        self.prev_wait = None
        # For autoupdating the size (commented due to heavy load times while resizing)
        self.bind("<Configure>", self.update_wait)
        if is_button:
            self.bind("<Button>", self.select_card)

    def _get_image(self, image):
        """
        Obtains the image of the card, creating an empty image if no image is associated with it, a path to the
        image or a Pillow image.
        """
        if image is None:
            return Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), color=WHITE)
        return Image.open(image) if isinstance(image, str) else image

    def update_image(self, image):
        """Update the image associated to the card"""
        self.image = self._get_image(image)
        self.event_generate("<Configure>")

    def select_card(self, event):
        """Function associated to clicking the card, if the card is acting as a button"""
        activated = self.valid_selection()
        if not activated:
            return
        self.change_selection()

    def change_selection(self):
        """Changes the selection of the card"""
        if self.selected:
            self.configure(highlightbackground=None, highlightthickness=0)
        else:
            self.configure(
                highlightbackground=ACCENT_COLOR, highlightthickness=BD_WIDTH
            )
        self.selected = not self.selected

    def update_wait(self, event):
        """Updates the image size, after waitint for 0ms, to avoid lagging the interface"""
        if self.prev_wait is not None:
            self.after_cancel(self.prev_wait)
        self.prev_wait = self.after(
            0,
            lambda: (
                self.update_size_ratio(event)
                if self.update_size_type == "ratio"
                else self.update_size_fit(event)
            ),
        )

    def update_size_ratio(self, event):
        """Updates the image size taking into consideration the size ratio of the canvas"""
        self.prev_wait = None
        if self.image_tk is not None:
            self.delete(self.image_tk)
        event_width = event.width if event.width != 0 else self.winfo_width()
        event_height = event.height if event.height != 0 else self.winfo_height()
        image_ratio = self.image.width / self.image.height
        canvas_ratio = event_width / event_height
        if canvas_ratio > image_ratio:
            height = int(event_height)
            width = int(height * image_ratio)
        else:
            width = int(event_width)
            height = int(width / image_ratio)
        resized_image = self.image.resize((width, height))
        CARD_IMAGES[self.image_id] = ImageTk.PhotoImage(resized_image)
        resized_image.close()
        self.image_tk = self.create_image(
            int(event_width / 2),
            int(event_height / 2),
            anchor="center",
            image=CARD_IMAGES[self.image_id],
        )

    def update_size_fit(self, event):
        """Updates the image to fit the Canvas"""
        self.prev_wait = None
        if self.image_tk is not None:
            self.delete(self.image_tk)
        event_width = event.width if event.width != 0 else self.winfo_width()
        event_height = event.height if event.height != 0 else self.winfo_height()
        resized_image = self.image.resize((event_width, event_height))
        CARD_IMAGES[self.image_id] = ImageTk.PhotoImage(resized_image)
        resized_image.close()
        self.image_tk = self.create_image(
            int(event_width / 2),
            int(event_height / 2),
            anchor="center",
            image=CARD_IMAGES[self.image_id],
        )

    def destroy(self):
        """Destroy the Widget"""
        if self.image_id in CARD_IMAGES:
            del CARD_IMAGES[self.image_id]
        super().destroy()


class CardPicker(ctk.CTkFrame):
    def __init__(
        self,
        master,
        n_attributes: int,
        n_attribute_values: int,
        fg_color=SECONDARY_COLOR,
        border_color=ACCENT_COLOR,
        border_width=BD_WIDTH,
        corner_radius=10,
        card_generator=lambda master, card: ImageCard(master),
    ):
        super().__init__(
            master,
            fg_color=fg_color,
            border_color=border_color,
            border_width=border_width,
            corner_radius=corner_radius,
        )
        self.rowconfigure(0, uniform="a", weight=5)
        self.rowconfigure(1, uniform="a", weight=1)
        self.columnconfigure((0, 1), uniform="a", weight=1)
        self.card_generator = card_generator
        self.curr_card = None
        self.card_picked = None
        # Font card
        button_font = ctk.CTkFont(
            family=CARD_PICK_BUTTON_FONT, size=CARD_PICK_BUTTON_SIZE, weight="bold"
        )
        option_font = ctk.CTkFont(
            family=CARD_INPUT_FONT, size=CARD_INPUT_SIZE, weight="bold"
        )
        # Placements
        self.pos_attributes = ATTRIBUTE_ORDER[:n_attributes]
        card_options = {opt_id: CARD_OPTIONS[opt_id] for opt_id in self.pos_attributes}
        self.picker_slide = SelectionPanel(
            self,
            rel_start=(1, 0),
            rel_end=(0, 0),
            rel_height=1,
            rel_width=1,
            option_dictionary=card_options,
            max_options=n_attribute_values,
            selection_font=option_font,
            button_font=button_font,
            accept_function=self.update_pick,
        )
        pick_card = custom_button(
            self, text=PICK, command=self.picker_slide.move, font=button_font
        )
        reset_card = custom_button(
            self, text=RESETPICK, command=self.reset_pick, font=button_font
        )
        # Place cards
        pick_card.grid(row=1, column=0, sticky="nsew", padx=PADX, pady=PADY)
        reset_card.grid(row=1, column=1, sticky="nsew", padx=PADX, pady=PADY)
        self.place_card()

    def set_card_generator(self, card_generator):
        """Set the card graphics generator"""
        self.card_generator = card_generator
        self.place_card()

    def selected_card(self):
        """Returns the card that was selected"""
        curr_picks = self.picker_slide.get_values()
        card = tuple(curr_picks[att_id] for att_id in self.pos_attributes)
        any_is_none = any(c is None for c in card)
        if any_is_none:
            return None
        return card

    def place_card(self):
        """Updates the ImageCard Widget with the new card selection"""
        if self.card_picked is not None:
            self.card_picked.destroy()
        self.card_picked = self.card_generator(self, self.curr_card)
        self.card_picked.grid(
            row=0, column=0, columnspan=2, sticky="nsew", padx=PADX, pady=PADY
        )

    def reset_pick(self):
        """Resets the pick to no card selected"""
        self.picker_slide.set_default()
        self.curr_card = None
        self.place_card()

    def update_pick(self):
        """Updates the card pick in the widget"""
        self.curr_card = self.selected_card()
        self.place_card()

    def set_curr_card(self, card: Tuple[int]):
        """Updates the ImageCard with the passed card"""
        self.curr_card = card
        self.place_card()

    def get_card(self):
        """Returns the card value of the card that was picked"""
        return self.curr_card


class PickerWindow(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        n_attributes: int,
        n_attribute_values: int,
        width: int = PICK_WINDOW_WIDTH,
        height: int = PICK_WINDOW_HEIGHT,
        bg_color: str | Tuple[str, str] | None = BG_COLOR,
        button_text: str = GUESS_CARD,
        fg_color=SECONDARY_COLOR,
        border_color=ACCENT_COLOR,
        border_width=BD_WIDTH,
        corner_radius=10,
        card_generator=lambda master, card: ImageCard(master),
    ):
        super().__init__(parent, fg_color=bg_color)
        # Window settings
        self.title("Pick a Card")
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)
        self.maxsize(width, height)
        self.rowconfigure(0, weight=5, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        # Window widgets
        self.card_input = CardPicker(
            self,
            n_attributes,
            n_attribute_values,
            fg_color,
            border_color,
            border_width,
            corner_radius,
            card_generator,
        )
        button_font = ctk.CTkFont(
            family=CARD_PICK_BUTTON_FONT, size=CARD_PICK_BUTTON_SIZE, weight="bold"
        )
        accept_input = custom_button(
            self, text=button_text, command=self.select, font=button_font
        )
        # Widget placement
        self.card_input.grid(row=0, column=0, sticky="nsew", padx=PADX, pady=PADY)
        accept_input.grid(row=1, column=0, sticky="nsew", padx=PADX, pady=PADY)
        self.selection = None
        self.image = None

    def select(self):
        """Select the card from the CardPicker"""
        self.selection = self.card_input.get_card()
        self.image = self.card_input.card_picked.image
        self.destroy()

    def show(self):
        """
        Opens the PickerWindow, and closes when the card is selected or the window is manually closed
        """
        self.deiconify()
        self.wm_protocol("WM_DELETE_WINDOW", self.destroy)
        self.wait_window(self)
        return self.selection, self.image


class PickerButton(ImageCard):
    def __init__(
        self,
        master,
        picker_window_generator: Callable[[None], PickerWindow],
        bg_color: str = "white",
        bd_color: str = None,
        bd_width: int = 0,
        relief: str = "flat",
        state: Literal["normal", "disabled"] = "normal",
        command: Callable[[None], None] = lambda: (),
    ):
        super().__init__(
            master,
            bg_color=bg_color,
            bd_color=bd_color,
            bd_width=bd_width,
            relief=relief,
            state=state,
            is_button=True,
        )
        self.command = command
        self.curr_card = None
        self.picker_window_generator = picker_window_generator

    def select_card(self, event):
        """
        Opens a PickerWindow, the user picks a card in the window, and on closing updates
        curr_card and button image
        """
        self.configure(state="disabled")
        picker_wd = self.picker_window_generator()
        if self.curr_card:
            picker_wd.card_input.set_curr_card(self.curr_card)
        self.curr_card, card_im = picker_wd.show()
        self.update_image(card_im)
        if self.curr_card is None:
            self.configure(highlightbackground=None, highlightthickness=0)
        else:
            self.configure(
                highlightbackground=ACCENT_COLOR, highlightthickness=BD_WIDTH
            )
        self.configure(state="normal")
        self.command()

    def reset_button(self):
        """Resets the button value to None and its image to an empty image"""
        self.update_image(None)
        self.curr_card = None

    def get_card(self):
        """Obtains the current value of the button"""
        return self.curr_card
