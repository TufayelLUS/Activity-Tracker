from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer
from time import sleep
import datetime
import wx
import threading


class MyApp(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs,
                                    style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.stopTracker = True
        self.SetSize(wx.Size(600, 400))
        self.SetTitle("Activity Tracker By Tufayel Ahmed")
        self.generatePanel()
        # self.Fit()
        self.Centre()
        self.Layout()

    def generatePanel(self):
        panel = wx.Panel(parent=self, id=wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)
        programLabel = wx.StaticText(
            parent=panel, id=wx.ID_ANY, label="Activity Tracker Software", style=wx.CENTER)
        programLabel.SetFont(wx.Font(15, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))
        programLabel.SetForegroundColour((42, 85, 128))
        programLabel2 = wx.StaticText(
            parent=panel, id=wx.ID_ANY, label="Click START TRACKER to start tracker", style=wx.CENTER)
        programLabel2.SetFont(wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))
        programLabel2.SetForegroundColour((42, 85, 128))
        self.submitBtn = wx.Button(parent=panel, id=wx.ID_ANY,
                                   label="START TRACKER", style=wx.CENTER)
        self.submitBtn.SetFont(wx.Font(13, wx.DECORATIVE, wx.BOLD, wx.NORMAL))
        programLabel3 = wx.StaticText(
            parent=panel, id=wx.ID_ANY, label="*Tracker log is available in activity_log.txt file", style=wx.CENTER)
        programLabel3.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        sizer.Add(programLabel, proportion=0,
                  flag=wx.CENTER | wx.ALL, border=15)
        sizer.Add(programLabel2, proportion=0,
                  flag=wx.CENTER | wx.ALL, border=15)
        sizer.Add(self.submitBtn, proportion=0,
                  flag=wx.CENTER | wx.ALL, border=10)
        sizer.Add(programLabel3, proportion=0,
                  flag=wx.CENTER | wx.ALL, border=10)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.startTracking, self.submitBtn)

    def startTracking(self, event):
        if self.submitBtn.GetLabel() == "START TRACKER":
            self.SetTitle("Tracking -- Activity Tracker By Tufayel Ahmed")
            self.submitBtn.SetLabel("STOP TRACKER")
            self.stopTracker = False
            t = threading.Thread(target=self.trackerActivity, args=())
            t.start()
        else:
            self.submitBtn.SetLabel("START TRACKER")
            self.stopTracker = True

    def trackerActivity(self):
        while True:
            if self.stopTracker:
                self.SetTitle("Activity Tracker By Tufayel Ahmed")
                return
            try:
                current_focus = self.getForegroundWindowTitle()
                if current_focus is None:
                    self.print_log("No window in focus")
                else:
                    self.print_log(current_focus)
            except:
                pass
            finally:
                sleep(1)

    def print_log(self, text):
        with open('activity_log.txt', mode='a+', encoding='utf-8') as logFile:
            logFile.write(
                "{} -- {}\n".format(datetime.datetime.now().strftime("%H:%M:%S %m-%d-%Y"), text))

    def getForegroundWindowTitle(self):
        hWnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(hWnd)
        buf = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hWnd, buf, length + 1)
        if buf.value:
            return buf.value
        else:
            return None


if __name__ == "__main__":
    app = wx.App()
    frame = MyApp(None)
    frame.Show()
    app.MainLoop()


# if __name__ == "__main__":
