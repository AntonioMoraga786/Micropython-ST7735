from ST7735 import Frame

frame = Frame()# set frame to portrait by default
frame.split([0],2,True)
print(frame.Q)

frame.split([0,1],3,False)
print(frame.Q)

