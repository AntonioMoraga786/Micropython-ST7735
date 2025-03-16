from machine import SPI,Pin
import time

## commands
Doff = 0x28
Don = 0x29
Sout = 0x11
Xset = 0x2A
Yset = 0x2B
data = 0x2C


## constanst
black = 0x0000
pixel = 0x06
red = [0xFC,0x00,0x00]
green = [0x00,0xFC,0x00]
blue = [0x00,0x00,0xFC]


class Display():
    def __init__(self,sck,mosi,miso,cs,dc,res,f):
        self.pixels = [128,160]


        ## define SPI interface
        self.spi = SPI(0,baudrate = f,
                polarity=0,
                phase=0,
                bits=8,
                firstbit=SPI.MSB,
                sck=Pin(sck),
                mosi=Pin(mosi),
                miso=Pin(miso))

        self.cs = Pin(cs,Pin.OUT)    # Chip select pin
        self.DC = Pin(dc,Pin.OUT)    # Data/Command pin
        self.RES = Pin(res,Pin.OUT)   # Reset pin

        ## bring display out of reset
        self.DC.value(0)
        self.RES.value(1)
        time.sleep(0.2)
        self.cs.value(1)

        ## initialization sequence
        # get Screen out of sleep
        self.cs.value(0)
        self.spi.write(bytearray([Sout]))
        self.cs.value(1)

        # turn Display on
        self.cs.value(0)
        self.spi.write(bytearray([Don]))
        self.cs.value(1)

        ## setup complete

    def send(self):
        for paquet,mode in zip(self.data,self.dc):
            self.DC.value(mode)
            self.cs.value(0)
            self.spi.write(paquet)
            self.cs.value(1)

    def SetBackground(self,color):
        Xset = 0x2A
        Yset = 0x2B
        Data = 0x2C

        self.data = [Xset,0x00,0x00,0x00,128,
                Yset,0x00,0x00,0x00,160,
                Data]
        
        self.dc = [0,1,1,1,1,
                   0,1,1,1,1,
                   0]
        
        for i in range(len(self.data)):
            self.data[i] = bytearray([self.data[i]])

        self.send()
        self.data = []
        self.dc = []

        for row in range(int(self.pixels[1]/10)):
            self.data = []
            self.dc = []

            for i in range(10):
                for pixel in range(self.pixels[0]):
                    for V in color:
                        self.data.append(V)
                        self.dc.append(1)

                self.send()

    def UpdatePixel(self,pixels,edge):
        # commands
        Xset = 0x2A
        Yset = 0x2B
        Data = 0x2C

        # starting cordinates (px)
        self.Sx = edge[0]
        self.Sy = edge[1]

        # end cordinates (px)
        self.Ex = self.Sx + len(pixels[0]) - 1
        self.Ey = self.Sy + len(pixels) - 1

        ## calculate all paquets to be sent
        self.data = [Xset,0x00,self.Sx,0x00,self.Ex,
                     Yset,0x00,self.Sy,0x00,self.Ey,
                     Data]
        
        self.dc = [0,1,1,1,1,
                   0,1,1,1,1,
                   0]
        
        for i in range(len(self.data)):
            self.data[i] = bytearray([self.data[i]])
        
        for row in pixels:
            for pixel in row:
                for color in pixel:
                    self.data.append(color)
                    self.dc.append(1)

        ## send all the data
        self.send()