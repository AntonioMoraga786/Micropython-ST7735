import ST7735
import machine
from Character import Character

# set machine frequency
machine.freq(240000000)

TFT = ST7735.Display(sck=18,
                     mosi=19,
                     miso=16,
                     cs=20,dc=14,
                     res=15,
                     f=40000000)

o = 0#bytearray([0])
m = 63#bytearray([63*4])

b = [o,o,o]
w = [m,m,m]
r = [m,o,o]
g = [o,m,o]
bl = [o,o,m]
y = [m,m,o]
p = [m,o,m]
lb = [o,m,m]

letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]

def scale(val,f):
    output = []
    
    for row in val:
        r = []
        for pixel in row:
            for I in range(f):
                r.append(pixel)
                
        for I in range(f):
            output.append(r)
            
    return output
    
TFT.color = p
TFT.SetBackground()

TFT.color = p
TFT.SetBackground()

TFT.color = p
TFT.SetBackground()

TFT.color = w
TFT.SetBackground()

text = """prueba de la pantalla numero dos"""

factor = 2

x = 0
y = 0



for letter in text:
    px = Character(letters.index(letter.upper()),p,b)
    
    # check if we are gonna overflow from screen
    if (x+1)*5*factor > 128:
        x = 0
        y += 1
    
    TFT.UpdatePixel(scale(px,factor),[x*5*factor,y*5*factor+3*y])
    
    x+=1
    
