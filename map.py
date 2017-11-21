from curses import A_BOLD, A_NORMAL

MAP_MARG = 1

class Field(list):
    def __init__(self, x, y, defstr=" "):
        self.x, self.y = x, y
        self.defstr = defstr

    def uppest(self):
        try:
            upper = self[-1]
        except IndexError:
            return None
        else:
            return upper

    def __str__(self):
        try:
            upper = self[-1]
        except IndexError:
            return self.defstr
        else:
            return str(upper)

    def color(self):
        try:
            upper = self[-1]
        except IndexError:
            return ('w','b')
        else:
            return upper.color()

    def penetrable(self):
        for obj in self:
            if not obj.penetrable:
                return False
                break
        return True
    
    def bold(self):
        try:
            upper = self[-1]
        except IndexError:
            return None
        else:
            return upper.bold

    def descr(self):
        S = ""
        for obj in self[:-1]:
            S = S+" "+obj.descr()

        return S

    #def __repr__(self):
        #return "Field({0})".format(super().__repr__())


class Map(dict):

    def __init__(self, WSIZE,MXSIZE,MYSIZE):
        self.x, self.y = WSIZE, WSIZE
        self.mx, self.my = MXSIZE, MYSIZE
        self.screen = None
        for j in range(self.y):
            for i in range(self.x):
                self[i, j] = Field(i,j)
        self.aloop = []
        self.console = None
        self.prng = ((self.x//2-MXSIZE,self.x//2+MXSIZE),(self.y//2-MYSIZE,self.y//2+MYSIZE))

    #__repr__ = object.__repr__
    #__str__ = object.__str__

    def print(self, stdscr, clrs):
        prng = self.prng
        m = MAP_MARG
        for j in range(prng[1][0],prng[1][1]):
            n = MAP_MARG
            for i in range(prng[0][0],prng[0][1]):
                try:
                    obj = self[i, j]
                    cc = obj.color()
                    if obj.bold():
                        attr = A_BOLD
                    else:
                        attr = A_NORMAL
                    
                    #stdscr.attron(A_BOLD | clrs[cc])
                    stdscr.addstr(m, n, str(obj), clrs[cc] | attr )
                    
                except KeyError:
                    pass
                n+=1
            m+=1
        x = prng[0][1]-self.mx//2
        y = prng[1][1]-self.my//2

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
