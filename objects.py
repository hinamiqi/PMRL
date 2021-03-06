import abc

'''OBJECTS'''

class Obj(metaclass=abc.ABCMeta):
    pickable = True
    penetrable = True
    bold = False
    @abc.abstractmethod
    def __str__(self):
        return " "

    def color(self):
        #return 2
        return ('w','b')
    
    def descr(self):
        return "void"
    
    def fdescr(self):
        return "Nothing to describe"



class Stick(Obj):

    def __str__(self):
        return "/"

    def descr(self):
        return "stick"
    
    def fdescr(self):
        return "Long piece of wood"

class Cauldron(Obj):
    pickable = False
    dropable = False
    def __str__(self):
        return "U"

    def descr(self):
        return "cauldron"
    
    def fdescr(self):
        return "Device for making potions"


class Bush(Obj):
    pickable = False
    def __str__(self):
        return '"'
    def color(self):
        #return 2
        return ('g','b')
    def descr(self):
        return 'bush'
    def fdescr(self):
        return "Ordinary forest plant"

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
        return 'ground'
    

class Tree(Obj):
    pickable = False
    bold = False
    def __str__(self):
        return "&"
    def color(self):
        return 'g','b'
    def descr(self):
        return 'tree'
    def fdescr(self):
        return "Ordinary forest plant"

class BoldTree(Tree):
    penetrable = False
    bold = True
    def color(self):
        return 'y','g'

class Stone(Obj):
    def __str__(self):
        return ","
    def color(self):
        return 'w','b'
    def descr(self):
        return 'stone'
    def fdescr(self):
        return "Small piece of stone"

class Rock(Obj):
    pickable = False
    penetrable = False
    def __str__(self):
        return "#"
    def color(self):
        return 'b','w'
    def descr(self):
        return "rock"
    def fdescr(self):
        return "Solid, unpenetrable rock"

class Mushroom(Obj):
    def __str__(self):
        return ";"
    def color(self):
        return 'm','b'
    def descr(self):
        return 'mushroom'
    def fdescr(self):
        return "Tiny unknown fungus"


class Player(Obj):
    pickable = False
    def __str__(self):
        return "@"
    def color(self):
        return 'w','b'
