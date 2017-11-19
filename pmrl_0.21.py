#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import curses
import random
import abc
from collections import defaultdict


'''CONSTS'''
WSIZE = 100
MXSIZE = 30
MYSIZE = 20
LSIZE = 25
TREE_PR = 0.2
BUSH_PR = 0.3
STONE_PR = 0.5


'''MAIN CLASSES'''

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

    def descr(self):
        try:
            upper = self[-2]
        except IndexError:
            return 'Void'
        else:
            return upper.descr()

    #def __repr__(self):
        #return "Field({0})".format(super().__repr__())

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

    def print(self):
        prng = self.prng
        m = 0
        for j in range(prng[1][0],prng[1][1]):
            n = 0
            for i in range(prng[0][0],prng[0][1]):
                obj = self[i, j]
                cc = obj.color()
                self.screen.addstr(m, n, str(obj), curses.color_pair(self.console.color_pallete[cc]))
                n+=1
            m+=1
        x = prng[0][1]-MXSIZE//2
        y = prng[1][1]-MYSIZE//2
        that = self[x, y]
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


class Console(object):

    def __init__(self, map, inp, logsize):
        self.map = map
        map.console = self
        self.inp = inp
        #self.inp = InputHandler(False)
        self.inp.callbacks[27] = self.set_end
        self.end = False
        self.logsize = logsize
        self.init_curses()

    def init_curses(self):
        try:
            fullwin = curses.initscr()
            self.init_colors()
            #xsize, ysize = self.map.x, self.map.y
            xsize, ysize = MXSIZE, MYSIZE
            logx = self.logsize
            screen = curses.newpad(ysize+1 , xsize+1 )
            log = curses.newwin(MYSIZE+2, logx)
            panel = curses.newwin(1, MXSIZE, MYSIZE, logx)
            panel.scrollok(False)
            log.scrollok(True)
            curses.noecho()
            curses.cbreak()
            orig = curses.curs_set(0)
            screen.keypad(1)
            self.run(screen, fullwin, log, panel)
        finally:
            curses.nocbreak()
            try:
                pad.keypad(0)
            except NameError:
                pass
            curses.echo()
            try:
                curses.curs_set(orig)
            except:
                pass
            curses.endwin()

    def init_colors(self):
        curses.start_color()
        color_names =     ['RED',
                           'GREEN',
                           'YELLOW',
                           'BLUE',
                           'MAGENTA',
                           'CYAN',
                           'WHITE',
                           'BLACK']
        color_list =      [curses.COLOR_RED,
                           curses.COLOR_GREEN,
                           curses.COLOR_YELLOW,
                           curses.COLOR_BLUE,
                           curses.COLOR_MAGENTA,
                           curses.COLOR_CYAN,
                           curses.COLOR_WHITE,
                           curses.COLOR_BLACK]
        self.color_pallete = {}
        N = 1
        for n in range(len(color_list)):
            for m in range(len(color_list)):
                curses.init_pair(N, color_list[n], color_list[m])
                self.color_pallete[(color_names[n],color_names[m])]=N
                N+=1

    def logwrite(self, text):
        """Write text to the log"""
        self.log.addstr(self.log.getmaxyx()[0] - 1, 0, text)
        self.log.scroll()
        self.log.refresh()

    def panelwrite(self, text):
        self.panel.clear()
        self.panel.addstr(0, 0, text)
        self.panel.refresh()


    def refresh(self, screen, fullwin):
        fullmaxy, fullmaxx = fullwin.getmaxyx()
        padmaxy, padmaxx = screen.getmaxyx()
        logwidth = MYSIZE+2
        self.map.print()
        screen.refresh(0, 0, 0, logwidth,
                       fullmaxy - 1, fullmaxx - 1)
        x = self.map.prng[0][1]-MXSIZE//2
        y = self.map.prng[1][1]-MYSIZE//2
        that = self.map[x, y]
        self.panelwrite(that.descr())
        self.inp.get_input()

    def run(self, screen, fullwin, log, panel):
        self.log = log
        self.panel = panel
        self.map.screen = screen
        self.inp.screen = screen
        while True:
            self.refresh(screen, fullwin)
            if self.end:
                break

    def set_end(self, _=None):
        self.end = True

'''OBJECTS'''

class Obj(metaclass=abc.ABCMeta):
    pickable = True

    @abc.abstractmethod
    def __str__(self):
        return " "

    def color(self):
        #return 2
        return ('WHITE','BLACK')




class Stick(Obj):
    pickable = False

    def __str__(self):
        return "/"

    def descr(self):
        return "Stick"


class Bush(Obj):
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
        if not self.dftclr:
            return ('GREEN','BLACK')
        else:
            return self.dftclr
    def descr(self):
        return 'Ground'

