from world import *

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

    def draw(self, stdscr, clrs):
        self.create_map()
        self.world.map.print(stdscr, clrs)
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
        return None

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


