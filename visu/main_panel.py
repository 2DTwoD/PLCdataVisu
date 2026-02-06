from tkinter import ttk, X

from ordered_set import OrderedSet

from visu.trend_panel import TrendPanel


class MainPanel(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.trend_panels_frame = ttk.Frame(self)

        self.trend_panels = OrderedSet()

        add_trend_button = ttk.Button(self, text='Добавить график', command=self._add_trend)

        self.trend_panels_frame.pack(fill=X)
        add_trend_button.pack()

    def _add_trend(self):
        trend_panel = TrendPanel(self.trend_panels_frame)
        self.trend_panels.add(trend_panel)
        trend_panel.pack()
