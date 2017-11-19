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
        return ('w','b')




class Stick(Obj):

    def __str__(self):
        return "/"

    def descr(self):
        return "Stick"

class Cauldron(Obj):
    pickable = False
    dropable = False
    def __str__(self):
        return "U"

    def descr(self):
        return "Cauldron"


class Bush(Obj):
    pickable = False
    def __str__(self):
        return '"'
    def color(self):
        #return 2
        return ('g','b')
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
            return ('g','b')
        else:
            return self.dftclr

    def descr(self):
        return 'Ground'

class Tree(Obj):
    pickable = False
    def __str__(self):
        return "&"
    def color(self):
        return 'g','b'
    def descr(self):
        return 'Tree'

class Stone(Obj):
    def __str__(self):
        return "o"
    def color(self):
        return 'w','b'
    def descr(self):
        return 'Stone'

class Rock(Obj):
    pickable = False
    penetrable = False
    def __str__(self):
        return "#"
    def color(self):
        return 'b','w'
    def descr(self):
        return "Rock"

class Mushroom(Obj):
    def __str__(self):
        return ","
    def color(self):
        return 'm','b'
    def descr(self):
        return 'Mushroom'


class Player():
    pickable = False
    def __str__(self):
        return "@"
    def color(self):
        return 'w','b'
