#!/usr/bin/env python3

import wx
import re

class MenuWrapper:
    def __init__(self):
        self.menu = wx.Menu()
        self.items = {}
        self.created = False
        self.add_items()

    def append(self, label, helpString='', wId=wx.ID_ANY, kind=wx.ITEM_NORMAL):
        match = re.search('[a-zA-Z]+', label)
        item = self.menu.Append(wId, label, helpString, kind)
        if match[0] != None: self.items['on'+match[0]] = item

    def get_menu(self):
        if not self.created:
            for name in self.items:
                method = getattr(self, name, None)
                if callable(method):
                    self.menu.Bind(wx.EVT_MENU, method, self.items[name])

        return self.menu

class FileMenu(MenuWrapper):
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


class MainMenuBar(wx.MenuBar):
    def __init__(self):
        super().__init__()
        #menu_file = wx.Menu()
        #menu_file.Append(wx.ID_ABOUT, "&About"," Information about this program")
        #menu_file.AppendSeparator()
        #menu_file.Append(wx.ID_EXIT, "E&xit"," Exit the Program")
        self.Append(FileMenu().get_menu(), "&File")

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(200,100))
        self.CreateStatusBar()
        self.SetMenuBar(MainMenuBar())

class Recipes(wx.App):
    def OnInit(self):
        MainWindow(None, 'Recipes').Show(True)
        return True

r = Recipes()
r.MainLoop()
