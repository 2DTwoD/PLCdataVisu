from tkinter import ttk, LEFT, messagebox, BOTTOM, X, CENTER, StringVar, TOP
from tkinter.filedialog import askopenfilename

from ordered_set import OrderedSet

from misc.plot_dict_work import append_plot_dict, get_xy
from visu.file_name_panel import FileNamePanel
from visu.trend_window import Trend


class TrendPanel(ttk.Frame):
    def __init__(self, parent, name='График'):
        ttk.Frame.__init__(self, parent, padding=10, relief='solid')

        self._plot_dict = {}

        self._file_name_panels = OrderedSet()

        self._name_var = StringVar()
        self._name_var.set(name)
        name_entry = ttk.Entry(self, textvariable=self._name_var)

        button_frame = ttk.Frame(self)
        add_file_button = ttk.Button(button_frame, text='Добавить файл', command=self._add_command)
        remove_all_file_names_button = ttk.Button(button_frame, text='Удалить файлы из списка', command=self._remove_all_file_names)
        build_trend_button = ttk.Button(button_frame, text='Построить график', command=self.build_trend)
        remove_trend_button = ttk.Button(button_frame, text='Удалить график', command=self.remove_trend)

        name_entry.pack(side=TOP, pady=5)
        button_frame.pack(side=BOTTOM, pady=5)
        add_file_button.pack(side=LEFT)
        remove_all_file_names_button.pack(side=LEFT)
        build_trend_button.pack(side=LEFT)
        remove_trend_button.pack(side=LEFT)

    def _add_command(self):
        file_names = askopenfilename(multiple=True, filetypes=(("Файлы трендов", "*.trnd"), ))
        for file_name in file_names:
            if file_name in map(lambda i: i.file_name, self._file_name_panels):
                print(True)
                continue
            file_name_panel = FileNamePanel(self, file_name,
                                            delete_action=lambda fnp: self._file_name_panels.remove(fnp))
            self._file_name_panels.add(file_name_panel)
            file_name_panel.pack()

    def _remove_all_file_names(self, ask_flag=True):
        if ask_flag and not messagebox.askyesno('Вопрос', 'Очистить список файлов?'):
            return
        for file_name_panel in self._file_name_panels:
            file_name_panel.destroy()
        self._file_name_panels.clear()

    def remove_trend(self, ask_flag=True):
        if ask_flag and not messagebox.askyesno('Вопрос', 'Удалить график?'):
            return
        self._remove_all_file_names(ask_flag=False)
        self.destroy()

    def get_name(self):
        return self._name_var.get()

    def build_trend(self):
        if self._file_name_panels == 0:
            return

        for file_name_panel in self._file_name_panels:
            append_plot_dict(self._plot_dict, file_name_panel.file_name)

        trend = Trend()
        for key, val in self._plot_dict.items():
            x_list, y_list = get_xy(val)
            trend.add_data(x_list, y_list, key)

        trend.show()
