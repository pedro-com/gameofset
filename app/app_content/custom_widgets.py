from tkinter import BooleanVar, IntVar, StringVar, filedialog
from typing import List, Tuple, Callable, Dict
import customtkinter as ctk

from settings import *

def custom_button(master, text:str = "", command = lambda: (), text_color:str=BG_COLOR, state:str="normal", font:ctk.CTkFont = None, border_width=BD_WIDTH, fg_color=BUTTON_COLOR, hover_color=ACCENT_COLOR, textvariable=None):
    return ctk.CTkButton(master,
        fg_color=fg_color,
        hover_color=hover_color,
        border_width=border_width,
        border_color=hover_color,
        font=font,
        state=state,
        text=text,
        textvariable=textvariable,
        text_color=text_color,
        command=command
    )

def info_panel(master,
            rel_start: Tuple[float, float],
            rel_end: Tuple[float, float],
            rel_width: float,
            rel_height: float,
            text:str,
            font:ctk.CTkFont = None,
            dismiss_action: Callable[[None], None] = lambda : ()):
    slide_panel = SlidingFrame(master, rel_start, rel_end, rel_width, rel_height)
    slide_panel.rowconfigure(0, weight = 3, uniform = 'a')
    slide_panel.rowconfigure(1, weight = 1, uniform = 'a')
    slide_panel.columnconfigure(0, weight = 1, uniform = 'a')
    def dismiss_panel():
        slide_panel.move()
        dismiss_action()
    label_font = ctk.CTkFont(family = INFO_FONT, size = INFO_TEXT_SIZE, weight = 'bold')
    text_output = TextOutput(slide_panel, text = text, anchor='nw', font=label_font)
    dismiss_button = custom_button(slide_panel, text = UNDERSTOOD, font = font, command=dismiss_panel)
    text_output.grid(row = 0, column = 0, sticky = 'nsew', padx = PADX, pady = PADY)
    dismiss_button.grid(row = 1, column = 0, sticky = 'sew', padx = PADX, pady = PADY)
    # Update the Wrap of the text
    # text_output.update_wrap()
    return slide_panel
    
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
        text_font = ctk.CTkFont(family = OUTPUT_FONT, size = OUTPUT_TEXT_SIZE, weight = "bold")
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
    
    def modify_max_value(self, max_value:int):
        self.max_value = max_value

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
            font = None,
            text = 'TextValue',
            anchor = 'center'
        ):
        super().__init__(master, corner_radius=corner_radius, border_width=border_width, fg_color=fg_color, border_color=border_color)
        self.text = StringVar(value=text)
        self.text_label = ctk.CTkLabel(self,
            fg_color=component_color,
            corner_radius=corner_radius,
            text_color=fg_color,
            text=text,
            font=font,
            anchor=anchor
        )
        self.text.trace_add('write', self.modify_label)
        self.text_label.pack(fill = 'both', expand = True, padx = PADX, pady = PADY)
        self.bind('<Configure>', lambda e: self.text_label.configure(wraplength=master.winfo_width() - 3*PADX))
    
    def modify_label(self, *args):
        self.text_label.configure(text = self.text.get())

class FileNameInput(ctk.CTkFrame):
    def __init__(self, master,
            fg_color = BG_COLOR,
            component_color = SECONDARY_COLOR,
            border_color = ACCENT_COLOR,
            border_width = BD_WIDTH,
            corner_radius = 10,
            font:ctk.CTkFont= None,
        ):
        super().__init__(master, corner_radius=corner_radius, border_width=border_width, fg_color=fg_color, border_color=border_color)
        ctk.CTkLabel(self, text = INPUTNAME,
            fg_color="transparent",
            font=font,
            text_color=component_color,
            corner_radius=corner_radius,
        ).pack(fill = 'x', expand=True, padx=PADX, pady=PADY)
        self.output = ctk.CTkLabel(self, text = '',
            fg_color=component_color,
            font=font,
            text_color='white',
            corner_radius=corner_radius,
        )
        self.name = StringVar(self, value = '')
        self.file_ext = StringVar(self, value = 'jpg')
        self.name.trace_add('write', self.update_text)
        self.file_ext.trace_add('write', self.update_text)
        ctk.CTkEntry(self,
            textvariable = self.name,
            font=font,
            fg_color=component_color,
            text_color='white'
        ).pack(fill = 'x', padx = PADX, pady = PADY)
        self.create_ext_frame(component_color, font)
        self.output.pack(fill = 'x', padx = PADX, pady = PADY)
    
    def update_text(self, *args):
        file_name = self.get_file_name()
        self.output.configure(text=file_name if file_name else '')
    
    def get_file_name(self):
        name = self.name.get()
        return f'{name.replace(' ', '_')}.{self.file_ext.get()}' if name else None
        
    def set_ext(self, ext:str):
        self.file_ext.set(ext)

    def create_ext_frame(self, component_color, font):
        ext_frame = ctk.CTkFrame(self, fg_color='transparent')
        jpg_check = ctk.CTkCheckBox(ext_frame, text = 'jpg', variable = self.file_ext, font = font, text_color = component_color, command=self.set_ext('jpg'), onvalue = 'jpg', offvalue = 'png', fg_color = component_color)
        png_check = ctk.CTkCheckBox(ext_frame, text = 'png', variable = self.file_ext, font = font, text_color = component_color, command=self.set_ext('png'), onvalue = 'png', offvalue = 'jpg', fg_color = component_color)
        jpg_check.pack(side = 'left', fill='both', padx = PADX, pady= PADY)
        png_check.pack(side = 'left', fill='both', padx = PADX, pady= PADY)
        ext_frame.pack(fill = 'x', padx = PADX, pady=PADY)

