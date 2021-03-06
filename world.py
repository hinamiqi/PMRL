import random
from objects import *
from map import *

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
                        BoldTree():0.01,
                        Bush():0.05,
                      }
        self.objects = {
                          Stone():0.002,
                          Mushroom():0.003,
                          Stick():0.0001
                        }


    def create_world(self,WSIZE,MXSIZE,MYSIZE):
        self.map = Map(WSIZE,MXSIZE,MYSIZE)
        for i in range(self.size):
            for j in range(self.size):
                #if i<=MXSIZE//2 or i>=WSIZE-MXSIZE//2 \
                #   or j<=MYSIZE//2 or j>=WSIZE-MYSIZE//2:
                if i == 0 or i == WSIZE-1 or j == 0 or j == WSIZE-1:
                    obj = Rock()
                else:
                    rndclr = (random.choice((\
                                               'g',\
                                               'y',\
                                               'b')),'b')
                    obj = Ground(rndclr)
                self.map.place(obj,i,j)
        #st = Stick()
        #self.map.place(st,WSIZE//2+3,WSIZE//2+3)

    def create_plants(self,WSIZE,MXSIZE,MYSIZE):
        for i in range(1,WSIZE-2):
            for j in range(1,WSIZE-2):
                for plant in self.plants:
                    if random.random()<self.plants[plant]:
                        self.map.place(plant,i,j)
                        break

    def create_objs(self,WSIZE,MXSIZE,MYSIZE):
        for i in range(1,WSIZE-2):
            for j in range(1,WSIZE-2):
                if len(self.map[i, j]) <= 1:
                    for obj in self.objects:
                        if random.random()<self.objects[obj]:
                            self.map.place(obj,i,j)
                            break

