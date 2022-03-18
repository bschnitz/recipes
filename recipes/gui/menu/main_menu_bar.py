import wx
from recipes.core.util.event import ev

class MainMenuBar(wx.MenuBar):
    def __init__(self, parent):
        super().__init__()
        self.add_import_menu()
        parent.SetMenuBar(self)

    def add_import_menu(self):
        menu = wx.Menu()
        menu.Append(ev.IMPORT_MEAL_MASTER, item="Import &MealMaster file")
        self.Append(menu, '&Import')
