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
                        Bush():0.05,
                      }
        self.objects = {
                          Stone():0.002,
                          Mushroom():0.003
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
                                               'g',\
                                               'y',\
                                               'w',\
                                               'r')),'b')
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

