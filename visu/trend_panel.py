from tkinter import ttk, LEFT, messagebox, BOTTOM, X
from tkinter.filedialog import askopenfilename

from ordered_set import OrderedSet

from visu.file_name_panel import FileNamePanel


class TrendPanel(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding=10, relief='solid')

        self.file_name_panels = OrderedSet()

        button_frame = ttk.Frame(self)
        add_file_button = ttk.Button(button_frame, text='Добавить файл', command=self._add_command)
        remove_all_button = ttk.Button(button_frame, text='Удалить файлы из списка', command=self._remove_all)

        button_frame.pack(side=BOTTOM)
        add_file_button.pack(side=LEFT)
        remove_all_button.pack(side=LEFT)

    def _add_command(self):
        file_names = askopenfilename(multiple=True, filetypes=(("Файлы трендов", "*.trnd"), ))
        for file_name in file_names:
            if file_name in map(lambda i: i.file_name, self.file_name_panels):
                print(True)
                continue
            file_name_panel = FileNamePanel(self, file_name,
                                            delete_action=lambda fnp: self.file_name_panels.remove(fnp))
            self.file_name_panels.add(file_name_panel)
            file_name_panel.pack()

    def _remove_all(self):
        if not messagebox.askyesno('Вопрос', 'Очистить список файлов?'):
            return
        for file_name_panel in self.file_name_panels:
            file_name_panel.destroy()
        self.file_name_panels.clear()
