import math
import random as r

"""GENERATORS"""

class Gen():
    def __init__(self, func, x, y, val0, val1):
        self.x = x
        self.y = y
        self.val0 = val0
        self.val1 = val1
        if func == 'forest':
            self.forest()
        elif func == 'quads':
            self.quads()
        elif func == 'random':
            self.rand_fill()
        elif func == 'circles':
            self.circles()
        else:
            self.empty()
        
    def forest(self):
        f1 = Fractal(self.x,self.y,self.val0,self.val1)
        self.array = f1.array


    def quads(self):
        array = new_array(self.x, self.y, self.val0)
        for i in range(r.randint(1,max(self.x,self.y))):
            sx = r.randint(0,self.x-1)
            sy = r.randint(0,self.y-1)
            ex = r.randint(sx,self.x)
            ey = r.randint(sy,self.y)
            array = quad(array, sx, sy, ex, ey, self.val1)
        self.array = array

    def circles(self):
        array = new_array(self.x, self.y, self.val0)
        for i in range(r.randint(1,max(self.x,self.y))):
            R = r.randint(0,min(self.x//2,self.y//2))
            x = r.randint(R,self.x-R)
            y = r.randint(R,self.y-R)
          
            array = circle(array, x, y, R, self.val1)
        self.array = array
        
    
    def rand_fill(self):
        array = [[r.choice((self.val0,self.val1))] for i in range(self.y)]
        self.array = array
    
    def empty(self):
        array = new_array(self.x,self.y,self.val0)
        for i in range(r.randint(1,max(self.x,self.y))):
            sx = r.randint(0,self.x-1)
            sy = r.randint(0,self.y-1)
            array[sy][sx] = self.val1
        self.array = array

        
        

def new_array(x,y, val):
    return [[val for i in range(x+1)] for i in range(y+1)]

def print_array(array):
    for line in array:
        st = ""
        for i in line:
            symb = str(i)
            st += symb
        print(st)

def quad(array, x1, y1, x2, y2, val):
    for i in range(x1, x2):
        for j in range(y1, y2):
            array[j][i] = val
    return array

def romb(array, x0, y0, r):
    for i in range(0,r,1):
        x1 = x0 + i
        x2 = x0 - i
        for y in range(y0-(r-i)+1,y0+(r-i)):
            #print(y, " ", x)
            array[y][x1] = "x"
            array[y][x2] = "x"
        #x1 = X
        #x2 = X
        #y = [y for y in range(Y-(N-i),Y+(N-i))]

    
    return array

def circle(array, x0, y0, r, v1):
    for x in range(-r,r):
        y1 = round(math.sqrt((r**2 - (x)**2)))
        for y in range(y0-y1,y0+y1):
            array[y][x+x0]=v1
    return array

def elips(array, x0, y0, a, b):
    for x in range(-a,a):
        #y1 = round(math.sqrt((b**2 - (x)**2)))
        y1 = round(math.sqrt(b**2 - ((x**2)*(b**2))/a**2))
        for y in range(y0-y1,y0+y1):
            print(y+y0,',',x+x0)
            array[y][x+x0]="x"
    return array

def sinus(array, x0, y0, r):
    for x in range(-r,r):
        y1 = round(r/2*math.sin(x*(math.pi/r)))
        for y in range(y0-y1,y0+y1):
            array[y][x+x0]="x"
    return array

        
class Fractal(object):
    def __init__(self, X, Y, v0, v1):
        self.step = r.randint(1,7)
        self.x = X
        self.y = Y
        self.plot()
        self.build_array(v0, v1)
    #def resize(self):
        #self.w = self.win.width
        #self.h = self.win.height
        #print(self.w, self.h)
        #self.vertex_list = self.plot()
    
    def plot(self):
        step = self.step
        XS = self.x
        YS = self.y
        pairs = []
        dx = step
        dy = step
        x  = 0
        y  = 0
        k  = 1
        pairs.append(x)
        pairs.append(y)
        pairs.append(x+dx)
        pairs.append(y+dy)
        i = 0
        while True:
            x = x + dx
            y = y + dy
            if (x==XS and y==YS) or (x==0 and y==0):
                break
            if (x==XS and y==YS) or (x==0 and y==0):
                break
            if x >= XS or x <= 0:
                dx = dx*(-1)
            if y >= YS or y <= 0:
                dy = dy*(-1)
            k = k*(-1)
            if k == 1:
                pairs.append(x)
                pairs.append(y)
                pairs.append(x+dx)
                pairs.append(y+dy)
            i += 1

        #return pairs
        self.pairs = pairs
        
    
    def build_array(self, v0, v1):
        #A = new_array(self.x, self.y)
        A = [[v0 for i in range(self.x+1)] for i in range(self.y+1)]
        #print("pairs: ", self.pairs)
        k = 1
        for i in range(0, len(self.pairs), 4):
            startx = self.pairs[i]
            starty = self.pairs[i+1]
            endx   = self.pairs[i+2]
            endy   = self.pairs[i+3]
            dx = (endx-startx)//abs(endx-startx)
            dy = (endy-starty)//abs(endy-starty)
            #print("pair ", k, ":")
            #k += 1
            #print("start ", startx, " ", starty)
            #print("end ", endx, " ", endy)
            #m = [i for i in range(startx,endx,dx)]
            #n = [i for i in range(starty,endy,dy)]
            #print("m, n: ",m,n)
            #for i in range(len(m)):
             #A[n[i]][m[i]] = "x"
            x = startx
            y = starty
            while x != endx and y != endy:

                #print("x, y ", x," ", y)
                try:
                    A[y][x] = v1
                except IndexError:
                    pass
                x += dx
                y += dy
        self.array = A
        #print_array(A)
    
#f1 = Fractal(44,105)
# = new_array(20,20)

#print_array(create_quad(A, 1,1, 6,7))
#print_array(romb(A, 9, 9, 3))
#print_array(circle(A, 6, 5, 7))
#print_array(elips(A, 30, 40, 20, 15))
#print_array(sinus(A, 5, 6, 15))
#for i in range(3,22):
    #for j in range(3,22):
        #a, b = i, j
        #print('new size: ',i," ",j)
        #print_array(fract(new_array(a,b),a,b))

#val0 = r.choice((1,2,3))
#val1 = r.choice((4,5,6,7))
#func = r.choice(('forest','quads','random','empty'))
#gen = Gen(func, 10, 10, val0, val1)
#print_array(gen.array)
