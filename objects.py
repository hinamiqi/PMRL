import abc

'''OBJECTS'''

class Obj(metaclass=abc.ABCMeta):
    pickable = True
    penetrable = True
    @abc.abstractmethod
    def __str__(self):
        return " "

    def color(self):
        #return 2
        return ('WHITE','BLACK')




class Stick(Obj):

    def __str__(self):
        return "/"

    def descr(self):
        return "Stick"


class Bush(Obj):
    pickable = False
    def __str__(self):
        return '"'
    def color(self):
        #return 2
        return ('GREEN','BLACK')
    def descr(self):
        return 'Bush'

class Ground(Obj):
    pickable = False
    def __init__(self,dftclr=None):
        self.dftclr = dftclr
    def __str__(self):
        return "."
    def color(self):
        #return ('GREEN','BLACK')
        if not self.dftclr:
            return ('GREEN','BLACK')
        else:
            return self.dftclr
            
    def descr(self):
        return 'Ground'

class Tree(Obj):
    pickable = False
    def __str__(self):
        return "&"
    def color(self):
        return 'GREEN','BLACK'
    def descr(self):
        return 'Tree'

class Stone(Obj):
    def __str__(self):
        return "o"
    def color(self):
        return 'WHITE','BLACK'
    def descr(self):
        return 'Stone'

class Rock(Obj):
    pickable = False
    penetrable = False
    def __str__(self):
        return "#"
    def color(self):
        return 'BLACK','WHITE'
    def descr(self):
        return "Rock"

class Mushroom(Obj):
    def __str__(self):
        return ","
    def color(self):
        return 'MAGENTA','BLACK'
    def descr(self):
        return 'Mushroom'


class Player():
    pickable = False
    def __str__(self):
        return "@"
    def color(self):
        return 'WHITE','BLACK'
