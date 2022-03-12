import wx
import re
import functools
from recipes.gui.form.framework import PaddedBox
from recipes.gui.form.framework import FlexGridSizer

class RowWiseForm:
    def __init__(self, parent, row_factory_class):
        self.parent = parent
        self.rows = []
        self.factory = row_factory_class(parent)
        self.fgs = None

    def ncols(self):
        return len(self.rows[0]) if len(self.rows) > 0 else 0

    def __getattr__(self, name):
        match = re.match('(insert|append)_(.*)', name)

        if not match: raise AttributeError(name)

        return getattr(self, match[1])(match[2])

    def append(self, factory_method_name):
        def append(*args, **kwargs):
            row = getattr(self.factory, factory_method_name)(*args, **kwargs)
            self.append_row(row)
        return append

    def insert(self, factory_method_name):
        def insert(index, *args, **kwargs):
            row = getattr(self.factory, factory_method_name)(*args, **kwargs)
            self.insert_row(index, row)
        return insert

    def append_row(self, row):
        self.rows.append(row)
        if self.fgs:
            self.fgs.AddMany(row)
            self.fgs.Layout()

    def insert_row(self, index, row):
        if index < 0: index = index + len(self.rows)
        self.rows.insert(index, row)
        if self.fgs:
            item_index = index * self.ncols()
            for item in reversed(row):
                self.fgs.Insert(item_index, *item)
                self.fgs.normalize_tab_order_for_window_at_index(item_index)
            self.fgs.Layout()

    def create_grid(self):
        if self.fgs: return self.fgs

        self.fgs = FlexGridSizer(cols = self.ncols(), vgap = 10, hgap = 10)
        flatten_rows = lambda flattened, row: [*flattened, *row]
        flattened_ros = functools.reduce(flatten_rows, self.rows, [])
        self.fgs.AddMany(flattened_ros)
        self.created = True
        return self.fgs

    def create_box(self):
        return PaddedBox(self.create_grid())
