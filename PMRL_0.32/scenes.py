from world import *
from collections import Counter

#class Scene():
#    def __init__

class Menu():
    def __init__(self, VERSION, WSIZE, MXSIZE, MYSIZE):
        self.par = (WSIZE, MXSIZE, MYSIZE)
        self.title = "POTION MASTER RL"
        self.subtitle = "v" + VERSION
        self.info = "Roguelike about making potions and stuff."
        self.bar = "[C]ontinue   [H]elp   [Q]uit"
        #self.game = None

    def draw(self, stdscr, clrs):
        height, width = self.par[2], self.par[1]*2
        self.startx_title = int((width // 2) - (len(self.title) // 2) - len(self.title) % 2)
        self.startx_subtitle = int((width // 2) - (len(self.subtitle) // 2) - len(self.subtitle) % 2)
        self.startx_info = int((width // 2) - (len(self.info) // 2) - len(self.title) % 2)
        self.startx_bar = int((width // 2) - (len(self.bar) // 2) - len(self.title) % 2)
        #stdscr.attron(curses.A_BOLD)
        stdscr.addstr(height//2-2, self.startx_title, self.title, clrs['r','w'])
        #stdscr.attroff(curses.A_BOLD)
        stdscr.addstr(height//2-1, self.startx_subtitle, self.subtitle)
        stdscr.addstr(height//2, self.startx_info, self.info)
        stdscr.addstr(height-1, self.startx_bar, self.bar)

    def inp_handler(self, key):
        if key == ord('c'):
                return Play(*self.par, 1, self)
        else:
            return None
        #pass

    def quiting(self):
        return None

class Help():
    def __init__(self, prev_secene):
        self.prev_scene = prev_secene
        self.title = "Help page (q to exit):"
        with open('help.txt', 'r') as f:
            self.data = f.readlines()



    def draw(self,stdscr, clrs):
        #stdscr.attron(curses.A_BOLD)
        stdscr.addstr(MAP_MARG, MAP_MARG, self.title, clrs['b','w'])
        #stdscr.attroff(curses.A_BOLD)
        i = MAP_MARG + 1
        for line in self.data:
            stdscr.addstr(i, 2, line)
            i+=1

    def inp_handler(self, key):
        return None

    def quiting(self):
        return self.prev_scene

class Inventory():
    def __init__(self, prev_secene, items):
        self.title = "Inventory:"
        self.prev_scene = prev_secene
        self.items = items

    def draw(self,stdscr, clrs):
        #stdscr.attron(curses.A_BOLD)
        stdscr.addstr(MAP_MARG, MAP_MARG, self.title, clrs['b','w'])
        #stdscr.attroff(curses.A_BOLD)
        i = MAP_MARG + 1
        item_list = []
        for item in self.items:
            item_list.append(item.descr())
        cntd = Counter(item_list)
        print(cntd)
        for item in cntd:
            string = item+" "+"x"+str(cntd[item])
            stdscr.addstr(i, 2, string)
            i+=1
        #for item in self.items:
        #    stdscr.addstr(i, 2, item.descr())
        #    i+=1

    def inp_handler(self, key):
        return None

    def quiting(self):
        return self.prev_scene

class Play():
    def __init__(self, WSIZE, MXSIZE, MYSIZE, MAP_MARG, MENU):
        self.menu = MENU
        self.world = World(WSIZE, MXSIZE, MYSIZE)
        self.mx, self.my = MXSIZE, MYSIZE
        self.x_w_cord = self.world.size//2
        self.y_w_cord = self.world.size//2
        self.player = Player()
        obj = Cauldron()
        self.player.bp = [obj]
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

        if key == ord('i'):
            return Inventory(self, self.player.bp)
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
