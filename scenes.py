from world import *
from collections import Counter
from curses import A_BOLD, A_DIM

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
        stdscr.attron(A_BOLD)
        stdscr.addstr(height//2-2, self.startx_title, self.title, clrs['r','w'])
        stdscr.attroff(A_BOLD)
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
        stdscr.attron(A_BOLD)
        stdscr.addstr(MAP_MARG, MAP_MARG, self.title, clrs['b','w'])
        stdscr.attroff(A_BOLD)
        i = MAP_MARG + 1
        for line in self.data:
            stdscr.addstr(i, 2, line)
            i+=1

    def inp_handler(self, key):
        return None

    def quiting(self):
        return self.prev_scene

class Inventory():
    def __init__(self, items):
        self.title = "Inventory:"
        #self.prev_scene = prev_secene
        self.items = items
        self.actions = ""
        
    
    def update(self, prev_secene, add=None):
        self.prev_scene = prev_secene
        self.pos = 0
        self.calc_items()
        if add:
            self.actions = "[A]dd what?"
        else:
            self.actions = ""
    
    def delete_item(self, item):
        self.items.remove(item)
    def add_item(self, item):
        self.items.append(item)
    
    def calc_items(self):
        self.item_list = []
        cntd = Counter(self.items)
        for item in cntd:
            self.item_list.append((item,cntd[item]))
    
    def draw(self,stdscr, clrs):
        stdscr.attron(A_BOLD)
        stdscr.addstr(MAP_MARG, MAP_MARG, self.title)
        stdscr.attroff(A_BOLD)
        i = MAP_MARG + 1
        #item_list = []
        #for item in self.items:
        #    item_list.append(item.descr())
        
        n = 0
        if self.item_list == []:
            stdscr.addstr(i, 2, "Empty", clrs['w','b'] | A_DIM)
        else:
            for item in self.item_list:
                if n == self.pos:
                    color =  clrs['b','w']
                else:
                    color =  clrs['w','b']
                string = item[0].descr()+" "+"x"+str(item[1])
                stdscr.addstr(i, 2, string, color)
                i+=1
                n+=1
                if i >= 10 + MAP_MARG + 1: break
            stdscr.addstr(12, 2, self.item_list[self.pos][0].fdescr())
        stdscr.addstr(14, 2, self.actions)
        #for item in self.items:
        #    stdscr.addstr(i, 2, item.descr())
        #    i+=1

    def inp_handler(self, key):
        if key == 258:
            self.pos +=1
            if self.pos >= len(self.item_list):
                self.pos = 0
        elif key == 259:
            self.pos -=1
            if self.pos < 0:
                self.pos = len(self.item_list)-1
        elif key == ord('a') and self.actions != "" and len(self.items)>0:
            item = self.item_list[self.pos][0]
            self.items.remove(item)
            return self.quiting(item)
        else:
            return None

    def quiting(self, item=None):
        if item:
            self.prev_scene.add_item(item)
        return self.prev_scene

class PotionMaker():
    def __init__(self, game, MXSIZE, MYSIZE):
        self.mx, self.my = MXSIZE, MYSIZE
        self.title = "Making potion..."
        self.game = game
        #self.items = items
        self.fire = False
        self.ingr = []
    
    def add_item(self, item):
        self.ingr.append(item)
    
    def make_pot(self):
        return Potion(self.ingr)
        
    
    def draw(self,stdscr, clrs):
        stdscr.attron(A_BOLD)
        stdscr.addstr(MAP_MARG, MAP_MARG, self.title)
        stdscr.attroff(A_BOLD)
        s = MAP_MARG+1
        stdscr.addstr(s+1, MAP_MARG, "[A]dd ingridient or [M]ake the potion?")
        N = 1
        stdscr.addstr(s+3, MAP_MARG, "Turn: "+str(N))
        string = ""
        for obj in self.ingr:
            string = string + " " + obj.descr()
        stdscr.addstr(s+5, MAP_MARG, "Currently in cauldron:  "+"Water"+string)
        stdscr.addstr(s+7, MAP_MARG, "Current flame:  "+"None")
        
        stdscr.addstr(self.my, MAP_MARG, "Pot looks "+"just like water.")
    
    def inp_handler(self, key):
        if key == ord('a'):
            self.game.inv.update(self, add=True)
            return self.game.inv
        elif key == ord('m'):
            pot = self.make_pot()
            self.game.inv.add_item(pot)
            return self.quiting()
        else:
            return None

    def quiting(self):
        return self.game

class Play():
    def __init__(self, WSIZE, MXSIZE, MYSIZE, MAP_MARG, MENU):
        self.menu = MENU
        self.world = World(WSIZE, MXSIZE, MYSIZE)
        self.mx, self.my = MXSIZE, MYSIZE
        self.x_w_cord = self.world.size//2
        self.y_w_cord = self.world.size//2
        self.player = Player()
        obj = Cauldron()
        #self.player.bp = [obj]
        self.inv = Inventory([])
        self.world.map.place(self.player,self.x_w_cord,self.y_w_cord)
        self.log = ['','','']
        self.paneltext = ""

    def draw(self, stdscr, clrs):
        self.update_map()
        
        self.world.map.print(stdscr, clrs)
        stdscr.attron(A_BOLD)
        stdscr.addstr(self.my+1, self.mx+1, self.paneltext)
        stdscr.attroff(A_BOLD)
        self.log_draw(stdscr)

    def update_map(self):
        self.world.map.prng = ((self.x_w_cord-self.mx//2,self.x_w_cord+self.mx//2),\
                         (self.y_w_cord-self.my//2,self.y_w_cord+self.my//2))
        
        self.paneltext = "Here "+self.obj_here().descr()
        
    
    def obj_here(self, x=None,y=None):
        if x == None and y == None:
            x,y = self.x_w_cord,self.y_w_cord
        obj = self.world.map[x, y][-2]
        return obj
    
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
            self.inv.update(self, add=None)
            return self.inv
        elif key == ord('m'):
            return PotionMaker(self, self.mx, self.my)
        return None
        
        

    def move(self,vector):
        nx = self.x_w_cord + vector[0]
        ny = self.y_w_cord + vector[1]
        f = self.world.map[nx ,ny].penetrable()
        if f:
            self.world.map.remove(self.player,self.x_w_cord,self.y_w_cord)
            self.x_w_cord += vector[0]
            self.y_w_cord += vector[1]
            self.world.map.place(self.player,self.x_w_cord,self.y_w_cord)
            self.update_map()
            
            

    def get_obj(self):
        x, y = self.x_w_cord, self.y_w_cord
        obj = self.obj_here()
        if obj.pickable:
            self.world.map.remove(obj, x, y)
            self.inv.add_item(obj)
            #self.player.bp.append(obj)
            #self.logwrite("Got "+obj.descr())
            #self.logtext = "Got "+obj.descr()
            self.logwrite("Got "+obj.descr())
            

    def logwrite(self, text):
        self.log.append(text)
    
    def log_draw(self, stdscr):
        stdscr.addstr(self.my+2, 1, self.log[-3])
        stdscr.addstr(self.my+3, 1, self.log[-2])
        stdscr.addstr(self.my+4, 1, self.log[-1])
        
    


    def quiting(self):
        return self.menu