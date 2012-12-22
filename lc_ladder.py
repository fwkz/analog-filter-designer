from main import Filter
import numpy as np

class LCladder(Filter):
    def __init__(self, R1, R2, fp, fs, gpass, gstop, ftype, btype):
        Filter.__init__(self, fp, fs, gpass, gstop, ftype, btype)
        self.R1 = R1
        self.R2 = R2

        """TEST DATA FOR CHEBY"""
        #self.gpass = 1.5
        #self.ord = 4
        #self.wn = np.pi * 100000.0

        """TEST DATA FOR BUTTER"""
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

    def load_not_matched(self):
        if self.R2 > self.R1:
            value_1 = self.coil_1() #Initial value
            initial_element_key = "L1"
            key_2 = 'C'
            key_1 = 'L'
        else:
            value_1 = self.cap_1() #Initial value
            initial_element_key = "C1"
            key_2 = 'L'
            key_1 = 'C'

        lc_ladder = {}
        m = self.ord/2
        lc_ladder[initial_element_key] = value_1

        for m in range(1, m+1):
            if self.ftype == "butter":
                value_2 = (4.0 * np.sin(self.phi_m(4.0*m-3.0)) * np.sin(self.phi_m(4.0*m-1.0))) / (value_1 * np.power(self.wn, 2.0)*(1.0 - 2.0 * self.alpha*np.cos(self.phi_m(4.0*m-2.0))+np.power(self.alpha,2.0))) #2.65a
                value_1 = (4.0 * np.sin(self.phi_m(4.0*m-1.0)) * np.sin(self.phi_m(4.0*m+1.0))) / (value_2 * np.power(self.wn, 2.0)*(1.0 - 2.0 * self.alpha*np.cos(self.phi_m(4.0*m))+np.power(self.alpha,2.0))) #2.65b
            elif self.ftype in ("cheby1", "cheby2"):
                value_2 = (4.0 * np.sin(self.phi_m(4.0*m-3.0)) * np.sin(self.phi_m(4.0*m-1.0))) / (value_1 * np.power(self.wn, 2.0) * self.fm(2.0*m-1.0, np.sinh(self.a), np.sinh(self.a_)))
                value_1 = (4.0 * np.sin(self.phi_m(4.0*m-1.0)) * np.sin(self.phi_m(4.0*m+1.0))) / (value_2 * np.power(self.wn, 2.0) * self.fm(2.0*m, np.sinh(self.a), np.sinh(self.a_)))

            value_2_id = 2 * m
            value_2_key = key_2 + str(value_2_id)
            lc_ladder[value_2_key] = value_2

            if len(lc_ladder) == self.ord:
                break

            value_1_id = 2 * m + 1
            value_1_key = key_1 + str(value_1_id)
            lc_ladder[value_1_key] = value_1
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
        return cap_1


    def coil_1(self):
        """Computing initial coil value"""
        if self.ftype == 'butter':
            coil_1 = (2.0 * self.R1 * np.sin(self.phi_m(1.0)))/((1.0-self.alpha) * self.wn) #2.64
        elif self.ftype in ('cheby1', 'cheby2'):
            coil_1 = (2.0*self.R1*np.sin((np.pi/2.0)/self.ord))/((np.sinh(self.a) - np.sinh(self.a_)) * self.wn)  #2.73
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
        """Chebyshev pass band ripple"""
        E = np.sqrt(np.power(10.0, self.gpass/10.0)-1.0)
        return E


    def fm(self, m, x, y):
        fm = np.power(x, 2) + np.power(y, 2) + np.power((np.sin(self.phi_m(2.0*m))),2) - 2.0*x*y*np.cos(self.phi_m(2.0*m))
        return fm


    '''
    def R1_gt_R2(self, ord):
        """TEST R1 > R2"""

        lc_ladder = {}
        """TEST"""
        self.ord = 4.0
        self.wn = 100000.0
        """"""""
        m = ord/2
        C_value = self.cap_1() #Initial L value
        lc_ladder['C1'] = C_value

        for m in range(1, m+1):
            L_value = (4.0 * np.sin(self.phi_m(4.0*m-3.0)) * np.sin(self.phi_m(4.0*m-1.0))) / (C_value * np.power(self.wn, 2.0)*(1.0 - 2.0 * self.alpha*np.cos(self.phi_m(4.0*m-2.0))+np.power(self.alpha,2.0))) #2.65a
            C_value = (4.0 * np.sin(self.phi_m(4.0*m-1.0)) * np.sin(self.phi_m(4.0*m+1.0))) / (L_value * np.power(self.wn, 2.0)*(1.0 - 2.0 * self.alpha*np.cos(self.phi_m(4.0*m))+np.power(self.alpha,2.0))) #2.65b

            L_id = 2 * m
            coil_key = "L" + str(L_id)
            lc_ladder[coil_key] = L_value

            if len(lc_ladder) == self.ord:
                break

            C_id = 2 * m + 1
            cap_key = "C" + str(C_id)
            lc_ladder[cap_key] = C_value
        return lc_ladder


    def R2_gt_R1(self, ord):
        """TEST R2 > R1"""

        lc_ladder = {}
        m = ord/2
        L_value = self.coil_1() #Initial L value
        lc_ladder['L1'] = L_value

        for m in range(1, m+1):
            C_value = (4.0 * np.sin(self.phi_m(4*m-3)) * np.sin(self.phi_m(4*m-1))) / (L_value * np.power(self.wn, 2)*(1.0 - 2.0 * self.alpha*np.cos(self.phi_m(4*m-2.0))+np.power(self.alpha,2))) #2.65a
            L_value = (4.0 * np.sin(self.phi_m(4*m-1)) * np.sin(self.phi_m(4*m+1))) / (C_value * np.power(self.wn, 2)*(1.0 - 2.0 * self.alpha*np.cos(self.phi_m(4*m))+np.power(self.alpha,2))) #2.65b
            
            C_id = 2 * m
            cap_key = "C" + str(C_id)
            lc_ladder[cap_key] = C_value

            if len(lc_ladder) == self.ord:
                break

            L_id = 2 * m + 1
            coil_key = "L" + str(L_id)
            lc_ladder[coil_key] = L_value
        return lc_ladder
    '''

if __name__ == '__main__':
    ladder = LCladder(1500.0, 620.0, 500, 700, 1.0, 20, 'butter', 'lowpass')
    print ladder.ord
    print ladder.load_not_matched()  

    # print 'phi ', ladder.phi_m(1)
    # print 'alpha ', ladder.alpha()
    # print 'cap_1 ', ladder.cap_1()
    # print 'coil_1', ladder.coil_1()