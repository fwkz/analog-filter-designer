from PIL import Image
import sys

class Scheme(object):
    """ Draw circuit scheme. """

    def __init__(self, R1, R2, ord):
        self.R1 = R1
        self.R2 = R2
        self.ord = ord

        init =  Image.open("img/init.jpg")
        cap = Image.open("img/cap.jpg")
        coil = Image.open("img/coil.jpg")
        out = Image.open("img/out.jpg")
 
        self.cap_copy = cap.copy()
        self.init_copy = init.copy()
        self.out_copy = out.copy()
        self.coil_copy = coil.copy()
 
        self.input_size = init.size
        self.element_size = cap.size 
        self.out_size = out.size

    def design(self):
        img_size = (self.element_size[0]*self.ord + self.input_size[0] + self.out_size[0], self.element_size[1]) 

        self.img = Image.new("RGB", img_size)

        self.img.paste(self.init_copy, (0,0))
        self.width = self.input_size[0]

        if self.R2 > self.R1:
            cycle = 2
        else:
            cycle = 1

        for m in range(1, self.ord + 1):
            if cycle%2 == 0:
                self.__add_element("coil")
                cycle = cycle + 1
            else:
                self.__add_element("cap")
                cycle = cycle + 1

        self.img.paste(self.out_copy, (self.width, 0))
        self.img.show()

    def __add_element(self, element):
        if element == "cap":
            element = self.cap_copy
        elif element == "coil":
            element = self.coil_copy
        else:
            raise Exception("Element not recognized!")
            sys.exit(1)

        self.img.paste(element, (self.width, 0))
        self.width = self.width + self.element_size[0] 

if __name__ == "__main__":
    scheme = Scheme(100, 200, 5)
    scheme.design()