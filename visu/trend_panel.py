from tkinter import ttk, messagebox, BOTTOM, StringVar, TOP, BOTH
from tkinter.filedialog import askopenfilename

from ordered_set import OrderedSet

from misc.file_work import get_data_from_file
from visu.file_name_panel import FileNamePanel
from visu.trend_window import Trend


def _get_xy(items):
    x_list = []
    y_list = []
    for item in items:
        x_list.append(item[0])
        y_list.append(item[1])
    return x_list, y_list


def _sort_fun(item):
    return item[0]


class TrendPanel(ttk.Frame):
    def __init__(self, parent, name='График', delete_action=lambda tp: 0, update_main_panel_action=lambda: 0):
        ttk.Frame.__init__(self, parent, padding=10, relief='solid')

        self._plot_dict = {}
        self.update_main_panel_action = update_main_panel_action

        self._file_name_panels = OrderedSet()

        self._name_var = StringVar()
        self._name_var.set(name)
        name_entry = ttk.Entry(self, textvariable=self._name_var)

        def delete_command():
            if not messagebox.askyesno('Вопрос', f'Удалить график "{name}"?'):
                return
            delete_action(self)
            self._remove_all_file_names(ask_flag=False)
            self.destroy()

        button_frame = ttk.Frame(self)
        self.add_file_button = ttk.Button(button_frame, text='+ Добавить файлы +', command=self._add_command)
        self.remove_all_file_names_button = ttk.Button(button_frame, text='- Очистить список файлов -',
                                                  command=self._remove_all_file_names)
        self.build_trend_button = ttk.Button(button_frame, text='Построить график', command=self.build_trend)
        self.remove_trend_button = ttk.Button(button_frame, text='- Удалить график -', command=delete_command)

        name_entry.pack(side=TOP, pady=5)
        button_frame.pack(side=BOTTOM, pady=5)
        self.add_file_button.grid(row=0, column=0, sticky='EW')
        self.remove_all_file_names_button.grid(row=0, column=1, sticky='EW')
        self.build_trend_button.grid(row=1, column=0, sticky='EW')
        self.remove_trend_button.grid(row=1, column=1, sticky='EW')

        self._update_buttons()

    def _add_command(self):
        file_names = askopenfilename(multiple=True, filetypes=(("Файлы трендов", "*.trnd"), ))
        for file_name in file_names:
            if file_name in map(lambda i: i.file_name, self._file_name_panels):
                print(True)
                continue

            def delete_action(fnp):
                self._file_name_panels.remove(fnp)
                self._update_buttons()

            file_name_panel = FileNamePanel(parent=self, file_name=file_name, delete_action=delete_action)

            self._file_name_panels.add(file_name_panel)
            file_name_panel.pack(fill=BOTH, pady=2)
        self._update_buttons()

    def _remove_all_file_names(self, ask_flag=True):
        if ask_flag and not messagebox.askyesno('Вопрос', 'Очистить список файлов?'):
            return
        for file_name_panel in self._file_name_panels:
            file_name_panel.destroy()
        self._file_name_panels.clear()
        self._update_buttons()

    def get_name(self):
        return self._name_var.get()

    def _append_plot_dict(self, file_name: str):
        data, error = get_data_from_file(file_name)
        if error != '':
            messagebox.showerror('Ошибка', error)
            return error
        try:
            name = f"{data['ПЛК']}/{data['Переменная']}"
            if name not in self._plot_dict:
                self._plot_dict[name] = []

            for i in data['values']:
                self._plot_dict[name].append(i)

            self._plot_dict[name].sort(key=_sort_fun)
        except Exception as e:
            error = str(e)
        return error

    def build_trend(self):
        if self._file_name_panels == 0:
            return

        self._plot_dict.clear()

        for file_name_panel in self._file_name_panels:
            self._append_plot_dict(file_name_panel.file_name)

        if len(self._plot_dict) == 0:
            return

        trend = Trend()
        for key, val in self._plot_dict.items():
            x_list, y_list = _get_xy(val)
            trend.add_data(x_list, y_list, key)

        trend.show(title=self._name_var.get())

    def _update_buttons(self):
        st = 'normal' if len(self._file_name_panels) > 0 else 'disable'
        self.remove_all_file_names_button.config(state=st)
        self.build_trend_button.config(state=st)
        self.update_main_panel_action()

    def is_empty(self):
        return len(self._file_name_panels) == 0