class FilePathInput(ctk.CTkFrame):
    def __init__(self, master,
            fg_color = BG_COLOR,
            component_color = SECONDARY_COLOR,
            border_color = ACCENT_COLOR,
            border_width = BD_WIDTH,
            corner_radius = 10,
            font:ctk.CTkFont= None,
            button_font:ctk.CTkFont= None
        ):
        super().__init__(master, corner_radius=corner_radius, border_width=border_width, fg_color=fg_color, border_color=border_color)
        self.path = StringVar(self, value='.')
        custom_button(self,
            text = OPEN_EXPLORER,
            command = self.select_file_directory,
            font=button_font
        ).pack(fill = 'x', padx = PADX, pady = PADY)
        ctk.CTkEntry(self,
            textvariable=self.path,
            fg_color=component_color,
            corner_radius=corner_radius,
            font=font,
            state='disabled',
            text_color="white"
        ).pack(fill='both', expand=True, padx = PADX, pady= PADY)
    
    def select_file_directory(self):
        self.path.set(filedialog.askdirectory())
    
    def get_directory_path(self):
        return self.path.get()

class SlidingFrame(ctk.CTkFrame):
    def __init__(self, master,
            rel_start: Tuple[float, float],
            rel_end: Tuple[float, float],
            rel_width: float,
            rel_height: float,
            corner_radius: int | str | None = 10,
            border_width: int | str | None = BD_WIDTH,
            fg_color: str | Tuple[str] | None = PRIMARY_COLOR,
            border_color: str | Tuple[str] | None = ACCENT_COLOR,
            animation_steps: int = 5,
            anchor:str = 'nw'
        ):
        super().__init__(master, corner_radius=corner_radius, border_width=border_width, fg_color=fg_color, border_color=border_color)
        # Init variables
        self.rel_start = rel_start
        self.rel_end = rel_end
        self.rel_width = rel_width
        self.rel_height = rel_height
        self.anchor = anchor
        self.delta = tuple((self.rel_end[k] - self.rel_start[k]) / animation_steps
            for k in range(2)
        )        
        self.actual_pos = self.rel_start
        self.move_to_end = False
        self.prev_move = None # To cancel mid animation
        # Init and place buttons
        self.move_widget(self.rel_start)

    def move_widget(self, rel_pos: Tuple[float, float], lift:bool=True):
        if rel_pos in (self.rel_start, self.rel_end):
            pos_bound_x = rel_pos[0] + self.rel_width
            pos_bound_y = rel_pos[1] + self.rel_height
            if (rel_pos[0] < 0 or pos_bound_x > 1) or (pos_bound_y < 0 or pos_bound_y > 1):
                self.place_forget()
                return
        self.place(relx = rel_pos[0], rely = rel_pos[1], relwidth = self.rel_width, relheight = self.rel_height, anchor = self.anchor)
        if lift:
            self.lift()

    def _next_pos(self, dir:int):
        delta = self.delta[dir]
        actual_pos = self.actual_pos[dir]
        if delta == 0:
            return actual_pos
        if self.move_to_end:
            actual_pos += delta
            return max(self.rel_end[dir], actual_pos) if delta < 0 else min(self.rel_end[dir], actual_pos)
        actual_pos -= delta
        return min(self.rel_start[dir], actual_pos) if delta < 0 else max(self.rel_start[dir], actual_pos)
    
    def _move(self):
        self.actual_pos = tuple(self._next_pos(dir) for dir in range(2))
        self.move_widget(self.actual_pos)
        if self.actual_pos not in (self.rel_start, self.rel_end):
            # self.move_widget(self.actual_pos)
            self.after(10, self._move)
        else:
            self.prev_move = None

    def move(self):
        if self.prev_move:
            self.after_cancel(self.prev_move)
        self.move_to_end = not self.move_to_end
        self._move()
    
    def quick_move(self):
        if self.prev_move:
            self.after_cancel(self.prev_move)
        self.actual_pos = self.rel_start if self.move_to_end else self.rel_end
        self.move_widget(self.actual_pos)
        self.move_to_end = not self.move_to_end

