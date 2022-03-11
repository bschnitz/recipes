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
                self.correct_tab_order(item_index)
            self.fgs.Layout()

    def correct_tab_order(self, index):
        win = self.get_window_at(index)
        if not win: return

        prev = self.get_window_before(index)
        if prev:
            win.MoveAfterInTabOrder(prev)
            return

        next = self.get_window_after(index)
        if next:
            win.MoveBeforeInTabOrder(next)
            return

    def get_window_at(self, index):
        if not self.fgs: return

        item = self.fgs.GetItem(index)

        if not item: return

        return item.GetWindow()

    def get_window_before(self, index):
        for i in reversed(range(0, index)):
            win = self.get_window_at(i)
            if win: return win

    def get_window_after(self, index):
        for i in range(index+1, self.ncols() * len(self.rows)):
            win = self.get_window_at(i)
            if win: return win

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
