import tkinter as tk
from tkinter import ttk


class Table(ttk.Treeview):
    def __init__(self, headers, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.__index = 0
        self.build_headers(headers)

    def build_headers(self, headers=None):
        if headers is None:
            headers = []
        self['columns'] = tuple(header['column'] for header in headers)
        for header in headers:
            self.column(header['column'], width=300, anchor=tk.CENTER)
            self.heading(header['column'], text=header['name'])

    def build_raw(self, *values):
        self.insert('', self.__index, text=values[0], values=tuple(values[1:]))
        self.__index += 1

    def clear(self):
        for row in self.get_children():
            self.delete(row)
