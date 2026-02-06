from tkinter import ttk, LEFT, BOTH, messagebox


class FileNamePanel(ttk.Frame):
    def __init__(self, parent, file_name: str, delete_action=lambda fnp: 0):
        ttk.Frame.__init__(self, parent, padding=5, relief='solid')

        self.file_name = file_name


        def delete_command():
            if not messagebox.askyesno('Вопрос', f'Удалить строку "{file_name}"?'):
                return
            delete_action(self)
            self.destroy()

        file_name_label = ttk.Label(self, text=f'{file_name}')
        delete_button = ttk.Button(self, text='Удалить', command=delete_command)

        file_name_label.pack(side=LEFT, fill=BOTH)
        delete_button.pack(side=LEFT, fill=BOTH)
