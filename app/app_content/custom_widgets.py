from tkinter import BooleanVar, IntVar, StringVar
from typing import Any, Tuple
import customtkinter as ctk
from settings import *

def game_button(master, text:str, command = lambda: (), text_color:str=BG_COLOR, state:str="normal", font:ctk.CTkFont = None, border_width=BD_WIDTH):
    return ctk.CTkButton(master,
        fg_color=BUTTON_COLOR,
        hover_color=ACCENT_COLOR,
        border_width=border_width,
        border_color=ACCENT_COLOR,
        font=font,
        state=state,
        text=text,
        text_color=text_color,
        command=command
    )

class ProgressTracker(ctk.CTkFrame):
    def __init__(self, master, max_value:int,
            fg_color = BG_COLOR,
            border_color = ACCENT_COLOR,
            component_color = SECONDARY_COLOR,
            border_width = BD_WIDTH,
            corner_radius = 10,
            progress_color = DEF_PROGRESS_COLOR,
            text_format = 'Value %d points'
        ):
        super().__init__(master, fg_color=fg_color, border_color=border_color, border_width=border_width, corner_radius=corner_radius)
        text_font = ctk.CTkFont(family = LABEL_FONT, size = LABEL_TEXT_SIZE, weight = "bold")
        self.columnconfigure(0, uniform = 'a', weight = 1)
        self.rowconfigure(0, uniform = 'a', weight = 2)
        self.rowconfigure(1, uniform = 'a', weight = 1)
        # Variables
        self.actual_value = IntVar(self, value = 0)
        self.max_value = max_value
        self.text_format = text_format
        
        self.progress_bar = ctk.CTkProgressBar(self,
            progress_color=progress_color,
            fg_color=component_color,
            corner_radius=corner_radius
        )
        self.progress_bar.set(0)
        self.progress_label = ctk.CTkLabel(self,
            fg_color=component_color,
            corner_radius=corner_radius,
            text_color=progress_color,
            text=self.text_format % 0,
            font=text_font,
        )
        self.actual_value.trace_add('write', self._modify_values)
        self.progress_label.grid(row = 0, sticky = 'nsew', padx = PADX, pady = PADY)
        self.progress_bar.grid(row = 1, sticky = 'ew', padx = PADX)
    
    def _modify_values(self, *args):
        value = self.actual_value.get()
        if value < 0:
            self.actual_value.set(0)
            return
        self.progress_label.configure(text=self.text_format % (value,))
        self.progress_bar.set(max(value / self.max_value, 0))

class Timer(ProgressTracker):
    def __init__(self, master, max_time: int,
            fg_color=BG_COLOR,
            border_color=ACCENT_COLOR,
            component_color=SECONDARY_COLOR,
            border_width=BD_WIDTH,
            corner_radius=10,
            progress_color=DEF_PROGRESS_COLOR,
            text_format='Timer: %ds'
        ):
        super().__init__(master, max_time, fg_color, border_color, component_color, border_width, corner_radius, progress_color, text_format)
        self.is_end = BooleanVar(value = True)
        self.actual_value.set(self.max_value)
        self.prev_after = ""
    
    def time_loop(self):
        if not self.is_end.get():
            actual_time = self.actual_value.get() - 1
            self.actual_value.set(actual_time)
            if actual_time == 0:
                self.is_end.set(True)
            self.prev_after = self.after(1000, self.time_loop)
    
    def start(self):
        self.actual_value.set(self.max_value + 1)
        self.is_end.set(False)
        self.time_loop()
        self.after_cancel
    
    def reset(self):
        if not self.is_end.get():
            self.is_end.set(True)
            self.after_cancel(self.prev_after)

class TextOutput(ctk.CTkFrame):
    def __init__(self, master,
            fg_color = BG_COLOR,
            component_color = SECONDARY_COLOR,
            border_color = ACCENT_COLOR,
            border_width = BD_WIDTH,
            corner_radius = 10,
            text = 'TextValue',
        ):
        super().__init__(master, corner_radius=corner_radius, border_width=border_width, fg_color=fg_color, border_color=border_color)
        self.text = StringVar(value=text)
        font = ctk.CTkFont(family = LABEL_FONT, size = LABEL_TEXT_SIZE, weight = 'bold')
        self.text_label = ctk.CTkLabel(self,
            fg_color=component_color,
            corner_radius=corner_radius,
            text_color=fg_color,
            text=text,
            font=font
        )
        self.text.trace_add('write', self.modify_label)
        self.text_label.pack(fill = 'both', expand = True, padx = PADX, pady = PADY)
    
    def modify_label(self, *args):
        self.text_label.configure(text = self.text.get())
