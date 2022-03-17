#!/usr/bin/env python3

import re
import wx
import wx.aui

from recipes.gui.form.recipe import RecipeForm
from recipes.gui.form.recipe.ingredients import IngredientSection
from recipes.gui.form.importing.dialog import ImportMealMasterDialog
from recipes.gui.form.importing import MealMasterImportCheck

class MainWindow(wx.Frame):
    def __init__(self, title='', parent=None):
        super().__init__(title=title, parent=parent)
        nb = wx.aui.AuiNotebook(self)
        nb.AddPage(RecipeForm(nb), 'Recipes')
        nb.AddPage(MealMasterImportCheck(nb), 'Import')
        #path = ImportMealMasterDialog(self).run()
        self.Show()

def run():
    app = wx.App()
    MainWindow(title='recipes')
    app.MainLoop()
