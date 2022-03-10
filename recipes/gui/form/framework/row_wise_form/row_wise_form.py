import wx
import functools
from recipes.gui.form.framework import PaddedBox

class RowWiseForm:
    def __init__(self, parent, row_factory_class):
        self.parent = parent
        self.rows = []
        self.factory = row_factory_class(parent)
        self.fgs = None

    def ncols(self):
        return len(self.rows[0]) if len(self.rows) > 0 else 0

    def insert_row(self, index, *args, **kwargs):
        if index < 0: index = index + len(self.rows)
        row = self.factory.row(*args, **kwargs)
        self.rows.insert(index, row)
        if self.fgs:
            item_index = index * self.ncols()
            for item in reversed(row):
                self.fgs.Insert(item_index, *item)
            self.fgs.Layout()

    def append_row(self, *args, irow = None, **kwargs):
        row = self.factory.row(*args, **kwargs)
        self.rows.append(row)
        if self.fgs:
            self.fgs.AddMany(row)
            self.fgs.Layout()

    def create_grid(self):
        self.fgs = wx.FlexGridSizer(cols = self.ncols(), vgap = 10, hgap = 10)
        flatten_rows = lambda flattened, row: [*flattened, *row]
        flattened_ros = functools.reduce(flatten_rows, self.rows, [])
        self.fgs.AddMany(flattened_ros)
        self.fgs.AddGrowableCol(1, 1)
        self.created = True
        return self.fgs

    def create_box(self):
        return PaddedBox(self.create_grid())
