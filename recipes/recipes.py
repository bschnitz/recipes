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

class SimpleForm:
    def __init__(self, parent):
        self.parent = parent
        self.rows = []

    def add_element(self, element, label = '', column = 1):
        flags_col_0 = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL
        flags_col_1 = wx.EXPAND

        if column == 1:
            col_0 = wx.StaticText(self.parent, label=label)
            col_1 = element
        else:
            col_0 = element
            col_1 = 0

        self.rows.append([(col_0, 0, flags_col_0), (col_1, 1, flags_col_1)])

    def add_input(self, label = '', column = 1):
        self.add_element(wx.TextCtrl(self.parent), label=label, column=column)


    def create_grid(self):
        fgs = wx.FlexGridSizer(
            rows = len(self.rows),
            cols = 2,
            vgap = 10,
            hgap = 10
        )
        flatten_rows = lambda flattened, row: [*flattened, *row]
        flattened_ros = functools.reduce(flatten_rows, self.rows, [])
        fgs.AddMany(flattened_ros)
        fgs.AddGrowableCol(1, 1)
        return fgs

    def create_box(self):
        return PaddedBox(self.create_grid())

class RecipeHeaderForm:
    def __init__(self, parent, title, meta = {}):
        form = SimpleForm(parent)
        form.add_input(label = 'Title')

        # label and input for all other meta fields
        for key in meta:
            form.add_input(meta[key]['label'])

        parent.SetSizer(form.create_box())



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


        #panel.SetSizer(PaddedBox(fgs))

#class MainWindowWrapper:
#    def __init__(self, app, title='', parent=None):
#        frame = wx.Frame(parent, title=title, size = (300, 250))
#        #frame.CreateStatusBar()
#        #MainMenuBarWrapper(app, frame)
#        RecipeForm(frame)
#        frame.Show()

class MainWindow(wx.Frame):
    def __init__(self, title='', parent=None):
        super().__init__(title=title, parent=parent)
        RecipeForm(self)
        #panel = wx.Panel(self)

        #hbox = wx.BoxSizer(wx.HORIZONTAL)

        #fgs = wx.FlexGridSizer(3, 2, 10,10)

        #title = wx.StaticText(panel, label = "Title")
        #author = wx.StaticText(panel, label = "Name of the Author")
        #review = wx.StaticText(panel, label = "Review")

        #tc1 = wx.TextCtrl(panel)
        #tc2 = wx.TextCtrl(panel)
        #tc3 = wx.TextCtrl(panel, style = wx.TE_MULTILINE)

        #fgs.AddMany([(title), (tc1, 1, wx.EXPAND), (author),
        #             (tc2, 1, wx.EXPAND), (review, 1, wx.EXPAND), (tc3, 1, wx.EXPAND)])
        #fgs.AddGrowableRow(2, 1)
        #fgs.AddGrowableCol(1, 1)
        #hbox.Add(fgs, proportion = 2, flag = wx.ALL|wx.EXPAND, border = 15)
        #panel.SetSizer(hbox)

        self.Show()

app = wx.App()
MainWindow(title='recipes')
#MainWindow(title='recipes')
app.MainLoop()

#class Recipes(wx.App):
#    def OnInit(self):
#        MainWindowWrapper(self, title='Recipes')
#        return True

#r = Recipes()
#r.MainLoop()
