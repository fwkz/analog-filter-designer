import wx
from main import Filter
from matplotlib import pyplot
class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(270, 280))
        panel = wx.Panel(self)
        
        #GENERATE BUTTON
        button = wx.Button(panel, wx.ID_ANY, label="Generate", pos=(70, 190), size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.OnClick, button)

        #BANDTYPE
        ftype_txt = wx.StaticText(panel, label="Band type:", pos=(150, 100))
        btype_list = ["Lowpass", "Highpass", "Bandpass", "Bandstop"]
        self.btype_listbox = wx.ListBox(panel, wx.ID_ANY, (150, 115), (80, 60), btype_list, wx.LB_SINGLE)
        self.btype_listbox.SetSelection(0)
        self.get_btype(wx.EVT_LISTBOX)
        self.Bind(wx.EVT_LISTBOX, self.get_btype, self.btype_listbox)

        #FILTER APPROX TYPE
        ftype_txt = wx.StaticText(panel, label="Approximation:", pos=(150, 20))
        ftype_list = ["Butterworth", "Chebyshev I", "Chebyshev II", "Cauer"]
        self.ftype_listbox = wx.ListBox(panel, wx.ID_ANY, (150, 35), (80, 60), ftype_list, wx.LB_SINGLE)
        self.ftype_listbox.SetSelection(0)
        self.get_ftype(wx.EVT_LISTBOX)
        self.Bind(wx.EVT_LISTBOX, self.get_ftype, self.ftype_listbox)

        #FILTER PARAMETERS
        txt = wx.StaticText(panel, label="Filter parameters:", pos=(20, 20))

        fp_txt = wx.StaticText(panel, label="Fp", pos=(20, 40))
        self.fp_ctrl = wx.TextCtrl(panel, wx.ID_ANY, "1", (60, 40), (70, 20))
        self.get_fp(wx.EVT_TEXT)
        self.Bind(wx.EVT_TEXT, self.get_fp, self.fp_ctrl)

        fs_txt = wx.StaticText(panel, label="Fs", pos=(20, 70))
        self.fs_ctrl = wx.TextCtrl(panel, wx.ID_ANY, "1", (60, 70), (70, 20))
        self.get_fs(wx.EVT_TEXT)
        self.Bind(wx.EVT_TEXT, self.get_fs, self.fs_ctrl)

        gpass_txt = wx.StaticText(panel, label="gpass", pos=(20, 100))
        self.gpass_spinner = wx.SpinCtrl(panel, wx.ID_ANY, "", (60, 100), (70, 20))
        self.gpass_spinner.SetRange(1,100)
        self.get_gpass(wx.EVT_SPINCTRL)
        self.Bind(wx.EVT_SPINCTRL, self.get_gpass, self.gpass_spinner)
        
        gstop_txt = wx.StaticText(panel, label="gstop", pos=(20, 130))
        self.gstop_spinner = wx.SpinCtrl(panel, wx.ID_ANY, "", (60, 130), (70, 20))
        self.gstop_spinner.SetRange(1,100)
        self.get_gstop(wx.EVT_SPINCTRL)
        self.Bind(wx.EVT_SPINCTRL, self.get_gstop, self.gstop_spinner)

        self.Show(True)

    def get_fp(self, event):
        self.fp = self.fp_ctrl.GetValue()
        try:
            self.fp = int(self.fp)
        except ValueError:
            try:
                self.fp = self.fp.split(" ")
                self.fp = [int(freq) for freq in self.fp]
            except ValueError:
                pass
            print self.fp

    def get_fs(self, event):
        self.fs = self.fs_ctrl.GetValue()
        try:
            self.fs = int(self.fs)
        except ValueError:
            try:
                self.fs = self.fs.split(" ")
                self.fs = [int(freq) for freq in self.fs]
            except ValueError:
                pass
            print self.fs

    def get_gpass(self, event):
        self.gpass = self.gpass_spinner.GetValue()

    def get_gstop(self, event):
        self.gstop = self.gstop_spinner.GetValue()

    def get_ftype(self, event):
        self.ftype = self.ftype_listbox.GetStringSelection()
        types_dict = {"Butterworth":"butter", "Chebyshev I":"cheby1", "Chebyshev II":"cheby2", "Cauer": "ellip"}
        self.ftype = types_dict[self.ftype]
        print self.ftype
    
    def get_btype(self, event):
        self.btype = self.btype_listbox.GetStringSelection().lower()
        print self.btype

    def OnClick(self, event):
        filter_ = Filter(self.fp, self.fs, self.gpass, self.gstop, ftype=self.ftype, btype=self.btype)
        filter_.phase_response()
        filter_.poles_zeros()
        filter_.freq_response()
        filter_.step_response()
        pyplot.show()


app = wx.App(False)
frame = MyFrame(None, 'Analog Filter Designer')
app.MainLoop()