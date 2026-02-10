from tkinter import Toplevel, BOTH, BOTTOM, TOP

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class Trend:
    def __init__(self, x_data: list = None, y_data: list = None, name: str = None, show_flag: bool = False):
        self._all_data = []
        if name is not None and x_data is not None and y_data is not None:
            self.add_data(x_data, y_data, name)
            if show_flag:
                self.show()

    def add_data(self, x_data: list, y_data: list, name: str):
        self._all_data.append((x_data, y_data, name))

    def show(self, title: str = None, separately: bool = False):
        # self._all_data = [([1, 2, 3], [100, 200, 300], 'var1'), ([1, 2.5, 3], [400, 600, 500], 'var2'), ([1, 1.6, 3], [1000, 900, 100], 'var3'), ([1, 2.2, 3], [0, 2, 3], 'var4')]
        top_level = Toplevel()
        figure = Figure(figsize=(12, 8), dpi=100)
        if separately:
            axes = figure.subplots(len(self._all_data), 1, sharex=True)
        else:
            axes = figure.add_subplot()
        y_lab = ''
        for index, data in enumerate(self._all_data):
            if separately:
                axes[index].plot(data[0], data[1], label=data[2])
                axes[index].set_xlabel('Время')
                axes[index].set_ylabel(data[2])
                axes[index].grid()
                axes[index].set_ylabel(data[2])
            else:
                axes.plot(data[0], data[1], label=data[2])
            # axes.set_ylabel(data[2])
            # axes.yaxis.label.set_color(colors[index])
            # axes.tick_params(axis='y', colors=colors[index])
            y_lab += f'{data[2]}; '

        if not separately:
            axes.set_xlabel('Время')
            axes.set_ylabel(y_lab)
            axes.grid()
            figure.legend(loc="upper right")

        if title is None:
            title = y_lab

        figure.suptitle(title)
        figure.autofmt_xdate()
        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, top_level)
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, top_level)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

        top_level.title(title)
