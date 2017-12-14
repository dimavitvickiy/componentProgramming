import tkinter as tk
from tkinter import ttk

from models.employee import Employee
from models.subdivision import Subdivision


class AddEmployeeComponent(tk.Toplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title('Добавить нового сотрудника')

        self.set_widgets()
        self.grid_widgets()

    def set_widgets(self):
        self.last_name_label = ttk.Label(self, text='Фамилия: ')
        self.last_name_entry = ttk.Entry(self, font="Helvetica 14")
        self.first_name_label = ttk.Label(self, text='Имя: ')
        self.first_name_entry = ttk.Entry(self, font="Helvetica 14")
        self.subdivision_name_label = ttk.Label(self, text='Подразделение: ')
        self.subdivision_name_select = tk.Listbox(self, font="Helvetica 14")
        self.fill_select_items()
        self.error_message = ttk.Label(self, text="Все поля должны быть заполнены", font="Helvetica 14")
        self.save_button = ttk.Button(self, text='Сохранить', command=self.on_save)

    def grid_widgets(self):
        self.last_name_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.last_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)
        self.first_name_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)
        self.subdivision_name_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.subdivision_name_select.grid(row=2, column=1, padx=10, pady=10, sticky=tk.EW)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)

    def fill_select_items(self):
        for subdivision in Subdivision.get_list():
            self.subdivision_name_select.insert(tk.END, subdivision.name)

    def show_error(self):
        self.error_message.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)

    def on_save(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        subdivision_index = self.subdivision_name_select.curselection()
        subdivision_name = self.subdivision_name_select.get(subdivision_index)
        subdivision = Subdivision.get_entity(name=subdivision_name)

        if self.validate_form_data(first_name, last_name, subdivision):
            new_employee = Employee.create(first_name, last_name, subdivision)
            self.master.add_table_data(new_employee)
            self.destroy()
        else:
            self.show_error()

    @staticmethod
    def validate_form_data(first_name, last_name, subdivision):
        return first_name and last_name and subdivision is not None
