#!/usr/bin/env python3

import os
import re
import wx
import wx.aui
from recipes.core.parsers import MealMaster
from recipes.core.util.event import ev

from recipes.gui.menu import MainMenuBar
from recipes.gui.form.recipe import RecipeForm
from recipes.gui.form.recipe.ingredients import IngredientSection
from recipes.gui.form.importing.dialog import ImportMealMasterDialog
from recipes.gui.form.importing import MealMasterImportCheck

class MainWindow(wx.Frame):
    def __init__(self, title='', parent=None):
        super().__init__(title=title, parent=parent)
        MainMenuBar(self)
        self.nb = wx.aui.AuiNotebook(self)
        self.nb.AddPage(RecipeForm(self.nb), 'Recipes')
        self.Bind(wx.EVT_MENU, self.on_menu_item_select)
        self.Show()

    def on_menu_item_select(self, event):
        menu_callback_map = {
            ev.IMPORT_MEAL_MASTER: self.on_import_meal_master
        }
        menu_callback_map[event.GetId()](event)

    def on_import_meal_master(self, event):
        dialog = ImportMealMasterDialog(self)
        dialog.ShowModal()
        file = dialog.get_path()
        encoding = dialog.get_encoding()
        if file: self.import_meal_master_file(file, encoding)

    def import_meal_master_file(self, file, encoding):
        m = MealMaster()
        m.parse_file(file, encoding=encoding)
        mmic = MealMasterImportCheck(self.nb, m.original_recipes, m.recipes)
        filename = os.path.basename(file)
        self.nb.AddPage(mmic, f'Import: {filename}')

def run():
    app = wx.App()
    MainWindow(title='recipes')
    app.MainLoop()
