import math

def new_array(x,y):
    return [["." for i in range(x+1)] for i in range(y+1)]

def print_array(array):
    for line in array:
        st = ""
        for i in line:
            symb = str(i)
            st += symb
        print(st)

def create_quad(array, x1, y1, x2, y2):
    for i in range(x1, x2):
        for j in range(y1, y2):
            array[j][i] = "x"
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

def circle(array, x0, y0, r):
    for x in range(-r,r):
        y1 = round(math.sqrt((r**2 - (x)**2)))
        for y in range(y0-y1,y0+y1):
            array[y][x+x0]="x"
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

def fract(array, XS, YS):
    
    pairs = []
    x0 = 0
    y0 = 0
    x,y = x0, y0
    dx = 1
    dy = 1
    k = 1
    pairs.append([x,y])
    flag = True
    while True:
        x = x + dx
        y = y + dy
        if x == XS or x == 0:
            dx = dx*(-1)
        if y == YS or y == 0:
            dy = dy*(-1)
        #print(dx, dy)
        
        
        k = k*(-1)
        if k == 1:
            pairs.append([x,y])
            #print(x,' ',y)
        #pairs.append([x,y])
        
        if (x==XS and y==YS) or (x==0 and y==0):
            break
            
    #return pairs
    for pair in pairs:
        array[pair[1]][pair[0]] = "x"
    
    return array
        
        
        
    
    

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
