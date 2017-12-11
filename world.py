import random as r
import numpy as np

from objects import *
from map import *
from generators import *


class WorldMap(list):
    def __init__(self, size):
        self.size = size
        self.mins = 5
        self.maxs = self.size //10
        self.create_array()
        self.create_quads()
        self.generate_quads()
        
        #self = [[[[0] for j in range(self.size) ]] for i in range(self.size)]
        for i in range(self.size):
            self.append([[1] for j in range(self.size)])
        #for i in range(self.size):
            #self.append([])
            #for j in range(self.size):
                #self[i].append([0])
                #if i == 0 or i == self.size-1 or j == 0 or j == self.size-1:
                    #self[i].append([1])
 
                #else:
                 #   self[i].append([0])
                
    def create_array(self):
        self.array = [[0 for i in range(self.size)] for j in range(self.size)]
                
    def create_quads(self):
        verts = stair_ord(self.size-1)
        mins = self.mins
        maxs = self.maxs
        n = 1
        for v in verts:
            i = v[0]
            j = v[1]
            if self.array[i][j] == 0:
                #if self.array[i+mins][j] or self.array[i][j+mins] != 0:
                    
                dx = r.randint(mins, maxs)
                dy = r.randint(mins, maxs)
                x = 1
                y = 0
                
                while i+y<self.size and y<dy:
                    if self.array[i+y][j] == 0:
                        self.array[i+y][j] = n
                    else:
                        break
                    y += 1
                while j+x<self.size and x<dx:
                    if all([self.array[I][j+x] == 0 for I in range(i,i+y)]):
                        for I in range(i,i+y):
                            self.array[I][j+x] = n
                    else:
                        break
                    x += 1
                n += 1
        self.n = n
        
    def generate_quads(self):
        self.quads = []
        quads = [[] for i in range(self.n-1)]
        

        for i in range(self.size):
            for j in range(self.size):
                quads[self.array[i][j]-1].append((i, j))
        
        for el in quads:
            start = el[0]
            end = el[-1]
            xs = start[0]
            ys = start[1]
            xe = end[0]
            ye = end[1]
            quad = (xs, ys, xe+1, ye+1)
            self.quads.append(quad)
    
    def fill_quads(self, N):
        for quad in self.quads:
            choice = r.randint(1, N-1)
            xs = quad[0]
            xe = quad[2]
            ys = quad[1]
            ye = quad[3]
            #print(self)
            for i in range(ys, ye):
                for j in range(xs, xe):
                    if i == 0 or i == self.size-1 or j == 0 or j == self.size-1:
                        self[i][j].append(0)
                    else:
                        self[i][j].append(choice)
    
    def fill_quads2(self, N):
        for quad in self.quads:
            xs = quad[0]
            xe = quad[2]
            ys = quad[1]
            ye = quad[3]

            val0 = r.randint(1,7)
            val1 = r.randint(1,7)
            func = r.choice(('forest','quads','random','empty','circles'))
            self.quad_filling(xs, ys, xe, ye, val0, val1, func)
            
    
    def quad_filling(self, xs, ys, xe, ye, val0, val1, func):
        x = xe-xs
        y = ye-ys
        gen = Gen(func, x, y, val0, val1)
        m = 0
        for i in range(ys,ye):
            n = 0
            for j in range(xs,xe):
                if i == 0 or i == self.size-1 or j == 0 or j == self.size-1:
                    self[i][j].append(0)
                else:
                    try:

                        self[i][j].append(gen.array[i-ys][j-xs])
                    except IndexError:
                        pass
                n+=1
            m+=1
    
    
    def fill(self, N):
        for i in range(self.size):
            for j in range(self.size):
                if i == 0 or i == self.size-1 or j == 0 or j == self.size-1:
                    self[i][j].append(0)
                else:
                    self[i][j].append(r.randint(1,N-1))
    
    def make_border(self):
        size = self.size
        for i in range(self.size):
            self[i][0].append(0)
            self[i][size-1].append(0)
        for j in range(self.size):
            self[0][j].append(0)
            self[size-1][j].append(0)
    
    #def make_rnd_trees(self):
        
        #S = self.size - 1
        #for i in range(self.size):
            #for j in range(self.size):
                #if i == 0 or i == self.size-1 or j == 0 or j == self.size-1:
                    #self[i][j].append(1)
                #else:
                    #self[i][j].append(r.choice((2,4,5)))
    
    def upper(self, x, y):
        try:
            upper = self[x][y][-1]
        except IndexError:
            return None
        else:
            return upper
    
    def cell(self, x, y):
        try:
            cell = self[x][y]
        except IndexError:
            return []
        else:
            return cell
    
    
    
    
        

