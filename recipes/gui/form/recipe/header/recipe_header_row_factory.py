import wx
from recipes.gui.form.framework import FormRowFactory

class RecipeHeaderRowFactory(FormRowFactory):
    COLUMN_FLAGS = [
        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL,
        wx.EXPAND
    ]

    def attribute(self, label, value = ''):
        label = wx.StaticText(self.parent, label=label)
        input = wx.TextCtrl(self.parent, value=value)
        return [
            (label, 0, self.COLUMN_FLAGS[0]),
            (input, 1, self.COLUMN_FLAGS[1])
        ]

    def combo(self, choices, callback):
        combo = wx.ComboBox(self.parent, choices=choices)
        callback_with_element = lambda event: callback(event, combo)
        combo.Bind(wx.EVT_COMBOBOX, callback_with_element)
        return [
            (combo, 0, self.COLUMN_FLAGS[0]),
            (0, 1, self.COLUMN_FLAGS[1])
        ]
