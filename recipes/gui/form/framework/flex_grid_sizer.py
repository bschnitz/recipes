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

    def set_tabindex(self, window, index):
        prev_window = self.get_window_before(index)
        if prev_window:
            window.MoveAfterInTabOrder(prev_window)
            return

        next_window = self.get_window_after(index)
        if next:
            window.MoveBeforeInTabOrder(next_window)
            return

    def normalize_tab_order_for_window_at_index(self, index):
        window = self.get_window_at(index)

        if not window: return

        self.set_tabindex(window, index)
