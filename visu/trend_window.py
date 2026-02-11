from tkinter import Toplevel, BOTH, BOTTOM, TOP, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from matplotlib.pyplot import get_cmap

middle_font_size = 9
small_font_size = 8


class Trend:
    def __init__(self, x_data: list = None, y_data: list = None, name: str = None, show_flag: bool = False):
        self._all_data = []
        if name is not None and x_data is not None and y_data is not None:
            self.add_data(x_data, y_data, name)
            if show_flag:
                self.show()

    def add_data(self, x_data: list, y_data: list, name: str):
        self._all_data.append((x_data, y_data, name))

    def show(self, title: str = None, separately: bool = True):
        try:
            if len(self._all_data) == 0:
                raise Exception('Нет данных для графика')

            top_level = Toplevel()
            figure = Figure(figsize=(12, 8))
            figure.patch.set_facecolor((0.941, 0.941, 0.941))

            separately &= len(self._all_data) > 1

            if separately:
                axes_list = figure.subplots(len(self._all_data), sharex=True)
            else:
                axes_list = [figure.add_subplot()]
            axes = axes_list[0]

            y_lab = ''
            cmap = get_cmap("tab10")

            for index, data in enumerate(self._all_data):
                if separately:
                    axes = axes_list[index]
                    axes.set_ylabel(data[2], fontsize=middle_font_size)
                    axes.grid()
                axes.plot(data[0], data[1], label=data[2], color=cmap(index))
                y_lab += f'{data[2]}; '

            if not separately:
                axes.set_ylabel(y_lab, fontsize=middle_font_size)
                axes.grid()
                if len(self._all_data) > 1:
                    figure.legend(loc="upper right")

            axes.tick_params(axis='x', labelsize=small_font_size)

            formatter = DateFormatter('%d.%m.%Y\n%H:%M:%S.%f')
            axes.xaxis.set_major_formatter(formatter)

            if title is None or title.strip() == '':
                title = y_lab

            figure.suptitle(title)
            # figure.autofmt_xdate()
            figure.tight_layout()

            canvas = FigureCanvasTkAgg(figure, top_level)
            canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

            toolbar = NavigationToolbar2Tk(canvas, top_level)
            toolbar.update()
            canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

            top_level.title(title)

        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка при построении графика {title}: {str(e)}')
