import tkinter as tk
from tkinter import ttk

from add_employee_component import AddEmployeeComponent
from config import UKRAINIAN_LANGUAGE, set_language, RUSSIAN_LANGUAGE, get_language
from models import Base, engine
from models.employee import Employee
from services.localization.localization import translate_
from table import Table


TABLE_HEADERS = [
    {'column': 'employee', 'name': 'Сотрудник'},
    {'column': 'department', 'name': 'Подразделение'},
]


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky=tk.NSEW)

        self.set_widgets()
        self.grid_widgets()

        top = self.winfo_toplevel()
        top.grid_rowconfigure(0, weight=1)
        top.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.update_table_data()

    def set_widgets(self):
        self.entry = ttk.Entry(self, font="Helvetica 14")
        self.button = ttk.Button(self, text=translate_('search'), command=self.on_search)
        self.change_language_button = ttk.Button(self, text=translate_('change_language'), command=self.change_language)
        self.table = Table(headers=TABLE_HEADERS, master=self)
        self.add_employee_button = ttk.Button(
            self,
            text=translate_('add_new_employee'),
            command=self.create_add_employee_window,
        )

    def grid_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')

        self.entry.grid(row=0, column=0, padx=20, sticky=tk.EW)
        self.button.grid(row=0, column=1, padx=20, pady=10, sticky=tk.EW)
        self.change_language_button.grid(row=1, column=2, padx=20, pady=10, sticky=tk.EW)
        self.add_employee_button.grid(row=0, column=2, padx=20, pady=10, sticky=tk.EW)
        self.table.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky=tk.NSEW)

    def on_search(self):
        search_text = self.entry.get()
        self.table.clear()
        for employee in Employee.get_list():
            if search_text in employee.subdivision.name:
                self.table.build_raw(
                    employee.id,
                    f'{employee.last_name} {employee.first_name}',
                    employee.subdivision.name,
                )

    def update_table_data(self):
        for employee in Employee.get_list():
            self.table.build_raw(
                employee.id,
                f'{employee.last_name} {employee.first_name}',
                employee.subdivision.name,
            )

    def add_table_data(self, employee):
        self.table.build_raw(
            employee.id,
            f'{employee.last_name} {employee.first_name}',
            employee.subdivision.name,
        )

    def create_add_employee_window(self):
        self.add_employee_component = AddEmployeeComponent(self)
        self.add_employee_component.mainloop()

    def change_language(self):
        language = RUSSIAN_LANGUAGE if get_language() == UKRAINIAN_LANGUAGE else UKRAINIAN_LANGUAGE
        set_language(language)
        self.destroy_and_rebuild()
        self.update_table_data()

    def destroy_and_rebuild(self):
        for child in self.winfo_children():
            child.destroy()
        self.set_widgets()
        self.grid_widgets()


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    app = Application()
    app.mainloop()
