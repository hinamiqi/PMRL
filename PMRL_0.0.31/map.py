class Map(dict):

    def __init__(self, size):
        self.x, self.y = size
        self.screen = None
        for j in range(self.y):
            for i in range(self.x):
                self[i, j] = Field(i,j)
        self.aloop = []
        self.console = None
        #self.prng = ((0,self.x),(0,self.y))
        self.prng = ((self.x//2-MXSIZE,self.x//2+MXSIZE),(self.y//2-MYSIZE,self.y//2+MYSIZE))

    #__repr__ = object.__repr__
    #__str__ = object.__str__

    def print(self, COLORS):
        prng = self.prng
        m = MAP_MARG
        for j in range(prng[1][0],prng[1][1]):
            n = MAP_MARG
            for i in range(prng[0][0],prng[0][1]):
                obj = self[i, j]
                cc = obj.color()
                self.screen.addstr(m, n, str(obj), curses.color_pair(COLORS[cc]))
                n+=1
            m+=1
        x = prng[0][1]-MXSIZE//2
        y = prng[1][1]-MYSIZE//2
        #that = self[x, y]
        #self.screen.addstr(MSIZE, 0, that.descr(), curses.color_pair(0))



    def place(self, obj, x, y, actions=False):
        "Places obj on the map on x, y."
        self[x, y].append(obj)
        obj.pos = x, y
        obj.map = self
        if actions:
            self.aloop.append(obj)

    def distance(self, obj1, obj2):
        """Returns the distance between obj1 and obj2"""
        x1, y1 = obj1.pos
        x2, y2 = obj2.pos
        xdist = abs(x1 - x2)
        ydist = abs(y1 - y2)
        dist = max(xdist, ydist)
        return dist

    def remove(self, obj, x, y):
        field = self[x, y]
        field.remove(obj)
