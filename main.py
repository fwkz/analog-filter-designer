import numpy
from scipy import signal
from matplotlib import pyplot


class Filter(object):
    def __init__(self, fp, fs, gpass, gstop): 
        #Variables init.
        self.fp = fp
        self.fs = fs
        self.gpass =  gpass
        self.gstop = gstop
        self.sample_freq = 1000.0

        #Computing omegas [rad/s]
        self.wp = 2 * numpy.pi * self.fp
        self.ws = 2 * numpy.pi * self.fs

        ##Computing sampling frequency due to Whittaker-Nyquist-Kotelnikov-Shannon law.
        if self.wp > self.ws:
            self.sampling_w = 2 * self.wp
        else:
            self.sampling_w = 2 * self.ws
        
        #Normalizing omegas due to Nyquist frequency.
        self.wp_norm = self.wp / (self.sampling_w / 2)
        self.ws_norm = self.ws / (self.sampling_w / 2)
  
    def butterworth(self):
        (ord, wn) = signal.buttord(self.wp_norm, self.ws_norm, self.gpass, self.gstop, analog=True)
        print ord
        print wn

        (b, a) = signal.butter(ord, wn, btype="lowpass", analog=True, output='ba')
        (w, h) = signal.freqs(b, a, worN=1000)

        # filter frequency response
        pyplot.semilogx(w, numpy.abs(h))
        pyplot.title('Filter Frequency Response')
        pyplot.text(5e-2, 1e-3, str(ord) + "-th order Butterworth filter")
        pyplot.grid(True)
        pyplot.vlines(wn, 0, 1.2, color='k', linestyles='dashdot', label="wn")
        pyplot.show()
    
    def chebyshev(self):
        """To be implemented"""
        pass

filter = Filter(2000, 1000, 1.0, 20.0).butterworth()