class SelectionBox(ctk.CTkFrame):
    def __init__(self, master, selection_title:str, option_names:Tuple, option_values:Tuple,
            max_options:int=-1,
            default_value=None,
            fg_color=BG_COLOR,
            border_color=ACCENT_COLOR,
            component_color=SECONDARY_COLOR,
            border_width=BD_WIDTH,
            corner_radius=10,
            font=None):
        super().__init__(master, fg_color=fg_color, border_color=border_color, border_width=border_width, corner_radius=corner_radius)
        if len(option_names) != len(option_values):
            raise ValueError(f'Missing either option names[{option_names}] or option values[{option_values}]')
        self.rowconfigure((0, 1), uniform = 'a', weight = 1)
        self.columnconfigure(0, uniform = 'a', weight = 1)
        max_options = len(option_names) if max_options < 0 else min(len(option_names), max_options)
        self.option_names = option_names[:max_options]
        self.option_values = option_values[:max_options]
        title_label = ctk.CTkLabel(self,
            fg_color=component_color,
            corner_radius=corner_radius,
            text_color=fg_color,
            text=selection_title,
            font=font,
            anchor = 'w'
        )
        self.option_select =  ctk.CTkOptionMenu(self, font=font, dropdown_font=font, values=self.option_names, anchor='w')
        self.default_value = self.option_names[0]
        if default_value is not None:
            self.modify_default(default_value)
        title_label.grid(row = 0, column = 0, sticky = 'news', padx = PADX, pady = 6)
        self.option_select.grid(row = 1, column = 0, sticky = 'ew', padx = PADX, pady = 6)
    
    @staticmethod
    def _index(item_list:List, item):
        try:
            return item_list.index(item)
        except ValueError:
            return -1

    def get_value(self):
        curr_choice = self._index(self.option_names, self.option_select.get())
        return None if curr_choice == -1 else self.option_values[curr_choice]
    
    def get_name(self):
        curr_choice = self._index(self.option_names, self.option_select.get())
        return None if curr_choice == -1 else self.option_names[curr_choice]
    
    def _get_option_name(self, value):
        opt_id = self._index(self.option_values, value)
        if opt_id == -1:
            if value not in self.option_names:
                raise ValueError(f'Option {value} not in option names[{self.option_names}] or option values[{self.option_values}]')
            return value
        return self.option_names[opt_id]

    def modify_default(self, value):
        self.default_value = self._get_option_name(value)
        self.option_select.set(self.default_value)

    def set_value(self, value):
        self.option_select.set(self._get_option_name(value))

    def set_default(self):
        self.set_value(self.default_value)

