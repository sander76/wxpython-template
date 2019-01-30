import wx


class TabUi(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, style=wx.BK_DEFAULT)

    def add(self, window, title):
        self.AddPage(window, title)
