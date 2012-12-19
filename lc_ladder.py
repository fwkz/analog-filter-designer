from main import Filter
import numpy as np

class LCladder(Filter):
    def __init__(self, R1, R2, fp, fs, gpass, gstop, ftype, btype):
        Filter.__init__(self, fp, fs, gpass, gstop, ftype, btype)
        self.R1 = R1
        self.R2 = R2
        self.alpha = self.alpha()

        #Frequency to pulsation
        self.wn = self.wn * np.pi * 2
        print self.ord

        if self.R2 > self.R1:
            print self.L_2m_minus_one(self.ord)


    def L_2m_minus_one(self, ord):
        lc_ladder = {}
        m = ord/2
        L_value = self.coil_1() #Initial L value
        lc_ladder['L1'] = L_value

        for m in range(1, m+1):
            C_value = (4.0 * np.sin(self.phi_m(4*m-3)) * np.sin(self.phi_m(4*m-1))) / (L_value * np.power(self.wn, 2)*(1.0 - 2.0 * self.alpha*np.cos(self.phi_m(4*m))+np.power(self.alpha,2))) #2.65a
            L_value = (4.0 * np.sin(self.phi_m(4*m-1)) * np.sin(self.phi_m(4*m+1))) / (C_value * np.power(self.wn, 2)*(1.0 - 2.0 * self.alpha*np.cos(self.phi_m(4*m))+np.power(self.alpha,2))) #2.65b
            
            C_id = 2 * m
            cap_key = "C" + str(C_id)
            lc_ladder[cap_key] = C_value

            if len(lc_ladder) == 4:
                break

            L_id = 2 * m + 1
            coil_key = "L" + str(L_id)
            lc_ladder[coil_key] = L_value

        return lc_ladder

    def phi_m(self, m):
        return (m * np.pi) / (2 * self.ord) #2.67

    def alpha(self):
        return np.power(abs((self.R1-self.R2)/(self.R1+self.R2)), 1.0 / self.ord) #2.66
    
    def cap_1(self):
        return (2.0 * np.sin(self.phi_m(1.0)))/(self.R1*(1.0-self.alpha) * self.wn) #2.68

    def coil_1(self):
        return (2.0 * self.R1 * np.sin(self.phi_m(1.0)))/((1.0-self.alpha) * self.wn) #2.64

if __name__ == '__main__':
    ladder = LCladder(500.0, 1000.0, 500, 1000, 3, 20, 'butter', 'lowpass')
    # # print 'alpha ', ladder.alpha()
    print 'phi ', ladder.phi_m(1)
    # print 'cap_1 ', ladder.cap_1()
    # print 'coil_1', ladder.coil_1()