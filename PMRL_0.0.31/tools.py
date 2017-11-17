from collections import defaultdict

class InputHandler:

    def __init__(self, blocking):
        self.callbacks = defaultdict(lambda: nothing)
        self._screen = None
        self.blocking = blocking

    @property
    def blocking(self):
        return self._blocking

    @blocking.setter
    def blocking(self, value):
        if self._screen:
            self._screen.nodelay(bool(value))
        self._blocking = value

    @property
    def screen(self):
        if not self._screen:
            raise RuntimeError("{0} isn't initialized!".format(self))
        return self._screen

    @screen.setter
    def screen(self, value):
        self._screen = value
        try:
            value.nodelay(bool(self.blocking))
        except NameError:
            raise TypeError("screen must be a valid screen object!")

    @screen.deleter
    def screen(self):
        self._screen = None

    def get_input(self):
        if self.blocking:
            time.sleep(self.blocking)
        try:
            inp = self.screen.getch()
        except curses.error:
            pass
        else:
            self.callbacks[inp](inp)

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
            return ('WHITE','BLACK')
        else:
            return upper.color()
    
    def penetrable(self):
        for obj in self:
            if not obj.penetrable:
                return False
                break
        return True
        

    def descr(self):
        #try:
            #upper = self[-2]
        #except IndexError:
            #return 'Void'
        #else:
            #return upper.descr()
        #for obj in self:
            #if obj.pickable:
                #return obj.descr()
            #else:
                #return ''
        S = ""
        for obj in self[:-1]:
            S = S+" "+obj.descr()
        
        return S

    #def __repr__(self):
        #return "Field({0})".format(super().__repr__())
