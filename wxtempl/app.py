import wx
#
from wxtempl.worker import Worker
import logging
#
LOGGER = logging.getLogger(__name__)

class StatusBar(wx.StatusBar):
    def __init__(self):
        wx.StatusBar.__init__(self)

class AsyncFrame(wx.Frame):
    def __init__(self, title,size: wx.Size = None):
        if size is None:
            size = wx.Size(800, 600)
        wx.Frame.__init__(self, None, title=title, size=size)


        self.worker = Worker()
        self.Bind(wx.EVT_CLOSE, self.stop_app)
        self.statusbar = self.CreateStatusBar(1)
        self.bar= StatusBar()



    def stop_app(self, event):
        LOGGER.info("stop signal received")
        self.worker.stop_worker()
        self.Destroy()
#
#
# def async_start(async_frame:AsyncFrame):
#     app = wx.App()
#
#     app.MainLoop()
#     async_frame.worker.wait_to_finish()
#
#
# # def get_app(title: str, start_window, size: wx.Size = None):
# #     if size is None:
# #         size = wx.Size(800, 600)
# #     app = wx.App()
# #
# #     _app = App(title, start_window, size)
# #
# #     app.MainLoop()
# #     LOGGER.info("waiting for worker loop.")
# #     _app.worker.wait_to_finish()
# #     LOGGER.info("stopping app.")
