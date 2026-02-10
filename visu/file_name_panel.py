from tkinter import ttk, LEFT, messagebox, RIGHT


class FileNamePanel(ttk.Frame):
    def __init__(self, parent, file_name: str, delete_action=lambda fnp: 0):
        ttk.Frame.__init__(self, parent, relief='solid')

        self.file_name = file_name

        def delete_command():
            if not messagebox.askyesno('Вопрос', f'Удалить строку "{file_name}"?'):
                return
            delete_action(self)
            self.destroy()

        file_name_label_text = file_name
        if len(file_name) > 140:
            file_name_label_text = f'{file_name[:70]}...{file_name[len(file_name) - 70:]}'

        file_name_label = ttk.Label(self, text=file_name_label_text)
        delete_button = ttk.Button(self, text='- Удалить -', command=delete_command)

        file_name_label.pack(side=LEFT, padx=1)
        delete_button.pack(side=RIGHT)
