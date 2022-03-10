import wx

class PaddedBox(wx.BoxSizer):
    def __init__(self,
                 child,
                 orient=wx.HORIZONTAL,
                 proportion=2,
                 flag=wx.ALL|wx.EXPAND,
                 border=15):
        super().__init__(orient)
        self.Add(child, proportion=proportion, flag=flag, border=border)
