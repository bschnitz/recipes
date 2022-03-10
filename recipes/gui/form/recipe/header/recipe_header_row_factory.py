import wx
from recipes.gui.form.framework import FormRowFactory

class RecipeHeaderRowFactory(FormRowFactory):
    def row(self, label = None, value = '', choices = None, callback = None):
        flags_col_0 = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL
        flags_col_1 = wx.EXPAND

        if choices != None:
            element = wx.ComboBox(self.parent, choices=choices)
            callback_with_element = lambda event: callback(event, element)
            element.Bind(wx.EVT_COMBOBOX, callback_with_element)
        else:
            element = wx.TextCtrl(self.parent, value=value)

        if label != None:
            col_0 = wx.StaticText(self.parent, label=label)
            col_1 = element
        else:
            col_0 = element
            col_1 = 0

        return [(col_0, 0, flags_col_0), (col_1, 1, flags_col_1)]
