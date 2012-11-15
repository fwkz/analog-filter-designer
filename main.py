from numpy import *
from scipy import signal
from matplotlib import pyplot
from matplotlib.patches import Circle


class Filter(object):
    def __init__(self, fp, fs, gpass, gstop, ftype): 
        #Variables init.
        self.fp = fp
        self.fs = fs
        self.gpass =  gpass
        self.gstop = gstop
        self.ftype = ftype

        #Computing omegas [rad/s]
        self.wp = 2 * pi * self.fp
        self.ws = 2 * pi * self.fs

        #Computing sampling frequency due to Whittaker-Nyquist-Kotelnikov-Shannon law.
        if self.wp > self.ws:
            self.sampling_w = 2 * self.wp
            self.btype = "highpass"
            #self.xaxis_max = 2 * self.fp
        else:
            self.sampling_w = 2 * self.ws
            self.btype = 'lowpass'
            #self.xaxis_max = 2 * self.fs

        #Normalizing omegas due to Nyquist frequency.
        self.wp_norm = self.wp / (self.sampling_w / 2)
        self.ws_norm = self.ws / (self.sampling_w / 2)
  
        if ftype == "butterworth":
            (self.ord, self.wn) = signal.buttord(self.wp_norm,
                                                 self.ws_norm,
                                                 self.gpass,
                                                 self.gstop,
                                                 analog=True)
            #Designing filter.
            (self.b, self.a) = signal.butter(self.ord,
                                             self.wn,
                                             btype=self.btype,
                                             analog=True,
                                             output='ba')

        (self.w, self.h) = signal.freqs(self.b, self.a, worN=1000)
        # print self.w
        # print self.ord
        # print self.wn

    def phase_response(self):
        """Plotting PHASE response of the filter."""
        pyplot.figure()
        pyplot.plot(self.w, unwrap((angle(self.h))))
        pyplot.grid(True)
        pyplot.xlim(0, 1)
        pyplot.title('Phase Response' + "\n" + str(self.ord) + "th order " + self.btype +" Butterworth filter")

        #Denormalizing variabels for ploting.
        # w = (w * (self.sampling_w / 2)) / (2 * pi)
        # wn = (wn * (self.sampling_w / 2)) / (2 * pi)

    def freq_response(self):
        """Plotting FREQUENCY response of filter."""
        pyplot.figure()
        pyplot.semilogx(self.w, abs(self.h))
        pyplot.title('Frequency Response' + "\n" + str(self.ord) + "th order " + self.btype +" Butterworth filter")
        pyplot.xlabel('Frequency [Hz]')
        pyplot.ylabel('Amplitude [V]')
        pyplot.grid(True)
        #pyplot.axis([0, 2, 0, 1.2])
        pyplot.vlines(self.wn, 0, 1.2, color='k', linestyles='dashdot', label="wn")

    def poles_zeros(self):
        """Computing and plotting POLES-ZEROS of the filter"""
        pyplot.figure(figsize=(6, 6))
        (p, z, k) = signal.tf2zpk(self.b, self.a)
        z = -(z / min(real(z)))

        #try:
        #    p = -(p / min(real(p)))
        #except ValueError:
        #    pass

        #Plotting Poles-zeros
        pyplot.scatter(real(p), imag(p), marker='o', s=50)
        pyplot.scatter(real(z), imag(z), marker='x', s=100)
        circle = Circle((0, 0), radius=abs(z[1]), linestyle='dotted', fill=False)
        pyplot.gca().add_patch(circle)
        pyplot.axis([-1.2, 1.2, -1.2, 1.2])
        pyplot.vlines(0, -1.2, 1.2, color='k', linestyles='dotted')
        pyplot.hlines(0, -1.2, 1.2, color='k', linestyles='dotted')
        pyplot.xlabel('Real Part')
        pyplot.ylabel('Imaginary Part')
        pyplot.title('Pole-zeros' + "\n" + str(self.ord) + "th order " + self.btype +" Butterworth filter")

    def step_response(self):
        """Computing and plotting STEP response of the filter."""
        (T, yout) = signal.step((self.b, self.a))

        #Plotting step response
        pyplot.figure()
        pyplot.plot(T, yout)
        pyplot.grid(True)
        pyplot.xlabel('Time')
        pyplot.xlim(0, max(T))
        pyplot.title('Impulse Response' + "\n" + str(self.ord) + "th order " + self.btype +" Butterworth filter")

    def chebyshev(self):
        """To be implemented"""
        pass

if __name__ == '__main__':    
    #filter1 = Filter(10000, 17000, 1.0, 25.0, ftype="butterworth").phase_response()
    filter2 = Filter(155, 50, 1.0, 40.0, ftype="butterworth")

    filter2.phase_response()
    filter2.poles_zeros()
    filter2.freq_response()
    filter2.step_response()

    pyplot.show()