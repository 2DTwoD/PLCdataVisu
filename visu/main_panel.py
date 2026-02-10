import re
from tkinter import ttk, X, LEFT, messagebox, BOTTOM

from ordered_set import OrderedSet

from visu.trend_panel import TrendPanel


class MainPanel(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.trend_panels_frame = ttk.Frame(self, relief='solid', padding=5)
        title_label = ttk.Label(self.trend_panels_frame, text='Графики:', foreground='gray')

        self.trend_panels = OrderedSet()

        buttons_frame = ttk.Frame(self, padding=10)
        add_trend_button = ttk.Button(buttons_frame, text='Добавить график', command=self._add_trend)
        build_trend = ttk.Button(buttons_frame, text='Построить все графики', command=self._build_all_trends)
        delete_trends_button = ttk.Button(buttons_frame, text='Удалить все графики', command=self._delete_all_trends)

        self.trend_panels_frame.pack(fill=X)
        title_label.pack()

        buttons_frame.pack(side=BOTTOM)
        add_trend_button.pack(side=LEFT)
        build_trend.pack(side=LEFT)
        delete_trends_button.pack(side=LEFT)

    def _add_trend(self):
        trend_name = 'График'
        if len(self.trend_panels) > 0:
            trend_name = self.trend_panels[-1].get_name()
        search_result = re.search('\\d+$', trend_name)
        if search_result is None:
            trend_name += ' 1'
        else:
            index = int(search_result.group()) + 1
            trend_name = trend_name[:search_result.start()] + str(index)
        trend_panel = TrendPanel(self.trend_panels_frame, trend_name, lambda tp: self.trend_panels.remove(tp))
        self.trend_panels.add(trend_panel)
        trend_panel.pack(fill=X, pady=5)

    def _delete_all_trends(self):
        if not messagebox.askyesno('Вопрос', 'Очистить список трендов?'):
            return
        for trend_panel in self.trend_panels:
            trend_panel.destroy()
        self.trend_panels.clear()

    def _build_all_trends(self):
        for trend_panel in self.trend_panels:
            trend_panel.build_trend()
