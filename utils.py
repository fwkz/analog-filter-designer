import quantities as pq
from sys import exit


class Units(object):
    def __init__(self):
        self.mF = pq.UnitQuantity('millifarad', pq.farad/1e3, symbol='mF')
        self.uF = pq.UnitQuantity('microfarad', pq.farad/1e6, symbol='uF')
        self.nF = pq.UnitQuantity('nanofarad', pq.farad/1e9, symbol='nF')
        self.pF = pq.UnitQuantity('picofarad', pq.farad/1e12, symbol='pF')

        self.mH = pq.UnitQuantity('millihenry', pq.henry/1e3, symbol='mH')
        self.uH = pq.UnitQuantity('microhenry', pq.henry/1e6, symbol='uH')
        self.nH = pq.UnitQuantity('nanohenry', pq.henry/1e9, symbol='nH')
        self.pH = pq.UnitQuantity('picohenry', pq.henry/1e12, symbol='pH')

    def rescale(self, x, unit):
        if unit == "F":
            x = x * pq.farad

            self.milli = self.mF
            self.micro = self.uF
            self.nano = self.nF
            self.pico = self.pF
        elif unit == "H":
            x = x * pq.henry

            self.milli = self.mH
            self.micro = self.uH
            self.nano = self.nH
            self.pico = self.pH
        else:
            raise Exception("Unknown unit!")
            sys.exit(1)
        if x > 999e-12:
            if x > 999e-9:
                if x > 999e-6:
                    if x > 999e-3:
                        return x
                    else:
                        #rescale to mili
                        return x.rescale(self.milli)
                else:
                   #rescale to micro
                   return x.rescale(self.micro)
            else:
                #resale to pico
                return x.rescale(self.nano)
        else:
            return x.rescale(self.pico)

        return x


if __name__ == "__main__":
    units = Units()
    print units.rescale(1e-12, "F")
