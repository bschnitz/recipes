import wx
import math

class Head2(wx.Font):
    def __init__(self):
        super().__init__(wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT))
        point_size = self.GetPointSize()
        self.SetPointSize(math.floor(point_size * 2))
