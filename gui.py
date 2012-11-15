import wx
from main import Filter
from matplotlib import pyplot
class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,200))
        panel = wx.Panel(self)
        txt = wx.StaticText(panel, label="Lecisz z koksem?", pos=(20, 50))
        button = wx.Button(panel, wx.ID_ANY, label="heja", pos=(20, 70))
        self.Bind(wx.EVT_BUTTON, self.OnClick, button)
        self.Show(True)

    def OnClick(self, event):
        #filter1 = Filter(10000, 17000, 1.0, 25.0, ftype="butterworth").phase_response()
        filter2 = Filter(155, 50, 1.0, 40.0, ftype="butterworth")
        filter2.phase_response()
        filter2.poles_zeros()
        filter2.freq_response()
        filter2.step_response()
        pyplot.show()


app = wx.App(False)
frame = MyFrame(None, 'Analog Filter Designer')
app.MainLoop()