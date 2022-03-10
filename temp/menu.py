class MenuWrapper:
    def __init__(self):
        self.menu = wx.Menu()
        self.items = {}
        self.add_items()
        self.create()

    def append(self, label, helpString='', wId=wx.ID_ANY, kind=wx.ITEM_NORMAL):
        match = re.search('[a-zA-Z& ]+', label)
        key = re.sub('[& ]', '', match[0]) if match[0] != None else None
        item = self.menu.Append(wId, label, helpString, kind)
        if key: self.items['on'+key] = item

    def create(self):
        for name in self.items:
            method = getattr(self, name, None)
            if callable(method):
                self.menu.Bind(wx.EVT_MENU, method, self.items[name])

class FileMenuWrapper(MenuWrapper):
    def add_items(self):
        self.append(wId=wx.ID_ABOUT,
                    label="&About",
                    helpString=" Information about this program")
        self.menu.AppendSeparator()
        self.append(wId=wx.ID_EXIT,
                    label="E&xit",
                    helpString=" Exit the Program")
        self.append(label="&Import Recipes",
                    helpString=" Load new recipes into the database")

    def onAbout(self, event):
        print('onAbout')

    def onExit(self, event):
        print('onExit')

    def onImportRecipes(self, event):
        print('onImportRecipes')

class MainMenuBarWrapper:
    def __init__(self, app, frame):
        bar = wx.MenuBar()
        bar.Append(FileMenuWrapper().menu, "&File")
        frame.SetMenuBar(bar)
