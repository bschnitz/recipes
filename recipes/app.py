#!/usr/bin/env python3

import wx
import re

from recipes.gui.form.recipe import RecipeForm
from recipes.gui.form.recipe.ingredients import IngredientSection

class MainWindow(wx.Frame):
    def __init__(self, title='', parent=None):
        super().__init__(title=title, parent=parent)
        RecipeForm(self)
        self.Show()

def run():
    app = wx.App()
    MainWindow(title='recipes')
    app.MainLoop()
