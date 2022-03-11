import wx

class FlexGridSizer(wx.FlexGridSizer):
    def get_window_at(self, index):
        item = self.GetItem(index)

        if not item: return

        return item.GetWindow()

    def get_window_before(self, index):
        for i in reversed(range(0, index)):
            win = self.get_window_at(i)
            if win: return win

    def get_window_after(self, index):
        for i in range(index+1, self.ncols() * len(self.rows)):
            win = self.get_window_at(i)
            if win: return win
