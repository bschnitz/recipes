import wx
from recipes.core.util import Arguments

class ImportMealMasterDialog(wx.FileDialog):
    FILETYPE_MEALMASTER = 'MealMaster file (*.mm;*.mmf)|*.mm;*.mmf;*.MM;*.MMF'
    FILETYPE_ANY        = 'Any File (*)|*'
    def __init__(self, *args, **kwargs):
        a = Arguments(*args, **kwargs)
        a.soft_set(0, 'message', 'Import from MealMaster file')
        a.soft_set(4, 'wildcard', f'{self.FILETYPE_MEALMASTER}|{self.FILETYPE_ANY}')
        a.soft_set(5, 'style', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        super().__init__(*a.args, **a.kwargs)

    def run(self):
        self.ShowModal()
        path = self.GetPath()
        self.Destroy()
        return path
