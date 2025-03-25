
class Frame():
    def __init__(self,portrait=True):
        self.dimensions = [128,160]# save dimesions of the 
        self.portrait = portrait# set orientation
        self.color = [0,0,0]
        self.objects = []
        edge = [160,128]

        if self.portrait:
            edge = [128,160]

        self.Q = [[0,0],edge]

    def ADD(self,object,n=[1]):
        ## add objects into the desired cuadrant in the frame
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
