import wx
from main import Filter
from matplotlib import pyplot
class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(250, 250))
        panel = wx.Panel(self)
        
        txt = wx.StaticText(panel, label="Lecisz z koksem?", pos=(30, 20))
        button = wx.Button(panel, wx.ID_ANY, label="heja", pos=(30, 40))
        self.Bind(wx.EVT_BUTTON, self.OnClick, button)

        ftype_txt = wx.StaticText(panel, label="Approximation:", pos=(130, 20))
        ftype_list = ["Butterworth", "Chebyshev"]
        self.ftype_listbox = wx.ListBox(panel, wx.ID_ANY, (130, 35), (80, 60), ftype_list, wx.LB_SINGLE)
        self.ftype_listbox.SetSelection(0)
        self.ftype = self.ftype_listbox.GetStringSelection()
        self.Bind(wx.EVT_LISTBOX, self.get_ftype, self.ftype_listbox)

        fp_txt = wx.StaticText(panel, label="Fp", pos=(20, 80))
        self.fp_spinner = wx.SpinCtrl(panel, wx.ID_ANY, "", (60, 80), (60, 20))
        self.Bind(wx.EVT_SPINCTRL, self.get_fp, self.fp_spinner)

        fs_txt = wx.StaticText(panel, label="Fs", pos=(20, 110))
        self.fs_spinner = wx.SpinCtrl(panel, wx.ID_ANY, "", (60, 110), (60, 20))
        self.Bind(wx.EVT_SPINCTRL, self.get_fs, self.fs_spinner)

        gpass_txt = wx.StaticText(panel, label="gpass", pos=(20, 140))
        self.gpass_spinner = wx.SpinCtrl(panel, wx.ID_ANY, "", (60, 140), (60, 20))
        self.Bind(wx.EVT_SPINCTRL, self.get_gpass, self.gpass_spinner)
        
        gstop_txt = wx.StaticText(panel, label="gstop", pos=(20, 170))
        self.gstop_spinner = wx.SpinCtrl(panel, wx.ID_ANY, "", (60, 170), (60, 20))
        self.Bind(wx.EVT_SPINCTRL, self.get_gstop, self.gstop_spinner)

        self.Show(True)

    def get_fp(self, event):
        self.fp = self.fp_spinner.GetValue()

    def get_fs(self, event):
        self.fs = self.fs_spinner.GetValue()

    def get_gpass(self, event):
        self.gpass = self.gpass_spinner.GetValue()
        print self.gpass

    def get_gstop(self, event):
        self.gstop = self.gstop_spinner.GetValue()
        print self.gstop

    def get_ftype(self, event):
        self.ftype = self.ftype_listbox.GetStringSelection()

    def OnClick(self, event):
        #filter1 = Filter(10000, 17000, 1.0, 25.0, ftype="butterworth").phase_response()
        filter2 = Filter(self.fp, self.fs, self.gpass, 40.0, ftype="butterworth")
        filter2.phase_response()
        filter2.poles_zeros()
        filter2.freq_response()
        filter2.step_response()
        print ">" + str(self.ftype) + "<"
        pyplot.show()


app = wx.App(False)
frame = MyFrame(None, 'Analog Filter Designer')
app.MainLoop()