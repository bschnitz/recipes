#!/usr/bin/env python3

import wx
import re
import functools

class MenuWrapper:
    def __init__(self):
        self.menu = wx.Menu()
        self.items = {}
        self.add_items()
        self.create()

    def append(self, label, helpString='', wId=wx.ID_ANY, kind=wx.ITEM_NORMAL):
        match = re.search('[a-zA-Z& ]+', label)
        key = re.sub('[& ]', '', match[0]) if match[0] != None else None
        item = self.menu.Append(wId, label, helpString, kind)
        if key: self.items['on'+key] = item

    def create(self):
        for name in self.items:
            method = getattr(self, name, None)
            if callable(method):
                self.menu.Bind(wx.EVT_MENU, method, self.items[name])

class FileMenuWrapper(MenuWrapper):
    def add_items(self):
        self.append(wId=wx.ID_ABOUT,
                    label="&About",
                    helpString=" Information about this program")
        self.menu.AppendSeparator()
        self.append(wId=wx.ID_EXIT,
                    label="E&xit",
                    helpString=" Exit the Program")
        self.append(label="&Import Recipes",
                    helpString=" Load new recipes into the database")

    def onAbout(self, event):
        print('onAbout')

    def onExit(self, event):
        print('onExit')

    def onImportRecipes(self, event):
        print('onImportRecipes')


class MainMenuBarWrapper:
    def __init__(self, app, frame):
        bar = wx.MenuBar()
        bar.Append(FileMenuWrapper().menu, "&File")
        frame.SetMenuBar(bar)

class PaddedBox(wx.BoxSizer):
    def __init__(self,
                 child,
                 orient=wx.HORIZONTAL,
                 proportion=2,
                 flag=wx.ALL|wx.EXPAND,
                 border=15):
        super().__init__(orient)
        self.Add(child, proportion=proportion, flag=flag, border=border)

class RowWiseFormRowFactory:
    def __init__(self, parent):
        self.parent = parent

class RecipeHeaderRowFactory(RowWiseFormRowFactory):
    def row(self, label = None, value = '', choices = None, callback = None):
        flags_col_0 = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL
        flags_col_1 = wx.EXPAND

        if choices != None:
            element = wx.ComboBox(self.parent, choices=choices)
            callback_with_element = lambda event: callback(event, element)
            element.Bind(wx.EVT_COMBOBOX, callback_with_element)
        else:
            element = wx.TextCtrl(self.parent, value=value)

        if label != None:
            col_0 = wx.StaticText(self.parent, label=label)
            col_1 = element
        else:
            col_0 = element
            col_1 = 0

        return [(col_0, 0, flags_col_0), (col_1, 1, flags_col_1)]

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

class RecipeHeaderForm:
    def __init__(self, parent, title, meta = {}):
        self.form = RowWiseForm(parent, RecipeHeaderRowFactory)
        self.form.append_row(label = 'Title', value = title)

        # label and input for all other meta fields
        for key in meta:
            self.form.append_row(meta[key]['label'], meta[key].get('value', ''))

        choices = ['blue', 'yellow', 'green', 'very long option']
        self.form.append_row(choices = choices, callback = self.onAddMeta)

        parent.SetSizer(self.form.create_box())

    def onAddMeta(self, event, combobox):
        self.form.insert_row(-1, label = combobox.GetValue())


class RecipeForm:
    def __init__(self, parent):
        meta_fields = {
            'tags': {'label': 'Tags'},
            'portions': {'label': 'Portions'},
            'author': {'label': 'Author'},
        }
        RecipeHeaderForm(wx.Panel(parent), 'Hello Worlds!', meta_fields)

    def old(self):
        panel = wx.Panel(parent)
        fgs = wx.FlexGridSizer(3, 2, 10,10)

        title = wx.StaticText(panel, label = "Title")
        author = wx.StaticText(panel, label = "Name of the Author")
        review = wx.StaticText(panel, label = "Review")

        tc1 = wx.TextCtrl(panel)
        tc2 = wx.TextCtrl(panel)
        tc3 = wx.TextCtrl(panel, style = wx.TE_MULTILINE)

        fgs.AddMany([(title), (tc1, 1, wx.EXPAND),
                     (author), (tc2, 1, wx.EXPAND),
                     (review, 1, wx.EXPAND), (tc3, 1, wx.EXPAND)])
        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)

class MainWindow(wx.Frame):
    def __init__(self, title='', parent=None):
        super().__init__(title=title, parent=parent)
        RecipeForm(self)
        self.Show()

app = wx.App()
MainWindow(title='recipes')
app.MainLoop()
