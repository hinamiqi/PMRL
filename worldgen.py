import numpy as np
import random as r
import matplotlib.pyplot as plt
import numpy as np
from generators import *


class World(list):
    def __init__(self, size):
        self.x, self.y = size, size
        self.gen_empty()
        self.gen_areas()
        self.gen_plants()
        self.gen_objects()
    
    def gen_empty(self):
        self.midx = self.x//2-1
        self.midy = self.y//2-1
        for i in range(self.x):
            self.append([])
            for j in range(self.y):
                val = distance(i, j, self.midx, self.midy)
                if val%2 != 0:
                    self[i].append(1)
                else:
                    self[i].append(0)
                
    def gen_areas(self):
        pass

            
    def gen_plants(self):
        
        pass
    def gen_objects(self):
        pass
    
    def get_value(self, x, y):
        return self[x][y]
    def set_value(self, x, y, val):
        self[x][y] = val

def choice_distr(seq): #random choice from seq by distribution
    i = 1/len(seq)
    #print(i)
    res = int(r.betavariate(1,3)/i)
    #print(res)
    return seq[res]

def distance(x1, y1, x2, y2):
    xdist = abs(x1 - x2)
    ydist = abs(y1 - y2)
    dist = max(xdist, ydist)
    return dist

#w1 = World(50)
#for line in w1:
    #print(line)

#seq = [, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
#seq = ('ground','stone','gem', 'stick')
#x = np.array([i for i in range(len(seq))])
#xtic = seq
#y = [0 for i in range(len(seq))]
#for i in range(1000):
    #res = choice_distr(seq)
    #y[res] += 1
    
    ##print(y)

#for el in seq:
    #print(el,": ", y[seq.index(el)])

##print(choice_distr([1,2,3]))

#plt.xticks(x, xtic)
#plt.plot(x, y)
#plt.show()
##fig, ax = plt.subplots()


    
    
