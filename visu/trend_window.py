from tkinter import Toplevel, BOTH, BOTTOM, TOP

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class Trend:
    def __init__(self, master, x_data: list = None, y_data: list = None, name: str = None, show_flag: bool = False):
        self._all_data = []
        self.master = master
        if name is not None and x_data is not None and y_data is not None:
            self.add_data(x_data, y_data, name)
            if show_flag:
                self.show()

    def add_data(self, x_data: list, y_data: list, name: str):
        self._all_data.append((x_data, y_data, name))

    def show(self):
        top_level = Toplevel(master=self.master)
        figure = Figure(figsize=(12, 8), dpi=100)
        axes = figure.add_subplot()

        axes.set_xlabel('время')
        axes.set_ylabel('значение')
        axes.xaxis.grid()
        axes.yaxis.grid()
        title = ''
        for data in self._all_data:
            axes.plot(data[0], data[1], label=data[2])
            title += data[2]

        figure.autofmt_xdate()
        figure.tight_layout()
        figure.legend(loc="upper right")

        canvas = FigureCanvasTkAgg(figure, top_level)
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, top_level)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

        top_level.title(title)
