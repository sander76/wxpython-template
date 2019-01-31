from test_app.async_process import (
    start_process,
    start_process_and_return,
    process_manager,
)
from wxtempl.app import AsyncFrame, async_start
import wx

from wxtempl.helpers import Helpers
from wxtempl.splitter_window import TwoSplitterWindow
from wxtempl.tabbed_window import TabUi
from wxtempl.worker import Worker


class TabServer(TwoSplitterWindow):
    def __init__(self, parent):
        TwoSplitterWindow.__init__(self, parent)

        self.splitter_window_one.make_button(
            "another button",self.another_button,shortcut=(wx.ACCEL_NORMAL,"w"))

        # )
        #
        # self.make_button(
        #     self.splitter_window_one,
        #     "another button",
        #     self.another_button,
        #     self.window_one_sizer,
        #     shortcut=(wx.ACCEL_NORMAL, "w"),
        # )

    def another_button(self, event):
        pass


class TabDevelop(TwoSplitterWindow):
    def __init__(self, parent):
        self.short_cuts = []
        TwoSplitterWindow.__init__(self, parent,shortcuts=self.short_cuts)
        self.worker=Worker()

        # self.doc_folder = wx.TextCtrl(self.splitter_window_one)

        self.splitter_window_one.make_button(
            "select folder",self.choose_doc_folder,shortcut=(wx.ACCEL_NORMAL,"q")
        )

        self.splitter_window_one.make_checkbox("develop dirty")

        self.splitter_window_one.make_checkbox("make_pdf")

        self.splitter_window_one.make_button(
            "develop",self.on_develop
        )


        self.splitter_window_one.make_button(
            "start process",self.manage_process
        )

        self.splitter_window_one.make_button(
            "stop process",self.terminate_process
        )


        self.doc_folder = self.splitter_window_one.add_ctrl(wx.TextCtrl())


        self._logger = wx.TextCtrl(
            self.splitter_window_two, style=wx.TE_MULTILINE
        )
        #self.window_two_sizer.Add(self._logger, 1, flag=wx.EXPAND)

        self.serve_task = None

        self.SetAcceleratorTable(wx.AcceleratorTable(self.short_cuts))

    def log(self, message: str):
        self._logger.AppendText(message)

    def on_develop(self, event):
        self.log("starting process")
        self.worker.do_work(start_process(self.log))

    def manage_process(self, event):
        self.log("starting process")
        fut = self.worker.do_work(start_process_and_return())
        self.process = fut.result()
        self.worker.do_work(process_manager(self.process, self.log))

    def terminate_process(self, event):
        self.log("terminate process")
        self.process.terminate()

    def choose_doc_folder(self, event):
        dlg = wx.DirDialog(self, message="choose docs folder")
        if dlg.ShowModal() == wx.ID_OK:
            self.doc_folder.write(dlg.GetPath())
        dlg.Destroy()


class Tabbed(TabUi):
    def __init__(self, parent):
        TabUi.__init__(self, parent)
        self.AddPage(TabDevelop(self), "develop")
        self.AddPage(TabServer(self), "server")

app = wx.App()


async_app = AsyncFrame("a test app",Tabbed)
# async_start(async_app)

app.MainLoop()
async_app.worker.wait_to_finish()

#app = get_app("a test app", Tabbed)
