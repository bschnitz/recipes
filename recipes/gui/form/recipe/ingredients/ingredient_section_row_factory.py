import wx
from recipes.gui.form.framework import FormRowFactory
from recipes.gui.form.framework import AutoResizeTextCtrl

class IngredientSectionRowFactory(FormRowFactory):
    def ingredient(self, amount = 1, unit = '', name = '', callback = None):
        input_amount = wx.TextCtrl(self.parent, value=str(amount))
        input_unit = AutoResizeTextCtrl(self.parent, value=unit)
        input_name = wx.TextCtrl(self.parent, value=name)

        if callback:
            callback_with_element = lambda event: callback(event, input_unit)
            input_unit.Bind(wx.EVT_KEY_UP, callback_with_element)

        return [(input_amount), (input_unit), (input_name, 1, wx.EXPAND)]
