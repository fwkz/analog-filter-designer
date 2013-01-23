import wx
import wx.lib.scrolledpanel as scrolled
from main import Filter
from matplotlib import pyplot
from lc_ladder import LCladder
from scheme import Scheme
import Tkinter

class MyFrame(wx.Frame):
    """ New class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(270, 340))
        panel = wx.Panel(self)
        
        #GENERATE BUTTON
        button = wx.Button(panel, wx.ID_ANY, label="Generate", pos=(70, 240), size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.OnClick, button)

        #BANDTYPE
        ftype_txt = wx.StaticText(panel, label="Band type:", pos=(150, 120))
        btype_list = ["Lowpass", "Highpass", "Bandpass", "Bandstop"]
        self.btype_listbox = wx.ListBox(panel, wx.ID_ANY, (150, 135), (80, 60), btype_list, wx.LB_SINGLE)
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

        """" FILTER PARAMETERS """
        txt = wx.StaticText(panel, label="Filter parameters:", pos=(20, 20))
        
        #Passband corner frequency textbox
        fp_txt = wx.StaticText(panel, label="Fp", pos=(20, 40))
        self.fp_ctrl = wx.TextCtrl(panel, wx.ID_ANY, "1", (60, 40), (70, 20))
        self.get_fp(wx.EVT_TEXT)
        self.Bind(wx.EVT_TEXT, self.get_fp, self.fp_ctrl)

        #Stopband corner frequency textbox
        fs_txt = wx.StaticText(panel, label="Fs", pos=(20, 70))
        self.fs_ctrl = wx.TextCtrl(panel, wx.ID_ANY, "1", (60, 70), (70, 20))
        self.get_fs(wx.EVT_TEXT)
        self.Bind(wx.EVT_TEXT, self.get_fs, self.fs_ctrl)

        #Passband ripple spinner
        gpass_txt = wx.StaticText(panel, label="gpass", pos=(20, 100))
        self.gpass_spinner = wx.SpinCtrl(panel, wx.ID_ANY, "", (60, 100), (70, 20))
        self.gpass_spinner.SetRange(1,100)
        self.get_gpass(wx.EVT_SPINCTRL)
        self.Bind(wx.EVT_SPINCTRL, self.get_gpass, self.gpass_spinner)
        
        #Stopband attenuation spinner
        gstop_txt = wx.StaticText(panel, label="gstop", pos=(20, 130))
        self.gstop_spinner = wx.SpinCtrl(panel, wx.ID_ANY, "", (60, 130), (70, 20))
        self.gstop_spinner.SetRange(1,1000)
        self.get_gstop(wx.EVT_SPINCTRL)
        self.Bind(wx.EVT_SPINCTRL, self.get_gstop, self.gstop_spinner)

        #R1 - input load spinner
        R1_txt = wx.StaticText(panel, label= 'R1', pos=(20, 160))
        self.R1_spinner = wx.SpinCtrl(panel, wx.ID_ANY, "", (60, 160), (70, 20))
        self.R1_spinner.SetRange(1, 100000000)
        self.get_R1(wx.EVT_SPINCTRL)
        self.Bind(wx.EVT_SPINCTRL, self.get_R1, self.R1_spinner)
        
        #R2 - output load spinner
        R2_txt = wx.StaticText(panel, label= 'R2', pos=(20, 190))
        self.R2_spinner = wx.SpinCtrl(panel, wx.ID_ANY, "", (60, 190), (70, 20))
        self.R2_spinner.SetRange(1, 100000000)
        self.get_R2(wx.EVT_SPINCTRL)
        self.Bind(wx.EVT_SPINCTRL, self.get_R2, self.R2_spinner)

        self.Show(True)


    def get_fp(self, event):
        """ Get and parse passband corner frequency """
        self.fp = self.fp_ctrl.GetValue()
        try:
            self.fp = int(self.fp)
        except ValueError:
            try:
                self.fp = self.fp.split(" ")
                self.fp = [int(freq) for freq in self.fp]
            except ValueError:
                pass
            #print self.fp


    def get_fs(self, event):
        """ Get and parse stopband corner frequency """
        self.fs = self.fs_ctrl.GetValue()
        try:
            self.fs = int(self.fs)
        except ValueError:
            try:
                self.fs = self.fs.split(" ")
                self.fs = [int(freq) for freq in self.fs]
            except ValueError:
                pass
            #print self.fs


    def get_gpass(self, event):
        """ Get maximum passband ripple """
        self.gpass = self.gpass_spinner.GetValue()


    def get_R1(self, event):
        """ Get input Load """
        self.R1 = float(self.R1_spinner.GetValue())
        #print float(self.R1)


    def get_R2(self, event):
        """ Get output load """
        self.R2 = float(self.R2_spinner.GetValue())
        #print float(self.R2)


    def get_gstop(self, event):
        """ Get minimum stopband attenuation """
        self.gstop = self.gstop_spinner.GetValue()


    def get_ftype(self, event):
        """ Get filter approximation """
        self.ftype = self.ftype_listbox.GetStringSelection()
        types_dict = {"Butterworth":"butter", "Chebyshev I":"cheby1", "Chebyshev II":"cheby2", "Cauer": "ellip"}
        self.ftype = types_dict[self.ftype]
        #print self.ftype
    

    def get_btype(self, event):
        """ Get band type """
        self.btype = self.btype_listbox.GetStringSelection().lower()
        #print self.btype


    def OnClick(self, event):
        """ Event bind to 'Generate' button """
        filter_ = Filter(self.fp, self.fs, self.gpass, self.gstop, ftype=self.ftype, btype=self.btype)
        filter_.step_response()
        filter_.phase_response()
        filter_.poles_zeros() 
        filter_.freq_response()

        if self.ftype == "ellip":
            pass
        else:
            ladder = LCladder(self.R1, self.R2, self.fp, self.fs, self.gpass, self.gstop, ftype=self.ftype, btype=self.btype) 
            if filter_.btype == "lowpass":
                if self.R1 == self.R2:
                    normalized_lc_ladder_elements = ladder.load_matched()
                    lc_ladder_elements = ladder.load_matched_denormalizer(normalized_lc_ladder_elements)
                else:
                    lc_ladder_elements = ladder.load_not_matched()
                    
                scheme = Scheme(self.R1, self.R2, filter_.ord)
                scheme.design(lc_ladder_elements) 
                
                frame = wx.Frame(None, size=(scheme.img_size[0], 250))
                panel = SchemePanel(frame)
                frame.Show()
        pyplot.show()


