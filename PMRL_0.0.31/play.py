from tools import *
from objects import *

import random

MAP_MARG = 1

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
        #self.prng = ((0,self.x),(0,self.y))
        self.prng = ((self.x//2-MXSIZE,self.x//2+MXSIZE),(self.y//2-MYSIZE,self.y//2+MYSIZE))

    #__repr__ = object.__repr__
    #__str__ = object.__str__

    def print(self, stdscr):
        prng = self.prng
        m = MAP_MARG
        for j in range(prng[1][0],prng[1][1]):
            n = MAP_MARG
            for i in range(prng[0][0],prng[0][1]):
                obj = self[i, j]
                #cc = obj.color()
                stdscr.addstr(m, n, str(obj))
                n+=1
            m+=1
        x = prng[0][1]-self.mx//2
        y = prng[1][1]-self.my//2
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

class World(object):
    def __init__(self, WSIZE, MXSIZE, MYSIZE):
        self.size = WSIZE

        self.mxsize = MXSIZE
        self.mysize = MYSIZE
        self.init_world_obj()
        self.create_world(WSIZE,MXSIZE,MYSIZE)
        self.create_plants(WSIZE,MXSIZE,MYSIZE)
        self.create_objs(WSIZE,MXSIZE,MYSIZE)

    def init_world_obj(self):
        self.plants = {
                        Tree():0.1,
                        Bush():0.05,
                      }
        self.objects = {
                          Stone():0.005,
                          Mushroom():0.001
                        }


    def create_world(self,WSIZE,MXSIZE,MYSIZE):
        self.map = Map(WSIZE,MXSIZE,MYSIZE)
        for i in range(self.size):
            for j in range(self.size):
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

    def create_plants(self,WSIZE,MXSIZE,MYSIZE):
        for i in range(MXSIZE//2,WSIZE-MXSIZE//2):
            for j in range(MYSIZE//2,WSIZE-MYSIZE//2):
                for plant in self.plants:
                    if random.random()<self.plants[plant]:
                        self.map.place(plant,i,j)
                        break

    def create_objs(self,WSIZE,MXSIZE,MYSIZE):
        for i in range(MXSIZE//2,WSIZE-MXSIZE//2):
            for j in range(MYSIZE//2,WSIZE-MYSIZE//2):
                for obj in self.objects:
                    if random.random()<self.objects[obj]:
                        self.map.place(obj,i,j)
                        #break


class Play():
    def __init__(self, WSIZE, MXSIZE, MYSIZE, MAP_MARG, MENU):
        self.menu = MENU
        self.world = World(WSIZE, MXSIZE, MYSIZE)
        self.mx, self.my = MXSIZE, MYSIZE
        self.x_w_cord = self.world.size//2
        self.y_w_cord = self.world.size//2
        self.player = Player()
        self.player.bp = ["Cauldron"]
        self.world.map.place(self.player,self.x_w_cord,self.y_w_cord)
        self.logtext = ""
    
    def draw(self,stdscr):
        self.create_map()
        self.world.map.print(stdscr)
        stdscr.addstr(0, self.my, self.logtext)
    
    def create_map(self):
        self.world.map.prng = ((self.x_w_cord-self.mx//2,self.x_w_cord+self.mx//2),\
                         (self.y_w_cord-self.my//2,self.y_w_cord+self.my//2))
    
    def inp_handler(self, key):
        self.logtext = ""
        if key == 258:
            self.move( [ 0,  1] )
        elif key == 260:
            self.move( [-1,  0] )
        elif key == 259:
            self.move( [ 0, -1] )
        elif key == 261:
            self.move( [ 1,  0] )
        elif key == ord('g'):
            self.get_obj()
    
    def move(self,vector):
        nx = self.x_w_cord + vector[0]
        ny = self.y_w_cord + vector[1]
        f = self.world.map[nx ,ny].penetrable()
        if f:
            self.world.map.remove(self.player,self.x_w_cord,self.y_w_cord)
            self.x_w_cord += vector[0]
            self.y_w_cord += vector[1]
            self.create_map()
            self.world.map.place(self.player,self.x_w_cord,self.y_w_cord)
    
    def get_obj(self):
        x, y = self.x_w_cord, self.y_w_cord
        obj = self.world.map[x, y][-2]
        if obj.pickable:
            self.world.map.remove(obj, x, y)
            self.player.bp.append(obj)
            #self.logwrite("Got "+obj.descr())
            self.logtext = "Got "+obj.descr()
    
    def logwrite(self, text):
        self.logtext = text
        

    
    def quiting(self):
        return self.menu
        
        
