import wx
import math

class TitleBox(wx.BoxSizer):
    def __init__(self, child, parent, title, font, flag=wx.EXPAND):
        super().__init__(wx.VERTICAL)

        font_height = font.GetPixelSize()[1]

        title = wx.StaticText(parent, label=title)
        title.SetFont(font)

        self.Add(title, flag=flag|wx.BOTTOM, border=math.floor(font_height*0.3))
        self.Add(child, flag=flag)