class SchemePanel(scrolled.ScrolledPanel):
    """ Scheme of LC circuit window"""
    def __init__(self, parent, bg_img='img.jpg'):
        scrolled.ScrolledPanel.__init__(self, parent=parent)
        self.SetupScrolling(scroll_x=True, rate_x=20)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.bg = wx.Bitmap(bg_img)
        self._width, self._height = self.bg.GetSize()

        sizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        hSizer.Add((1,1), 1, wx.EXPAND)
        hSizer.Add(sizer, 0, wx.TOP, 100)
        hSizer.Add((1,1), 0, wx.ALL, 75)
        self.SetSizer(hSizer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnSize(self, size):
        self.Layout()
        self.Refresh()

    def OnEraseBackground(self, evt):
        pass

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    def Draw(self, dc):
        cliWidth, cliHeight = self.GetClientSize()
        if not cliWidth or not cliHeight:
            return
        dc.Clear()
        xPos = (cliWidth - self._width)/2
        yPos = (cliHeight - self._height)/2
        dc.DrawBitmap(self.bg, xPos, yPos)


def dependencies_for_myprogram():
    """ Function for py2exe purposes only """
    from scipy.sparse.csgraph import _validation

app = wx.App(False)
frame = MyFrame(None, 'Analog Filter Designer')
app.MainLoop()
