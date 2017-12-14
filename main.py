import tkinter as tk
from tkinter import ttk

from add_employee_component import AddEmployeeComponent
from models.employee import EmployeeDB
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
        self.button = ttk.Button(self, text='Поиск', command=self.on_search)
        self.table = Table(headers=TABLE_HEADERS, master=self)
        self.add_employee_button = ttk.Button(
            self,
            text='Добавить',
            command=self.create_add_employee_window,
        )

    def grid_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')

        self.entry.grid(row=0, column=0, padx=20, sticky=tk.EW)
        self.button.grid(row=0, column=1, padx=20, pady=10, sticky=tk.EW)
        self.add_employee_button.grid(row=0, column=2, padx=20, pady=10, sticky=tk.EW)
        self.table.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky=tk.NSEW)

    def on_search(self):
        search_text = self.entry.get()
        self.table.clear()
        for employee in EmployeeDB.get_list():
            if search_text in employee.subdivision:
                self.table.build_raw(
                    employee.id,
                    '{} {}'.format(employee.last_name, employee.first_name),
                    employee.subdivision,
                )

    def update_table_data(self):
        for employee in EmployeeDB.get_list(first_name='Дмитрий', last_name='Витвицкий'):
            self.table.build_raw(
                employee.id,
                '{} {}'.format(employee.last_name, employee.first_name),
                employee.subdivision,
            )

    def add_table_data(self, employee):
        self.table.build_raw(
            employee.id,
            '{} {}'.format(employee.last_name, employee.first_name),
            employee.subdivision,
        )

    def create_add_employee_window(self):
        self.add_employee_component = AddEmployeeComponent(self)
        self.add_employee_component.mainloop()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
