
class Frame():
    def __init__(self,portrait=True):
        self.dimensions = [128,160]# save dimesions of the 
        self.portrait = portrait# set orientation
        self.color = [0,0,0]
        self.objects = []
        edge = [160,128]

        if self.portrait:
            edge = [128,160]

        self.Q = [[[0,0],edge]]#Q for Quadrant

    def split(self,n,N,v):
        # n is the cuadrant to split as a list of n dimensions
        # split a quadrant into N secctions
        # split (v)ertical True/False
        o = self.getQ(n)# get the original quadrant

        # calculate the range of pixels from start to end of old quadrant
        r = [0,o[1][1]-o[0][1]]#the range will be [0,h]
        t = [0,1]# toggle list, only add the remainder pixels to the correct axis
        
        if v:
            r = [o[1][0]-o[0][0],0]# the range will be [w,0]
            t = [1,0]

        #calculate the step for each quadrant
        s = [r[0]//N,r[1]//N]# get the step pixel for each quadrant
        rem = r[0]%N+r[1]%N# get the remainder pixels

        # calculate the new quadrants
        new = []

        start = o[0]# get the start pixel position for the first quadrant
        fpos = o[1]# get the final position

        for I in range(N):
            rm = min(1,rem)# reminder multiplier (1 if there is a reminder, 0 if no reminder left to distribute)
            end = [start[0]+s[0]+t[0]*rm,start[1]+s[1]+t[1]*rm]
            new.append([start,[t[0]*end[0] + t[1]*fpos[0] , t[1]*end[1] + t[0]*fpos[1]]])
            start = end
            rem -= rm

        # sub value back into the quadrants list
        Q = self.Q

        # loop though all the dimensions to get the actual values of the quadrant
        for pos in n[:-1]:
            Q = Q[pos]

        Q[n[-1]] = new
        

    def ADD(self,object,n=[1]):
        ## add objects into the desired quadrant in the frame
        # object is the object to add to the window
        # n is the cuadrant in which the object is going to be added to
        self.objects.append(object(self.getQ(n)))

    def getQ(self,n):
        # function to get the cuadrant values
        # n is a nth dimensional list, each dimension is for each time each parent cuadrant was divided
        Q = self.Q

        # loop though all the dimensions to get the actual values of the quadrant
        for pos in n:
            Q = Q[pos]

        return Q# return the contents of the quadrant

    def Show(self,TFT):
        TFT.SetBackground(self.color)# set the background color of the display (about 5fps)

        ## display every object from the Frame in the Display
        for object in self.objects:
            TFT.update(object.output())
