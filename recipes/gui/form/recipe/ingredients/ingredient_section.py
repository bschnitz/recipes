import wx

from recipes.gui.fonts import Head2
from recipes.gui.form.framework import TitleBox
from recipes.gui.form.framework import PaddedBox
from recipes.gui.form.framework import RowWiseForm
from recipes.gui.form.recipe.ingredients import IngredientSectionRowFactory

class IngredientSection:
    def __init__(self, parent):
        self.parent = parent
        self.form = RowWiseForm(parent, IngredientSectionRowFactory)
        self.form.append_ingredient(1.5, 'very long teaspoons', 'water')
        self.form.append_ingredient(10, '', 'eggs')
        self.form.append_ingredient(1, '', '', callback=None)

        title = 'Ingredients for first meal'
        titled_box = TitleBox(self.form.create_grid(), parent, title, Head2())
        parent.SetSizer(PaddedBox(titled_box))
        self.form.fgs.AddGrowableCol(2)

    def on_user_input(self, event, element):
        #element.SetMinSize(wx.Size(self.text_extent(element)))
        extent = element.GetSize()
        border_width = element.GetWindowBorderSize()
        text_extent = self.text_extent(element)
        element.SetMinSize(wx.Size(text_extent[0] + 2*border_width[0], extent[1]))
        #self.form.fgs.Layout()
        self.parent.Layout()
        event.Skip()

    def text_extent(self, text_ctrl):
        font = text_ctrl.GetFont()
        dc = wx.ScreenDC()
        dc.SetFont(font)
        return dc.GetTextExtent(text_ctrl.GetValue())