class World(object):
    def __init__(self, PAR):
        self.size = PAR[1]
        
        #self.mxsize = PAR[3]//2 
        #self.mysize = PAR[4]-5
        self.mxsize = 30
        self.mysize = 20
        self.init_world_obj()
        self.create_world()
        self.msg = ""
        self.player = Player()
        
        self.set_world_cord()
        
        self.map_update()

    def init_world_obj(self):
        #self.objects = [ Ground(),
                        #Rock(),
                        #Tree(),
                        #BoldTree(),
                        #Bush(),
                        #Grass()
                      #]
        #chlist = [Ground(), ]
        #self.objects = [Rock(), Ground()]
        
        #for i in range(r.randint(1,10)):
            #obj = Elem()
            #obj.str = r.choice(['&','"',"'",'|'])
            #obj.clr = r.choice([('green','black'),('yellow','black'),('red','black')])
            
            #self.objects.append(obj)
        #self.cores = [Rock(), Ground(), Ground(('yellow','black')), Ground(('black','black'))]
        #self.plants = [Grass(), Bush(), Tree(), BoldTree()]
        #self.objects = [Stone(), Stick(), Mushroom()]
        #self.objects = [Rock(), Ground(), Ground(('yellow','black')), Ground(('black','black')),\
        #                Grass(), Bush(), Tree(), BoldTree(),\
        #                Stone(), Stick(), Mushroom()]
        loader = ObjLoader()
        loader.load_file()
        self.objects = loader.objects
        #grn = Elem()

    def create_world(self):
        self.world_map = WorldMap(self.size)
        #self.world_map.fill(len(self.objects))
        #self.world_map.fill_quads(len(self.objects))
        self.world_map.fill_quads2(len(self.objects))
        #self.world_map.make_border()
        #self.world_map.make_rnd_trees()
    
    def set_world_cord(self, x=None, y=None):
        if x == None:
            x = self.size//2
        if y == None:
            y = self.size//2
        self.x = x
        self.y = y
    
    def place(self, obj, x, y):
        self.world_map[x][y].append(self.objects.index(obj))
    
    def delete(self, x, y):
        #try:
            self.world_map[x][y].remove(self.world_map[x][y][-1])
        
            #except 
    
    def upper(self, x, y):
        return self.world_map.upper(x, y)
    
    def collision(self, x, y):
        result = self.map[x, y].penetrable()
        return result
    
    def print(self, stdscr, clrs):
        self.map.print(stdscr, clrs)
    
    def map_update(self):
        self.map = Map(self.mxsize, self.mysize)
        xstart = self.x - self.mxsize//2
        xend = self.x + self.mxsize//2
        ystart = self.y - self.mysize//2
        yend = self.y + self.mysize//2

        #self.msg = str(xstart) + " " + str(xend) + " " + str(ystart) + " " + str(yend)
        #self.msg = str(self.world_map.upper(self.x, self.y))
        i = 0
        for y in range(ystart, yend):
            j = 0
            for x in range(xstart, xend):
                #upper = self.world_map.upper(x, y)
                for obj in self.world_map.cell(x, y):
                    #if obj:
                    self.map.place(self.objects[obj], j, i)

                
                j += 1
            i += 1
        #self.map.place(self.objects[1], 3, 3)
        self.map.place(self.player, self.mxsize//2, self.mysize//2)
        self.msg = "Here " + str(self.objects[self.world_map.upper(self.x, self.y)].descr()) 
        #self.msg = str(x) + " " + str(y)
    
    

def find_min_less(d, xs):
    if [i for i in xs if i >= d] != []:
        return min([i for i in xs if i >= d])

def stair_ord(N):
    l1 = []
    l2 = []
    n = N
    for i in range(N+1):
        l1 += list(range(n,-1,-1))
        l2 += list(range(0,n+1,1))
        n -= 1
    m = 0
    l3 = []
    l4 = []
    for i in range(N):
        l3 += list(range(N,m,-1))
        l4 += list(range(m+1,N+1,1))
        m +=1
    l1.reverse()
    l2.reverse()
    l1 += l3
    l2 += l4
    return list(zip(l1,l2))

#w = WorldMap(10)
#print(w.quads)
#w.fill_quads(3)
