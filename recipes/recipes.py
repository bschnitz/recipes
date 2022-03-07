#!/usr/bin/env python3

import wx
import re

class MenuWrapper:
    def __init__(self):
        self.menu = wx.Menu()
        self.items = {}
        self.add_items()
        self.create()

    def append(self, label, helpString='', wId=wx.ID_ANY, kind=wx.ITEM_NORMAL):
        match = re.search('[a-zA-Z&]+', label)
        key = match[0].replace('&', '') if match[0] != None else None
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

    def onAbout(self, event):
        print('onAbout')

    def onExit(self, event):
        print('onExit')


class MainMenuBarWrapper:
    def __init__(self, app, frame):
        bar = wx.MenuBar()
        bar.Append(FileMenuWrapper().menu, "&File")
        frame.SetMenuBar(bar)

class MainWindowWrapper:
    def __init__(self, app, title='', parent=None):
        frame = wx.Frame(parent, title=title)
        frame.CreateStatusBar()
        MainMenuBarWrapper(app, frame)
        frame.Show()

class Recipes(wx.App):
    def OnInit(self):
        MainWindowWrapper(self, title='Recipes')
        return True

r = Recipes()
r.MainLoop()
