from numpy import *
from scipy import signal
from matplotlib import pyplot
from matplotlib.patches import Circle


class Filter(object):
    def __init__(self, fp, fs, gpass, gstop, ftype, btype): 
        #Variables init.
        self.fp = fp
        self.fs = fs
        self.gpass =  gpass
        self.gstop = gstop
        self.ftype = ftype

        #Filter type for plot's title.
        types_dict = {"butter":"Butterworth", "cheby1":"Chebyshev I", "cheby2":"Chebyshev II", "ellip": "Cauer"}
        self.ftype_plot = types_dict[ftype]

        if type(self.fp) and type(self.fs) is list:
            #Computing omegas [rad/s]
            self.wp = [fp * 2 * pi for fp in self.fp]
            self.ws = [fs * 2 * pi for fs in self.fs]
            self.btype = btype

            #Computing sampling frequency due to Whittaker-Nyquist-Kotelnikov-Shannon law.
            if max(self.wp) > max(self.ws):
                self.sampling_w = 2 * max(self.wp)
            else:
                self.sampling_w = 2 * max(self.ws)

            #Normalizing omegas due to Nyquist frequency.
            self.wp_norm = [wp / (self.sampling_w / 2) for wp in self.wp]
            self.ws_norm = [ws / (self.sampling_w / 2) for ws in self.ws]
        else:
            #Computing omegas [rad/s]
            self.wp = 2 * pi * self.fp
            self.ws = 2 * pi * self.fs

            #Computing sampling frequency due to Whittaker-Nyquist-Kotelnikov-Shannon law.
            if self.wp > self.ws:
                self.sampling_w = 2 * self.wp
                self.btype = "highpass"
            else:
                self.sampling_w = 2 * self.ws
                self.btype = 'lowpass'

            #Normalizing omegas due to Nyquist frequency.
            self.wp_norm = self.wp / (self.sampling_w / 2)
            self.ws_norm = self.ws / (self.sampling_w / 2)

        #Computing filters order and maximum value of X axis.
        if ftype == "butter":
            if self.btype == 'highpass':
                self.xaxis_max = 0.2
            else:
                self.xaxis_max = 0.15
            (self.ord, self.wn) = signal.buttord(self.wp_norm,
                                                 self.ws_norm,
                                                 self.gpass,
                                                 self.gstop,
                                                 analog=True)
        elif ftype == "cheby1":
            if self.btype == 'highpass':
                self.xaxis_max = 0.6
            else:
                self.xaxis_max = 0.15
            (self.ord, self.wn) = signal.cheb1ord(self.wp_norm,
                                                  self.ws_norm,
                                                  self.gpass,
                                                  self.gstop,
                                                  analog=True)
        elif ftype == "cheby2":
            if self.btype == 'highpass':
                self.xaxis_max = 0.2
            else:
                self.xaxis_max = 0.3
            (self.ord, self.wn) = signal.cheb2ord(self.wp_norm,
                                                  self.ws_norm,
                                                  self.gpass,
                                                  self.gstop,
                                                  analog=True)
        elif ftype == "ellip":
            if self.btype == 'highpass':
                self.xaxis_max = 0.6
            else:
                self.xaxis_max = 0.2
            (self.ord, self.wn) = signal.ellipord(self.wp_norm,
                                                  self.ws_norm,
                                                  self.gpass,
                                                  self.gstop,
                                                  analog=True)
            
        #Designing filter.
        (self.b, self.a) = signal.iirfilter(self.ord,
                                            self.wn,
                                            rp=self.gpass, 
                                            rs=self.gstop, 
                                            btype=self.btype, 
                                            analog=True, 
                                            output='ba', 
                                            ftype=ftype)

        #Frequency response of analog filter.
        (self.w, self.h) = signal.freqs(self.b, self.a, worN=1000)

        #Denormalizing variabels for ploting.
        self.w = (self.w * (self.sampling_w / 2)) / (2 * pi)
        self.wn = (self.wn * (self.sampling_w / 2)) / (2 * pi)

    def phase_response(self):
        """Plotting PHASE response of the filter."""
        pyplot.figure()
        pyplot.plot(self.w, unwrap((angle(self.h))))
        pyplot.grid(True)
        pyplot.xlim(0, max(self.w))
        pyplot.title('Phase Response' + "\n" + str(self.ord) + "th order " + self.btype + " " + self.ftype_plot + " filter")

    def freq_response(self):
        """Plotting FREQUENCY response of filter."""
        pyplot.figure()
        pyplot.plot(self.w, abs(self.h))
        pyplot.title('Frequency Response' + "\n" + str(self.ord) + "th order " + self.btype + " " + self.ftype_plot + " filter")
        pyplot.xlabel('Frequency')
        pyplot.ylabel('Amplitude')
        pyplot.grid(True)
        self.axis_formatter = [0, max(self.w)*self.xaxis_max, 0, 1.2]
        pyplot.axis(self.axis_formatter)
        pyplot.vlines(self.wn, 0, 1.2, color='k', linestyles='dashdot', label="wn")

    def poles_zeros(self):
        """Computing and plotting POLES-ZEROS of the filter"""
        pyplot.figure(figsize=(6, 6))
        (p, z, k) = signal.tf2zpk(self.b, self.a)
        
        if self.ftype == 'butter':
            z = -(z / min(real(z)))
            circle = Circle((0, 0), radius=abs(max(z)), linestyle='dotted', fill=False)
            try:
               p = -(p / min(real(p)))
            except ValueError:
               pass
        else:
            circle = Circle((0, 0), radius=1, linestyle='dotted', fill=False)

        #Plotting Poles-zeros
        pyplot.scatter(real(p), imag(p), marker='o', s=50)
        pyplot.scatter(real(z), imag(z), marker='x', s=100)

        pyplot.xlabel('Real Part')
        pyplot.ylabel('Imaginary Part')
        pyplot.title('Pole-zeros' + "\n" + str(self.ord) + "th order " + self.btype + " " + self.ftype_plot + " filter")

        #Formatting plot.
        pyplot.gca().add_patch(circle)
        limits = []
        limits.append(max(pyplot.gca().get_xlim()))
        limits.append(max(pyplot.gca().get_ylim()))
        max_limit = max(limits)
        
        if max_limit < 1.2:
            max_limit = 1.2

        pyplot.axis([-max_limit, max_limit, -max_limit, max_limit])
        pyplot.vlines(0, -max_limit, max_limit, color='k', linestyles='dotted')
        pyplot.hlines(0, -max_limit, max_limit, color='k', linestyles='dotted')

    def step_response(self):
        """Computing and plotting STEP response of the filter."""
        (T, yout) = signal.step((self.b, self.a))

        #Plotting step response
        pyplot.figure()
        pyplot.plot(T, yout)
        pyplot.grid(True)
        pyplot.xlabel('Time')
        pyplot.xlim(0, max(T))
        pyplot.title('Impulse Response' + "\n" + str(self.ord) + "th order " + self.btype + " " + self.ftype_plot + " filter")


if __name__ == '__main__':    
    filter1 = Filter([500, 1000], [600, 900], 1.0, 20.0, ftype="butter")
    filter2 = Filter([500, 1000], [300, 1200], 1.0, 20.0, ftype="cheby1")
    filter3 = Filter([500, 1000], [300, 1200], 1.0, 20.0, ftype="cheby2")
    filter4 = Filter([500, 1000], [300, 1200], 1.0, 20.0, ftype="ellip")

    # filter1 = Filter(100, 150, 1.0, 40.0, ftype="butter")
    # filter2 = Filter(100, 150, 1.0, 40.0, ftype="cheby1")
    # filter3 = Filter(100, 150, 1.0, 20.0, ftype="cheby2")
    # filter4 = Filter(100, 150, 1.0, 40.0, ftype="ellip")

    filter1.freq_response()
    filter2.freq_response()
    filter3.freq_response()
    filter4.freq_response()

    # filter2.poles_zeros()
    # filter2.freq_response()
    # filter2.step_response()
    # filter2.phase_response()

    pyplot.show()