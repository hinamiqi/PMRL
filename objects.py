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
        return ('white','black')
    
    def descr(self):
        return "void"
    
    def fdescr(self):
        return "Nothing to describe"

class Potion(Obj):
    bold = True
    def __init__(self, ingr):
        self.ingr = ingr
        #w = Water()
        #self.ingr.append(w)
        self.name = ""
        for ingr in self.ingr:
            self.name = self.name + ingr.descr()
        self.clr = self.ingr[0].color()
        
    def __str__(self):
        return "!"
    
    def color(self):
        return self.clr
        #return ('cyan','black')
    
    def descr(self):
        return self.name+" potion"
    
    def fdescr(self):
        return "Strange potion of "+self.name

class Water(Obj):
    def __str__(self):
        return "~"
    def color(self):
        return ('blue','black')
    def descr(self):
        return "water"
    def fdescr(self):
        return "That's definitely a water"

class Stick(Obj):

    def __str__(self):
        return "/"
    
    def color(self):
        return ('yellow','black')

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


class Ground(Obj):
    pickable = False
    def __init__(self,dftclr=None):
        self.dftclr = dftclr
    def __str__(self):
        return "."
    def color(self):
        #return ('GREEN','BLACK')
        if not self.dftclr:
            return ('green','black')
        else:
            return self.dftclr

    def descr(self):
        return 'ground'
    

class Tree(Obj):
    pickable = False
    #bold = False
    
    def __str__(self):
        return "&"
    def color(self):
        return 'green','black'
    def descr(self):
        return 'tree'
    def fdescr(self):
        return "Ordinary forest plant"

class BoldTree(Tree):
    penetrable = False
    bold = True
    def color(self):
        return 'green','black'


class Bush(Obj):
    pickable = False
    def __str__(self):
        return '"'
    def color(self):
        #return 2
        return ('green','black')
    def descr(self):
        return 'bush'
    def fdescr(self):
        return "Ordinary forest plant"

class Grass(Obj):
    def __str__(self):
        return "'"
    def color(self):
        #return 2
        return ('green','black')
    def descr(self):
        return 'grass'
    def fdescr(self):
        return "Ordinary forest plant"

class Stone(Obj):
    def __str__(self):
        return ","
    def color(self):
        return 'white','black'
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
        return 'black','white'
    def descr(self):
        return "rock"
    def fdescr(self):
        return "Solid, unpenetrable rock"

class Mushroom(Obj):
    def __str__(self):
        return ";"
    def color(self):
        return 'magenta','black'
    def descr(self):
        return 'mushroom'
    def fdescr(self):
        return "Tiny unknown fungus"


class Player(Obj):
    pickable = False
    def __str__(self):
        return "@"

