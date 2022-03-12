import wx

from recipes.gui.form.framework import RowWiseForm
from recipes.gui.form.framework import AutoResizeTextCtrl
from recipes.gui.form.recipe.ingredients import IngredientSectionRowFactory

class IngredientSection:
    def __init__(self, parent):
        self.parent = parent
        self.form = RowWiseForm(parent, IngredientSectionRowFactory)
        self.form.append_ingredient(1.5, 'very long teaspoons', 'water')
        self.form.append_ingredient(10, '', 'eggs')
        self.form.append_ingredient(1, '', '', callback=None)
        parent.SetSizer(self.form.create_box())
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
