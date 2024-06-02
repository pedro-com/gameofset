import os

os.chdir("app")
from app_content.app_manager import App

content_window = App(is_min_size=True)
content_window.mainloop()
"""
window = tk.Tk()
window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
window.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)
window.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)

window.title('The Game of SET')
window.configure(background = BACKGROUND_COLOR)
header = Header(window, title_name='The Game of SET')
content = GamePanel(window)

header.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.15)
content.place(relx = 0, rely = 0.15, relwidth = 1, relheight = 0.85)

window.mainloop()"""