class SelectionPanel(SlidingFrame):
    '''
    - option_dictionary: Associates the option id and the option choices for a selection box:
        * The option choices are a tuple, which has to contain: (selection_title, selection_names, selection_values, default_value)
    '''
    def __init__(self, master,
            rel_start: Tuple[float],
            rel_end: Tuple[float],
            rel_width: float,
            rel_height: float,
            option_dictionary: Dict[str, Tuple[str, tuple]],
            max_options: int = -1,
            corner_radius: int | str | None = 10,
            border_width: int | str | None = BD_WIDTH,
            fg_color: str | Tuple[str] | None = SECONDARY_COLOR,
            border_color: str | Tuple[str] | None = ACCENT_COLOR,
            animation_steps: int = 10,
            anchor: str = 'nw',
            selection_font: ctk.CTkFont = None,
            button_font:ctk.CTkFont = None,
            accept_function: Callable[[], None] = lambda : ()
        ):
        super().__init__(master, rel_start, rel_end, rel_width, rel_height, corner_radius, border_width, fg_color, border_color, animation_steps, anchor)
        num_rows = len(option_dictionary)
        self.rowconfigure(tuple(range(num_rows)), uniform = 'a', weight = 3)
        self.rowconfigure(num_rows, uniform = 'a', weight = 2)
        self.columnconfigure((0, 1), uniform = 'a', weight = 1)
        self.option_dict:Dict[str, SelectionBox]= {}
        self.curr_selection = {}
        self.accept_function = accept_function
        for idx, (opt_id, opt_values) in enumerate(option_dictionary.items()):
            self.option_dict[opt_id] = SelectionBox(self,
                max_options=max_options,
                selection_title=opt_values[0],
                option_names=opt_values[1],
                option_values=opt_values[2],
                default_value=opt_values[3],
                font=selection_font
            )
            self.curr_selection[opt_id] = self.option_dict[opt_id].get_value()
            self.option_dict[opt_id].grid(row = idx, column = 0, columnspan=2, sticky = 'nsew', padx = PADX, pady = PADY)
        accept_button = custom_button(self, text=ACCEPT, font=button_font, command=self.accept_selection, hover_color=ACCEPT_COLOR)
        cancel_button = custom_button(self, text=CANCEL, font=button_font, command=self.cancel_selection, hover_color=CANCEL_COLOR)
        accept_button.grid(row = num_rows, column = 0, sticky = 'sew', padx = PADX, pady = PADY)
        cancel_button.grid(row = num_rows, column = 1, sticky = 'sew', padx = PADX, pady = PADY)

    def get_values(self):
        return {opt_id: opt_box.get_value()
            for opt_id, opt_box in self.option_dict.items()
        }
    
    def get_names(self):
        return {opt_id: opt_box.get_name()
            for opt_id, opt_box in self.option_dict.items()
        }
    
    def set_default(self):
        for sel_box in self.option_dict.values():
            sel_box.set_default()
        self.curr_selection = self.get_values()
    
    def update_default(self):
        for opt_id, value in self.curr_selection:
            self.option_dict[opt_id].modify_default(value)

    def accept_selection(self):
        self.quick_move()
        self.curr_selection = self.get_values()
        self.accept_function()

    def cancel_selection(self):
        self.move()
        for opt_id, value in self.curr_selection.items():
            self.option_dict[opt_id].set_value(value)

class ExportPanel(SlidingFrame):
    def __init__(self, master, rel_start: Tuple[float], rel_end: Tuple[float], rel_width: float, rel_height: float,
            corner_radius: int | str | None = 10,
            border_width: int | str | None = BD_WIDTH,
            fg_color: str | Tuple[str] | None = PRIMARY_COLOR,
            border_color: str | Tuple[str] | None = ACCENT_COLOR,
            animation_steps: int = 10,
            anchor: str = 'nw',
            entry_font: ctk.CTkFont = None,
            button_font: ctk.CTkFont = None,
            save_file: Callable[[str], None] = lambda path : ()
        ):
        super().__init__(master, rel_start, rel_end, rel_width, rel_height, corner_radius, border_width, fg_color, border_color, animation_steps, anchor)
        self.columnconfigure((0, 1), weight = 1, uniform='a')
        self.rowconfigure((0, 1, 2), weight = 2, uniform='a')
        # Widgets
        self.save_file = save_file
        self.file_input = FileNameInput(self, font=entry_font)
        self.dir_input = FilePathInput(self, font=entry_font, button_font=button_font)
        accept_button = custom_button(self, text=ACCEPT, font=button_font, command=self.export_file, hover_color=ACCEPT_COLOR)
        cancel_button = custom_button(self, text=CANCEL, font=button_font, command=self.move, hover_color=CANCEL_COLOR)
        # Grid placement
        self.file_input.grid(row = 0, column = 0, columnspan=2, sticky = 'nsew', padx = PADX, pady = PADY)
        self.dir_input.grid(row = 1, column = 0, columnspan=2, sticky = 'new', padx = PADX, pady = PADY)
        accept_button.grid(row = 2, column = 0, sticky = 'sew', padx = PADX, pady = PADY)
        cancel_button.grid(row = 2, column = 1, sticky = 'sew', padx = PADX, pady = PADY)

    def export_file(self):
        file_name = self.file_input.get_file_name()
        if not file_name:
            self.quick_move()
            return
        file_directory = self.dir_input.get_directory_path() or '.'
        self.save_file(f'{file_directory}/{file_name}')
        self.quick_move()