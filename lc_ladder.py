from main import Filter
import numpy as np

class LCladder(Filter):
    def __init__(self, R1, R2, fp, fs, gpass, gstop, ftype, btype):
        Filter.__init__(self, fp, fs, gpass, gstop, ftype, btype)
        self.R1 = R1
        self.R2 = R2
 
    def phi_m(self, m):
        return (m * np.pi)/(2 * self.ord) #2.67

    def alpha(self):
        return np.power(abs((self.R1-self.R2)/(self.R1+self.R2)), 1.0 / self.ord) #2.66
    
    def cap_1(self):
        return (2.0 * np.sin(self.phi_m(1.0)))/(self.R1*(1.0-self.alpha()) * self.wn) #2.68

    def coil_1(self):
        return (2.0 * self.R1 * np.sin(self.phi_m(1.0)))/((1.0-self.alpha()) * self.wn) #2.64

if __name__ == '__main__':
    ladder = LCladder(100.0, 300.0, 100, 400, 3, 20, 'butter', 'lowpass')
    print 'alpha ', ladder.alpha()
    print 'phi ', ladder.phi_m(2)
    print 'cap_1 ', ladder.cap_1()
    print 'coil_1', ladder.coil_1()