from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from sys import exit
from lc_ladder import LCladder

class Scheme(object):
    """ Draw circuit scheme. """

    def __init__(self, R1, R2, ord):
        """ Variables init """
        self.R1 = R1
        self.R2 = R2
        self.ord = ord

        init =  Image.open("img/init.jpg")
        cap = Image.open("img/cap.jpg")
        coil = Image.open("img/coil.jpg")
        out = Image.open("img/out.jpg")
 
        self.font = ImageFont.truetype("times.ttf", 11)

        self.cap_copy = cap.copy()
        self.init_copy = init.copy()
        self.out_copy = out.copy()
        self.coil_copy = coil.copy()
 
        self.input_size = init.size
        self.element_size = cap.size 
        self.out_size = out.size


    def design(self, lc_ladder_elements):
        """ Designing scheme of LC ladder circuit """

        #Compute image size
        self.lc_ladder_elements = lc_ladder_elements
        self.img_size = (self.element_size[0]*self.ord + self.input_size[0] + self.out_size[0], self.element_size[1]) 

        #New image
        self.img = Image.new("RGB", self.img_size)
        self.draw = ImageDraw.Draw(self.img)

        #Input of scheme
        self.img.paste(self.init_copy, (0,0))
        self.width = self.input_size[0]

        #Input load label
        text = str(self.R1/1000.0) + u" k\u03A9"
        self.draw.text((75, 45), text, font=self.font, fill="black")
        self.draw.text((90, 17), "R1", font=self.font, fill="black")

        if self.R2 >= self.R1:
            cycle = 2
        else:
            cycle = 1

        #Adding elements
        for m in range(1, self.ord + 1):
            if cycle%2 == 0:
                self.__add_element("coil", m)
                cycle = cycle + 1
            else:
                self.__add_element("cap", m)
                cycle = cycle + 1
        
        #Output of scheme
        self.img.paste(self.out_copy, (self.width, 0))

        #Output load label
        text = str(self.R2/1000.0) + u" k\u03A9" 
        self.draw.text((self.width+50, 75), "R2", font=self.font, fill="black")
        self.draw.text((self.width+75, 75), text, font=self.font, fill="black")

        #self.img.show()
        self.img.save('img.jpg')

    def __add_element(self, element, m):
        """ Private method. Add element picture to scheme """
        if element == "cap":
            element = self.cap_copy
            element_label = "C" + str(m)
            print self.lc_ladder_elements
            element_label = element_label + "=" + str(self.lc_ladder_elements[element_label])
            print element_label
            pos = (self.width + 5, 150)
        elif element == "coil":
            element = self.coil_copy
            element_label = "L" + str(m)
            element_label = element_label + "=" + str(self.lc_ladder_elements[element_label])
            print element_label
            pos = (self.width, 35)
        else:
            raise Exception("Element not recognized!")
            sys.exit(1)
  
        self.img.paste(element, (self.width, 0))
        self.width = self.width + self.element_size[0]

        self.draw.text(pos, element_label, font=self.font, fill="black") 
   
if __name__ == "__main__":
    ladder = LCladder(1500.0, 222.0, 500, 700, 1.0, 20, 'butter', 'lowpass')
    lc_ladder_elements = ladder.load_not_matched()

    print lc_ladder_elements

    scheme = Scheme(ladder.R1, ladder.R2, 7)
    scheme.design(lc_ladder_elements)