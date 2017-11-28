import random
from objects import *
from map import *
from generators import *
import worldgen

class World(object):
    def __init__(self, WSIZE, MXSIZE, MYSIZE):
        self.size = WSIZE
        self.mxsize = MXSIZE
        self.mysize = MYSIZE
        self.init_world_obj()
        self.create_world(WSIZE,MXSIZE,MYSIZE)
        self.create_patterns(WSIZE,MXSIZE,MYSIZE)
        #self.create_plants(WSIZE,MXSIZE,MYSIZE)
        #self.create_objs(WSIZE,MXSIZE,MYSIZE)

    def init_world_obj(self):
        self.plants = {
                        Tree():0.1,
                        BoldTree():0.01,
                        Bush():0.05,
                        Grass():0.03
                      }
        self.objects = {
                          Stone():0.02,
                          Mushroom():0.003,
                          Stick():0.001
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
                                               'green',\
                                               'yellow',\
                                               'black')),'black')
                    obj = Ground(rndclr)
                self.map.place(obj,i,j)
        #st = Stick()
        #self.map.place(st,WSIZE//2+3,WSIZE//2+3)

    #def create_plants(self,WSIZE,MXSIZE,MYSIZE):
        #for i in range(1,WSIZE-2):
            #for j in range(1,WSIZE-2):
                #for plant in self.plants:
                    #if random.random()<self.plants[plant]:
                        #self.map.place(plant,i,j)
                        #break
    
    def create_patterns(self,WSIZE,MXSIZE,MYSIZE):
        x0, y0 = WSIZE//2, WSIZE//2
        #A = new_array(WSIZE,WSIZE)
        #pattern = elips(A, x0, y0, 5, 20)
        #for i in range(1,WSIZE-2):
            #for j in range(1,WSIZE-2):
                #if pattern[i][j] == "x":
                    #self.map.place(Tree(),i,j)
        #B = new_array(WSIZE,WSIZE)
        #pattern2 = sinus(B, x0, y0, 20)
        #for i in range(1,WSIZE-2):
            #for j in range(1,WSIZE-2):
                #if pattern2[i][j] == "x":
                    #self.map.place(Bush(),i,j)
        #C = new_array(WSIZE,WSIZE)
        #pattern3 = romb(C, x0, y0+20, 10)
        #for i in range(1,WSIZE-2):
            #for j in range(1,WSIZE-2):
                #if pattern3[i][j] == "x":
                    #self.map.place(Grass(),i,j)
        #a = random.randint(0,100)
        #b = random.randint(0,100)
        #D = new_array(WSIZE+a,WSIZE+b)
        #pattern4 = fract(D, WSIZE+a, WSIZE+b)
        #for i in range(1,WSIZE-2):
            #for j in range(1,WSIZE-2):
                #if pattern4[i][j] == "x":
                    #self.map.place(Tree(),i,j)
        #p1 = Fractal(random.randint(WSIZE//2,WSIZE),random.randint(WSIZE//2,WSIZE))
        #for i in range(1,WSIZE-2):
            #for j in range(1,WSIZE-2):
                #try:
                    #if p1.array[j][i] == "x":
                        #self.map.place(Tree(),i,j)
                #except IndexError:
                    #pass
        w1 = worldgen.World(WSIZE)
        seq = [Grass(), Bush(), Tree(), BoldTree()]
        for i in range(1,WSIZE-2):
            for j in range(1,WSIZE-2):
                try:
                    if w1[i][j] == 1:
                        choice = worldgen.choice_distr(seq)
                        self.map.place(choice,i,j)
                except IndexError:
                    pass
                        
        
    
    def create_plants(self,WSIZE,MXSIZE,MYSIZE):
        for i in range(1,WSIZE-2):
            for j in range(1,WSIZE-2):
                for plant in self.plants:
                    if random.random()<self.plants[plant]:
                        self.map.place(plant,i,j)
                        break
                dice = random.random()
                N = find_min_less(dice, self.objects.values())
                if N:
                    obj=list(self.objects.keys())[list(self.objects.values()).index(N)]
                    self.map.place(obj,i,j)
                        
    
    
    
        
    
    def create_objs(self,WSIZE,MXSIZE,MYSIZE):
        for i in range(1,WSIZE-2):
            for j in range(1,WSIZE-2):
                if len(self.map[i, j]) <= 1:
                    dice = random.random()
                    
                    N = find_min_less(dice, self.objects.values())
                    if N:
                        obj=list(self.objects.keys())[list(self.objects.values()).index(N)]
                        self.map.place(obj,i,j)
                            
                    #for obj in self.objects:
                        #if random.random()<self.objects[obj]:
                            #self.map.place(obj,i,j)
                            #break

def find_min_less(d, xs):
    if [i for i in xs if i >= d] != []:
        return min([i for i in xs if i >= d])
