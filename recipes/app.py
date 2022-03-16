#!/usr/bin/env python3

import wx
import re

from recipes.gui.form.recipe import RecipeForm
from recipes.gui.form.recipe.ingredients import IngredientSection
from recipes.gui.form.importing.dialog import ImportMealMasterDialog

class MainWindow(wx.Frame):
    def __init__(self, title='', parent=None):
        super().__init__(title=title, parent=parent)
        nb = wx.Notebook(self)
        nb.AddPage(RecipeForm(nb), 'Recipes')
        path = ImportMealMasterDialog(self).run()
        print(path)
        #RecipeForm(self)
        self.Show()

def run():
    app = wx.App()
    MainWindow(title='recipes')
    app.MainLoop()
