from main import Filter
import sys
import numpy as np
from utils import Units

class LCladder(Filter):
    def __init__(self, R1, R2, fp, fs, gpass, gstop, ftype, btype):
        Filter.__init__(self, fp, fs, gpass, gstop, ftype, btype)
        self.R1 = R1
        self.R2 = R2
        self.units = Units()
        """ TEST DATA FOR CHEBY """
        #self.gpass = 1.5
        #self.ord = 4
        #self.wn = np.pi * 100000.0

        """ TEST DATA FOR BUTTER """
        #self.ord = 4
        #self.wn = 100000.0

        if ftype == 'butter':
            self.alpha = self.alpha()
        elif ftype in ('cheby1', 'cheby2'):
            self.E = self.epsilon()
            self.gamma = self.gamma()
            self.a = self.a_help_var()
            self.a_ = self.a_prim_help_var()

            print "gamma ", self.gamma
            print "epsilon ", self.E
            print "a", self.a
            print "a_ ", self.a_
           
        #Frequency to pulsation
        self.wn = self.wn * np.pi * 2    

    def load_matched(self):
        if self.R1 != self.R2:
            raise Exception("Load not matched!")
            sys.exit(1)
        elif self.ftype in ('cheby1', 'cheby2'):
            lc_ladder = self.load_not_matched()
        elif self.ftype == "butter":
            lc_ladder = []
            for k in range(1, self.ord + 1):
                x = 2.0 * np.sin(((2.0*k-1.0)*np.pi)/(2.0*self.ord))
                x = x / self.R2
                lc_ladder.append(x)
        else:
            lc_ladder = None 

        return lc_ladder
        

    def load_not_matched(self):
        if self.R2 > self.R1:
            value_1 = self.coil_1() #Initial value
            initial_element_key = "L1"
            
            key_2 = 'C'
            value_2_unit = "F"

            key_1 = 'L'
            value_1_unit = "H"
        elif self.R2 < self.R1:
            value_1 = self.cap_1() #Initial value
            initial_element_key = "C1"

            key_2 = 'L'
            value_2_unit = "H"
            
            key_1 = 'C'
            value_1_unit = "F"
        else:
            if self.ftype == "butter":
                raise Exception("Load matched! Please execute LCladder.load_matched()")
                sys.exit(1)
            elif self.ftype in ("cheby1", "cheby2"):
                value_1 = self.coil_1() #Initial value
                initial_element_key = "L1"
                key_2 = 'C'
                value_2_unit = "F"

                key_1 = 'L'
                value_1_unit = "H"
            else:
                raise Exception("Unknown filter type.")
                sys.exit(1)
                  
        lc_ladder = {}
        m = self.ord/2
        lc_ladder[initial_element_key] = np.around(self.units.rescale(value_1, value_1_unit), 3)

        for m in range(1, m+1):
            if self.ftype == "butter":
                value_2 = (4.0 * np.sin(self.phi_m(4.0*m-3.0)) * np.sin(self.phi_m(4.0*m-1.0))) / (value_1 * np.power(self.wn, 2.0)*(1.0 - 2.0 * self.alpha*np.cos(self.phi_m(4.0*m-2.0))+np.power(self.alpha,2.0))) #2.65a
                value_1 = (4.0 * np.sin(self.phi_m(4.0*m-1.0)) * np.sin(self.phi_m(4.0*m+1.0))) / (value_2 * np.power(self.wn, 2.0)*(1.0 - 2.0 * self.alpha*np.cos(self.phi_m(4.0*m))+np.power(self.alpha,2.0))) #2.65b
            elif self.ftype in ("cheby1", "cheby2"):
                value_2 = (4.0 * np.sin(self.phi_m(4.0*m-3.0)) * np.sin(self.phi_m(4.0*m-1.0))) / (value_1 * np.power(self.wn, 2.0) * self.fm(2.0*m-1.0, np.sinh(self.a), np.sinh(self.a_)))
                value_1 = (4.0 * np.sin(self.phi_m(4.0*m-1.0)) * np.sin(self.phi_m(4.0*m+1.0))) / (value_2 * np.power(self.wn, 2.0) * self.fm(2.0*m, np.sinh(self.a), np.sinh(self.a_)))

            value_2_id = 2 * m
            value_2_key = key_2 + str(value_2_id)
            lc_ladder[value_2_key] = np.around(self.units.rescale(value_2, value_2_unit), 3)

            if len(lc_ladder) == self.ord:
                break

            value_1_id = 2 * m + 1
            value_1_key = key_1 + str(value_1_id)
            lc_ladder[value_1_key] = np.around(self.units.rescale(value_1, value_1_unit), 3)
        return lc_ladder


    def phi_m(self, m):
        phi_m = (m * np.pi) / (2 * self.ord) #2.67
        return phi_m


    def alpha(self):
        alpha = np.power(abs((self.R1-self.R2)/(self.R1+self.R2)), 1.0 / self.ord) #2.66
        return alpha


    def cap_1(self):
        """Computing initial capacitor value"""
        if self.ftype == 'butter':
            cap_1 = (2.0 * np.sin(self.phi_m(1.0)))/(self.R1*(1.0-self.alpha) * self.wn) #2.68
        elif self.ftype in ('cheby1', 'cheby2'):
            cap_1 = (2.0 * np.sin((np.pi/2.0)/self.ord))/(self.R1*(np.sinh(self.a) - np.sinh(self.a_)) * self.wn) #2.77
        else:
            cap_1 = None
        return cap_1


    def coil_1(self):
        """Computing initial coil value"""
        if self.ftype == 'butter':
            coil_1 = (2.0 * self.R1 * np.sin(self.phi_m(1.0)))/((1.0-self.alpha) * self.wn) #2.64
        elif self.ftype in ('cheby1', 'cheby2'):
            coil_1 = (2.0*self.R1*np.sin((np.pi/2.0)/self.ord))/((np.sinh(self.a) - np.sinh(self.a_)) * self.wn)  #2.73
        else:
            coil_1 = None
        return coil_1


    def a_help_var(self):
        """Chebyshev lc ladder help variable"""
        a = (1.0/4.0)*np.arcsinh(1.0/self.E) #2.72
        return a


    def a_prim_help_var(self):
        """Chebyshev lc ladder help variable"""
        a_ = (1.0/self.ord)*np.arcsinh(((np.sqrt(1.0 - np.power(self.gamma, 2.0)))/(self.E))) #2.72
        return a_


    def gamma(self):
        """Power transfer ratio. Chebyshev lc ladder help variable"""
        #gamma = ((np.sqrt(self.R1*self.R2))*np.sqrt(1.0 + np.power(self.E, 2.0)))/((self.R1+self.R2)/2.0)
        gamma = ((np.sqrt(self.R1*self.R2)))/((self.R1+self.R2)/2.0)
        return gamma


    def epsilon(self):
        """Maximum pass band ripple. Chebyshev lc ladder help variable"""
        E = np.sqrt(np.power(10.0, self.gpass/10.0)-1.0)
        return E


    def fm(self, m, x, y):
        "Chebyshev lc ladder help variable"
        fm = np.power(x, 2) + np.power(y, 2) + np.power((np.sin(self.phi_m(2.0*m))),2) - 2.0*x*y*np.cos(self.phi_m(2.0*m))
        return fm


    def prototype(self):
        if self.btype in ("bandpass", "bandstop"):
            omega0 = np.sqrt(self.fp[0]*self.fp[1])
            beta = (omega0)/(self.fp[1]-self.fp[0])
            print omega0, beta
        else:
            pass


if __name__ == '__main__':
    ladder = LCladder(1000.0, 200.0, [1000.0, 1500.0], [500.0, 2000], 3.0, 20, 'butter', 'bandpass')
    print ladder.ord
    # print ladder.load_not_matched()
    ladder.prototype()