import wx
from wxtempl.helpers import Helpers


class Container(wx.StaticBox, Helpers):
    def __init__(self, parent, label, shortcuts=None):
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        wx.StaticBox.__init__(self, parent, id=wx.ID_ANY, label=label)
        Helpers.__init__(self, shortcuts=shortcuts)
        self.top_border, self.other_border = self.GetBordersForSizer()

        self.sizer.AddSpacer(self.top_border)
        self.SetSizer(self.sizer)

    def _add_to_sizer(self, window, weight, sizer=None):
        self.sizer.Add(
            window,
            weight,
            wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT,
            self.other_border + 10,
        )

    def add_window(self, component):
        self.box_sizer.Add(component, 1, flag=wx.EXPAND)


class SplitterWindowPartial(wx.Window, Helpers):
    def __init__(self,parent, shortcuts=None):
        wx.Window.__init__(self,parent)
        Helpers.__init__(self, shortcuts=shortcuts)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)


class TwoSplitterWindow(wx.SplitterWindow):
    def __init__(
        self, parent, include_sizers=True, window_one_size=150, shortcuts=None
    ):
        
        wx.SplitterWindow.__init__(self, parent)

        self.splitter_window_one = SplitterWindowPartial(self,shortcuts=shortcuts)

        self.splitter_window_two = SplitterWindowPartial(self,shortcuts=shortcuts)

        # self.window_one_sizer = None
        # self.window_two_sizer = None

        # if include_sizers:
        #     self.window_one_sizer = wx.BoxSizer(wx.VERTICAL)
        #     self.window_two_sizer = wx.BoxSizer(wx.VERTICAL)
        #
        #     self.splitter_window_one.SetSizer(self.window_one_sizer)
        #     self.splitter_window_two.SetSizer(self.window_two_sizer)

        self.SetMinimumPaneSize(20)
        self.SplitVertically(
            self.splitter_window_one, self.splitter_window_two, window_one_size
        )
