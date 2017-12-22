import tkinter as tk
from tkinter import ttk

import asyncio

import time

from add_employee_component import AddEmployeeComponent
from models import Base, engine
from models.employee import Employee
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

    def set_widgets(self):
        self.load_button = ttk.Button(self, text='Загрузить таблицу', command=self.update_table_data)
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
        self.load_button.grid(row=2, column=2, padx=20, pady=20, sticky=tk.NSEW)

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
        number = Employee.number_employees()
        part1 = 0
        part2 = number / 5 + part1
        part3 = number / 5 + part2
        part4 = number / 5 + part3
        part5 = number / 5 + part4
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            asyncio.gather(
                Employee.get_list(offset=part1),
                Employee.get_list(offset=part2),
                Employee.get_list(offset=part3),
                Employee.get_list(offset=part4),
                Employee.get_list(offset=part5),
            )
        )
        loop.run_until_complete(
            asyncio.gather(
                self.build_table_part(result[0]),
                self.build_table_part(result[1]),
                self.build_table_part(result[2]),
                self.build_table_part(result[3]),
                self.build_table_part(result[4]),
            )
        )
        loop.close()

    async def build_table_part(self, employees):
        for employee in employees:
            await self.table.build_raw(
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


async def async_generator(generator):
    for item in generator:
        yield item


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    app = Application()
    app.mainloop()
