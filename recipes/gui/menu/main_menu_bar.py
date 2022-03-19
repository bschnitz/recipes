import wx
from recipes.gui.form.framework.events import EventIds as id

class MainMenuBar(wx.MenuBar):
    def __init__(self, parent):
        super().__init__()
        self.add_import_menu()
        parent.SetMenuBar(self)

    def add_import_menu(self):
        menu = wx.Menu()
        menu.Append(id.IMPORT_MEAL_MASTER, item="Import &MealMaster file")
        self.Append(menu, '&Import')
