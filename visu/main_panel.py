import re
from tkinter import ttk, X, messagebox, BOTTOM

from ordered_set import OrderedSet

from misc.file_work import save_config, read_config
from visu.trend_panel import TrendPanel


class MainPanel(ttk.Frame):
    def __init__(self, parent, title: str):
        ttk.Frame.__init__(self, parent)

        self._trend_panels_frame = ttk.Frame(self, relief='solid', padding=5)
        title_label = ttk.Label(self._trend_panels_frame, text='Графики:')

        self._trend_panels = OrderedSet()
        self.title = title

        buttons_frame = ttk.Frame(self, padding=10)
        self.add_trend_button = ttk.Button(buttons_frame, text='+ Добавить график +', command=self._add_new_trend)
        self.delete_trends_button = ttk.Button(buttons_frame, text='- Удалить все графики -', command=self._delete_all_trends)
        self.build_trend = ttk.Button(buttons_frame, text='Построить все графики', command=self._build_all_trends)

        self._trend_panels_frame.pack(fill=X)
        title_label.pack()

        buttons_frame.pack(side=BOTTOM)
        self.add_trend_button.grid(row=0, column=0)
        self.delete_trends_button.grid(row=0, column=1)
        self.build_trend.grid(row=1, column=0, columnspan=2, sticky='EW')

        config, error = read_config(f'{title}.cfg')
        if error == '':
            try:
                for key, value in config.items():
                    self._add_trend(key, value)
            except Exception as e:
                error = str(e)
        if error != '':
            messagebox.showerror('Ошибка',  f'Ошибка при чтении {title}.cfg: {error}')

        self._update_delete_trends_button()
        self._update_build_all_button()

    def _add_new_trend(self):
        trend_name = 'График'

        if len(self._trend_panels) > 0:
            trend_name = self._trend_panels[-1].get_name()
        search_result = re.search('\\d+$', trend_name)
        if search_result is None:
            trend_name += ' 1'
        else:
            index = int(search_result.group()) + 1
            trend_name = trend_name[:search_result.start()] + str(index)

        self._add_trend(trend_name)

    def _add_trend(self, trend_name, config=None):
        def delete_action(tp):
            self._trend_panels.remove(tp)
            self._update_delete_trends_button()
            self._update_build_all_button()

        trend_panel = TrendPanel(parent=self._trend_panels_frame, name=trend_name,
                                 delete_action=delete_action, update_main_panel_action=self._update_build_all_button,
                                 config=config)
        self._trend_panels.add(trend_panel)
        trend_panel.pack(fill=X, pady=5)
        self._update_delete_trends_button()
        self._update_build_all_button()

    def _delete_all_trends(self):
        if not messagebox.askyesno('Вопрос', 'Удалить все графики?'):
            return
        for trend_panel in self._trend_panels:
            trend_panel.destroy()
        self._trend_panels.clear()
        self._update_delete_trends_button()
        self._update_build_all_button()

    def _build_all_trends(self):
        if not messagebox.askyesno('Вопрос', 'Построить все графики?'):
            return
        for trend_panel in self._trend_panels:
            trend_panel.build_trend()

    def _update_delete_trends_button(self):
        self.delete_trends_button.config(state='normal' if len(self._trend_panels) > 0 else 'disable')

    def _update_build_all_button(self):
        empty = True
        for trend_panel in self._trend_panels:
            empty &= trend_panel.is_empty()
        self.build_trend.config(state='disable' if empty else 'normal')

    def on_close(self):
        result = {}
        for trend_panel in self._trend_panels:
            result[trend_panel.get_name()] = (trend_panel.get_file_names(), trend_panel.get_separate())
        error = save_config(f'{self.title}.cfg', result)
        if error != '':
            messagebox.showerror('Ошибка', f'Ошибка при чтении {self.title}.cfg: {error}')
