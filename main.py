import numpy
from scipy import signal
from matplotlib import pyplot
from matplotlib.patches import Circle


class Filter(object):
    def __init__(self, fp, fs, gpass, gstop): 
        #Variables init.
        self.fp = fp
        self.fs = fs
        self.gpass =  gpass
        self.gstop = gstop

        #Computing omegas [rad/s]
        self.wp = 2 * numpy.pi * self.fp
        self.ws = 2 * numpy.pi * self.fs

        #Computing sampling frequency due to Whittaker-Nyquist-Kotelnikov-Shannon law.
        if self.wp > self.ws:
            self.sampling_w = 2 * self.wp
            self.btype = "highpass"
            self.xaxis_max = 2 * self.fp
        else:
            self.sampling_w = 2 * self.ws
            self.btype = 'lowpass'
            self.xaxis_max = 2 * self.fs

        #Normalizing omegas due to Nyquist frequency.
        self.wp_norm = self.wp / (self.sampling_w / 2)
        self.ws_norm = self.ws / (self.sampling_w / 2)
  
    def butterworth(self):
        #Order of filter.
        (ord, wn) = signal.buttord(self.wp_norm,
                                   self.ws_norm,
                                   self.gpass,
                                   self.gstop,
                                   analog=True)
        #Designing filter.
        (b, a) = signal.butter(ord,
                               wn,
                               btype=self.btype,
                               analog=True,
                               output='ba')

        #Frequency response of filter.
        (w, h) = signal.freqs(b, a, worN=1000)
        
        print ord
        print wn

        #Denormalizing variabels for ploting.
        w = (w * (self.sampling_w / 2)) / (2 * numpy.pi)
        wn = (wn * (self.sampling_w / 2)) / (2 * numpy.pi)


        #Plotting frequency response of filter.
        pyplot.figure()
        pyplot.plot(w, numpy.abs(h))
        pyplot.title('Filter Frequency Response' + "\n" + str(ord) + "th order Butterworth filter")
        pyplot.xlabel('Frequency [Hz]')
        pyplot.ylabel('Amplitude [V]')
        pyplot.grid(True)
        pyplot.axis([0, self.xaxis_max, 0, 1.2])
        pyplot.vlines(wn, 0, 1.2, color='k', linestyles='dashdot', label="wn")

        #Poles-zeros
        fig = pyplot.figure(figsize=(6, 6))
        (p, z, k) = signal.tf2zpk(b, a)
        z = -(z / min(numpy.real(z)))

        try:
            p = -(p / min(numpy.real(p)))
        except ValueError:
            pass

        #Plotting Poles-zeros
        pyplot.scatter(numpy.real(p), numpy.imag(p), marker='o', s=50)
        pyplot.scatter(numpy.real(z), numpy.imag(z), marker='x', s=100)
        circle = Circle((0, 0), radius=numpy.abs(z[1]), linestyle='dotted', fill=False)
        fig.gca().add_patch(circle)
        pyplot.axis([-1.2, 1.2, -1.2, 1.2])
        pyplot.vlines(0, -1.2, 1.2, color='k', linestyles='dotted')
        pyplot.hlines(0, -1.2, 1.2, color='k', linestyles='dotted')
        pyplot.xlabel('Real Part')
        pyplot.ylabel('Imaginary Part')
        pyplot.title('Pole-zeros')

        # #Step response
        (T, yout) = signal.step((b, a))

        #Plotting step response
        pyplot.figure()
        pyplot.plot(T, yout)
        pyplot.grid(True)
        pyplot.xlabel('Time')
        pyplot.xlim(0, max(T))
        pyplot.title('Impulse Response')
    

    def chebyshev(self):
        """To be implemented"""
        pass
pyplot.close('all')
filter1 = Filter(10000, 17000, 1.0, 25.0).butterworth()
#filter2 = Filter(155, 550, 1.0, 40.0).butterworth()

pyplot.show()
