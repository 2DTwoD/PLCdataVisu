import threading
from tkinter import Tk, messagebox

import matplotlib

from visu.elements.scrolled_frame import ScrolledFrame
from visu.main_panel import MainPanel

matplotlib.use('TkAgg')
# matplotlib.rc('font', size=9)

win_width = 900
win_height = 900

version = "1.0"


def main():
    window = Tk()
    title = 'PLC data visu'
    title_with_version = f'{title}, v{version}'
    window.geometry(f'{win_width}x{win_height}')
    window.title(title_with_version)
    window.resizable(False, False)

    frame_with_scroll = ScrolledFrame(window, height=win_height, width=win_width)
    main_panel = MainPanel(frame_with_scroll.canvas, title)
    frame_with_scroll.setMainPanel(main_panel)

    def on_close():
        if messagebox.askokcancel('Выход', 'Закрыть приложение?'):
            main_panel.on_close()
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", lambda: threading.Thread(target=on_close, daemon=True).start())

    window.mainloop()


if __name__ == '__main__':
    main()