class Tree(Obj):
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
    def __str__(self):
        return "#"
    def color(self):
        return 'BLACK','WHITE'
    def descr(self):
        return "UCANTREADTHAT"

class Mushroom(Obj):
    def __str__(self):
        return ","
    def color(self):
        return 'WHITE','BLACK'
    def descr(self):
        return 'Mushroom'


class Player():
    def __str__(self):
        return "@"
    def color(self):
        return 'WHITE','BLACK'

class World(object):
    def __init__(self):
        self.size = WSIZE
        self.init_world_obj()
        self.create_world()
        self.create_plants()

    def init_world_obj(self):
        self.plants = {
                        Tree():0.1,
                        Bush():0.05,
                      }
        self.objects = {
                          Stone():0.0005,
                          Mushroom():0.00001
                        }


    def create_world(self):
        self.map = Map((WSIZE,WSIZE))
        for i in range(WSIZE):
            for j in range(WSIZE):
                if i<=MXSIZE//2 or i>=WSIZE-MXSIZE//2 \
                   or j<=MYSIZE//2 or j>=WSIZE-MYSIZE//2:
                    obj = Rock()
                else:
                    rndclr = (random.choice((\
                                               'GREEN',\
                                               'YELLOW',\
                                               'WHITE',\
                                               'RED')),'BLACK')
                    obj = Ground(rndclr)
                self.map.place(obj,i,j)
                st = Stick()
                self.map.place(st,WSIZE//2+3,WSIZE//2+3)

    def create_plants(self):
        for i in range(MXSIZE//2,WSIZE-MXSIZE//2):
            for j in range(MYSIZE//2,WSIZE-MYSIZE//2):
                for plant in self.plants:
                    if random.random()<self.plants[plant]:
                        self.map.place(plant,i,j)
                        break



'''GAME'''
class Game(object):
    def __init__(self):
        self.init_game()
        #self.console.run()

    def init_game(self):
        self.world = World()
        self.x_w_cord = self.world.size//2
        self.y_w_cord = self.world.size//2
        #self.map = Map((MSIZE, MSIZE))
        self.create_map()
        self.inp = InputHandler(False)
        self.init_player()
        self.console = Console(self.world.map, self.inp, LSIZE)

    def init_player(self):
        self.player = Player()
        self.world.map.place(self.player,self.x_w_cord,self.y_w_cord)
        self.inp.callbacks[KEY_DOWN]  = lambda _: self.move( [ 0,  1] )
        self.inp.callbacks[KEY_LEFT]  = lambda _: self.move( [-1,  0] )
        self.inp.callbacks[KEY_UP]    = lambda _: self.move( [ 0, -1] )
        self.inp.callbacks[KEY_RIGHT] = lambda _: self.move( [ 1,  0] )

        #self.inp.callbacks[G] = {ord('g'): self.get_obj()}
        self.inp.callbacks[ord('g')] = lambda _: self.get_obj()


    def create_map(self):
        self.world.map.prng = ((self.x_w_cord-MXSIZE//2,self.x_w_cord+MXSIZE//2),\
                         (self.y_w_cord-MYSIZE//2,self.y_w_cord+MYSIZE//2))


    def move(self,vector):
        self.world.map.remove(self.player,self.x_w_cord,self.y_w_cord)
        if WSIZE-MXSIZE//2 > self.x_w_cord+vector[0] > MXSIZE//2 \
            and WSIZE-MYSIZE//2 > self.y_w_cord+vector[1] > MYSIZE//2 :
            self.x_w_cord += vector[0]
            self.y_w_cord += vector[1]
        self.create_map()
        self.world.map.place(self.player,self.x_w_cord,self.y_w_cord)

    def get_obj(self):
        x, y = self.x_w_cord, self.y_w_cord
        obj = self.world.map[x, y][-2]
        if obj.pickable:
            self.world.map.remove(obj, x, y)
            self.world.map.console.logwrite("Got " + obj.descr())
        else:
            self.world.map.console.logwrite(obj.descr()+" isn't pickable!")




'''FUNCTIONS'''
def get_curses_key_const():
    #Get all key constants from curses
    do = globals()
    dc = curses.__dict__
    for symbol, value in dc.items():
        if symbol.startswith('KEY_'):
            do[symbol] = value
    del do, dc

def nothing(*args, **kwargs):
    """Takes a arbitrary amount of arguments and return None"""
    pass

def list_dev(choices,val):
    prob_l = []
    prob_int = 1/len(choices)
    s = 0
    for el in choices:
        s+=prob_int
        prob_l.append(s)
    n = 0
    for i in prob_l:
        if val <= i:
            return choices[n]
        n+=1

if __name__ == '__main__':

    get_curses_key_const()
    g1 = Game()



