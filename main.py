import datetime
import threading
from tkinter import Tk, messagebox

import matplotlib

from visu.elements.scrolled_frame import ScrolledFrame
from visu.main_panel import MainPanel
from visu.trend_window import Trend

matplotlib.use('TkAgg')

plot_dict = {}

win_width = 900
win_height = 900

version = "1.0"

def main():
    # append_plot_dict('records/ПЛК/Переменная 1/05.02.2026 11-37-43-605 total 3600.trnd')
    # append_plot_dict('records/ПЛК/Переменная 1/05.02.2026 11-30-24-997 total 3600.trnd')
    # append_plot_dict('records/ПЛК/Переменная 1/05.02.2026 11-44-59-563 total 3600.trnd')
    # append_plot_dict('records/ПЛК/Переменная 1/05.02.2026 11-52-12-944 total 3600.trnd')
    # append_plot_dict('records/ПЛК/Переменная 2/05.02.2026 11-30-24-999 total 3600.trnd')
    # append_plot_dict('records/ПЛК/Переменная 9/05.02.2026 11-37-43-677 total 3600.trnd')
    # append_plot_dict('records/ПЛК/Переменная 10/05.02.2026 11-30-25-015 total 3600.trnd')
    window = Tk()
    title = 'PLC data visu'
    title_with_version = f'{title}, v{version}'
    window.geometry(f'{win_width}x{win_height}')
    window.title(title_with_version)
    window.resizable(False, False)
    # trend = Trend(window)
    # for key, val in plot_dict.items():
    #     x_list, y_list = get_xy(val)
    #     trend.add_data(x_list, y_list, key)
    #
    # trend.show()

    frame_with_scroll = ScrolledFrame(window, height=win_height, width=win_width)
    main_panel = MainPanel(frame_with_scroll.canvas)
    frame_with_scroll.setMainPanel(main_panel)

    def on_close():
        if messagebox.askokcancel('Выход', 'Закрыть приложение?'):
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", lambda: threading.Thread(target=on_close, daemon=True).start())

    window.mainloop()


if __name__ == '__main__':
    main()
