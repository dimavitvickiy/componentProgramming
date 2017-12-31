import pickle
import tkinter as tk
from tkinter import ttk

import asyncio
from tkinter.ttk import Notebook

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

    def set_widgets(self):
        self.load_button = ttk.Button(self, text='Загрузить таблицу', command=self.update_table_data)
        self.entry = ttk.Entry(self, font="Helvetica 14")
        try:
            with open('cache.pickle', 'rb') as f:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, pickle.load(f))
        except FileNotFoundError:
            pass
        self.button = ttk.Button(self, text=translate_('search'), command=self.on_search)
        self.change_language_button = ttk.Button(self, text=translate_('change_language'), command=self.change_language)
        self.serialize_button = ttk.Button(self, text='Сериализировать данные', command=self.serialize)
        self.table = Table(headers=TABLE_HEADERS, master=self)
        self.add_employee_button = ttk.Button(
            self,
            text=translate_('add_new_employee'),
            command=self.create_add_employee_window,
        )

    def grid_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        self.serialize_button.grid(row=1, column=1)
        self.entry.grid(row=0, column=0, padx=20, sticky=tk.EW)
        self.button.grid(row=0, column=1, padx=20, pady=10, sticky=tk.EW)
        self.change_language_button.grid(row=1, column=2, padx=20, pady=10, sticky=tk.EW)
        self.add_employee_button.grid(row=0, column=2, padx=20, pady=10, sticky=tk.EW)
        self.table.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky=tk.NSEW)
        self.load_button.grid(row=2, column=2, padx=20, pady=20, sticky=tk.NSEW)

    def on_search(self):
        search_text = self.entry.get()
        self.table.clear()
        number = Employee.number_employees()
        part1 = 0
        part2 = number / 5 + part1
        part3 = number / 5 + part2
        part4 = number / 5 + part3
        part5 = number / 5 + part4
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            asyncio.gather(
                Employee.get_list(offset=part1),
                Employee.get_list(offset=part2),
                Employee.get_list(offset=part3),
                Employee.get_list(offset=part4),
                Employee.get_list(offset=part5),
            )
        )
        employees = []
        for res in results:
            employees.extend(res)
        for employee in employees:
            if search_text in employee.subdivision.name:
                self.table.build_raw(
                    employee.id,
                    f'{employee.last_name} {employee.first_name}',
                    employee.subdivision.name,
                )

    def serialize(self):
        with open('cache.pickle', 'wb') as f:
            pickle.dump(self.entry.get(), f)

    def update_table_data(self):
        self.table.clear()
        number = Employee.number_employees()
        part1 = 0
        part2 = number / 5 + part1
        part3 = number / 5 + part2
        part4 = number / 5 + part3
        part5 = number / 5 + part4
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            asyncio.gather(
                Employee.get_list(offset=part1),
                Employee.get_list(offset=part2),
                Employee.get_list(offset=part3),
                Employee.get_list(offset=part4),
                Employee.get_list(offset=part5),
            )
        )
        for result in results:
            self.build_table_part(result)

    def build_table_part(self, employees):
        for employee in employees:
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


async def async_generator(generator):
    for item in generator:
        yield item


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    root = tk.Tk()
    note = Notebook(root)
    tab1 = Application(note)
    tab2 = tk.Frame(note)
    note.add(tab1, text='Main app')
    note.add(tab2, text='Additional tab')
    note.grid()
    root.mainloop()
