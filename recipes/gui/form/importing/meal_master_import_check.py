import wx

class MealMasterImportCheck(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(self.scrolled_text('hello'), 1, wx.EXPAND|wx.ALIGN_TOP)
        vbox.Add(self.scrolled_text('blubber'), 1, wx.EXPAND|wx.ALIGN_TOP)
        self.SetSizer(vbox)

    def scrolled_text(self, value):
        return wx.TextCtrl(self, value=value, style=wx.TE_READONLY|wx.TE_MULTILINE)
