import asyncio

from wxtempl.worker import Worker
import wx
import logging

LOGGER = logging.getLogger(__name__)


class Helpers:
    def __init__(self, shortcuts=None):
        self.worker = Worker()
        if shortcuts:
            self.short_cuts = shortcuts
        else:
            self.short_cuts = []

    def add_short_cut(self, capture, key: str, callback, id=None):

        if id is None:
            id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, callback, id)
        self.short_cuts.append((capture, ord(key), id))

    def add_static_text(self, text, weight=0):
        txt = wx.StaticText(self, 1, text)
        
        self._add_to_sizer(txt, weight)
        # sizer.Add(txt, weight, flag=wx.EXPAND)
        return txt

    def _add_to_sizer(self, window, weight, sizer=None):
        if self.sizer:
            self.sizer.Add(window, weight, flag=wx.EXPAND)

    def add_text_ctrl(self, weight=0):
        txt_ctrl = wx.TextCtrl(self)
        self._add_to_sizer(txt_ctrl, weight)
        return txt_ctrl

    def add_ctrl(self, ctrl):
        ctrl.Create(self, -1)

        self._add_to_sizer(ctrl, 0)
        return ctrl

    def make_button(
        self,
        label,
        callback,
        weight=0,
        shortcut: tuple = None,
        modify_label=True,
    ):
        if shortcut:
            self.add_short_cut(shortcut[0], shortcut[1], callback)
            if modify_label:
                if shortcut[0] == wx.ACCEL_NORMAL:
                    label = "{} <{}>".format(label, shortcut[1])
                elif shortcut[0] == wx.ACCEL_CTRL:
                    label = "{} <CTR-{}>".format(label, shortcut[1])

        button = wx.Button(self, 1, label=label)
        button.Bind(wx.EVT_BUTTON, callback)

        self._add_to_sizer(button, weight)

        return button

    def make_checkbox(
        self, label, callback=None, sizer=None, weight=0
    ):
        checkbox = wx.CheckBox(self, weight, label=label)

        self._add_to_sizer(checkbox, weight, sizer)

        return checkbox


async def process_manager(process, logger, finished_callback):
    try:
        while not process.stdout.at_eof():
            line = await process.stdout.readline()
            logger(line.decode("ascii"))
        code = await process.wait()
        # logger("finished with {}".format(code))
        finished_callback(code)
    except Exception as err:
        logger(err)
