from world import *
from collections import Counter
from curses import A_BOLD, A_DIM

#class Scene():
#    def __init__

class Menu():
    def __init__(self, PAR):
        self.par = PAR
        self.title = "POTION MASTER RL"
        self.subtitle = "v" + PAR[0]
        self.info = "Roguelike about making potions and stuff."
        self.bar = "[C]ontinue   [H]elp   [Q]uit"
        #self.game = None

    def draw(self, stdscr, clrs):
        height, width = self.par[4], self.par[3]
        self.startx_title = int((width // 2) - (len(self.title) // 2) - len(self.title) % 2)
        self.startx_subtitle = int((width // 2) - (len(self.subtitle) // 2) - len(self.subtitle) % 2)
        self.startx_info = int((width // 2) - (len(self.info) // 2) - len(self.title) % 2)
        self.startx_bar = int((width // 2) - (len(self.bar) // 2) - len(self.title) % 2)
        #stdscr.attron(A_BOLD)
        stdscr.addstr(height//2-2, self.startx_title, self.title, clrs['red','black'] | A_BOLD)
        #stdscr.attroff(A_BOLD)
        stdscr.addstr(height//2-1, self.startx_subtitle, self.subtitle)
        stdscr.addstr(height//2, self.startx_info, self.info)
        stdscr.addstr(height-1, self.startx_bar, self.bar)

    def inp_handler(self, key):
        if key == ord('c'):

                return Play(self.par, 1, self)
                
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
        stdscr.addstr(MAP_MARG, MAP_MARG, self.title, clrs['black','white'])
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
        self.m = ""
        self.actions = self.m
        
    def set_drop(self):
        self.actions = "[D]rop what?"
    
    def update(self, prev_scene, add=None):
        self.prev_scene = prev_scene
        self.pos = 0
        self.calc_items()
        if add:
            self.actions = "[A]dd what?"
        else:
            self.actions = self.m
    
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
            stdscr.addstr(i, 2, "Empty", clrs['white','black'] | A_DIM)
        else:
            for item in self.item_list:
                if n == self.pos:
                    color =  clrs['black','white']
                else:
                    color =  clrs['white','black']
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
        elif key == ord('a') and self.actions != self.m and len(self.items)>0:
            item = self.item_list[self.pos][0]
            self.items.remove(item)
            return self.quiting(item)
        elif key == ord('d') and self.actions == "[D]rop what?" and len(self.items)>0:
            item = self.item_list[self.pos][0]
            self.items.remove(item)
            self.prev_scene.logwrite("You drop "+item.fdescr())
            return self.quiting(item)
        else:
            return None

    def quiting(self, item=None):
        if item:
            self.prev_scene.return_item(item)
            
        return self.prev_scene

class PotionMaker():
    def __init__(self, game, MXSIZE, MYSIZE):
        self.mx, self.my = MXSIZE, MYSIZE
        self.title = "Making potion..."
        self.game = game
        #self.items = items
        self.fire = False
        self.ingr = []
    
    def return_item(self, item):
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
            pot = Potion(self.ingr)
            self.game.inv.add_item(pot)
            self.game.logwrite("Got "+pot.fdescr())
            
            return self.quiting()
        else:
            return None

    def quiting(self):
        return self.game

class Play():
    def __init__(self, PAR, MAP_MARG, MENU):
        WORLD_SIZE = PAR[1]
        XSIZE = PAR[3]
        YSIZE = PAR[4]
        self.menu = MENU
        self.world = World(PAR)
        self.mx, self.my = PAR[3]//2, PAR[4]-5
        #self.x_w_cord = self.world.size//2
        #self.y_w_cord = self.world.size//2
        #self.player = Player()
        #obj = Cauldron()
        #self.player.bp = [obj]
        self.inv = Inventory([])
        #self.world.map.place(self.player,self.x_w_cord,self.y_w_cord)
        self.log = ['','','']
        self.paneltext = ""
    
    
        
    
    def draw(self, stdscr, clrs):
        self.update_map()
        
        #self.world.map.print(stdscr, clrs)
        self.world.print(stdscr, clrs)
        stdscr.attron(A_BOLD)
        stdscr.addstr(self.my+1, self.mx+1, self.paneltext)
        stdscr.attroff(A_BOLD)
        self.log_draw(stdscr)

    def update_map(self):
        #self.world.map.prng = ((self.x_w_cord-self.mx//2,self.x_w_cord+self.mx//2),\
        #                 (self.y_w_cord-self.my//2,self.y_w_cord+self.my//2))
        self.world.map_update()
        #self.paneltext = "Here "+self.obj_here().descr()
        #self.paneltext = str(self.world.x) + " " + str(self.world.y)
        self.paneltext = self.world.msg
        
    
    def return_item(self, item):
        #self.world.map.place(item, self.x_w_cord, self.y_w_cord)
        self.world.place(item, self.world.x, self.world.y)
        #self.move([0, 0])
        
    
    def obj_here(self, x=None,y=None):
        if x == None and y == None:
            x,y = self.world.x,self.world.y
        #obj = self.world.map[x, y][-2]
        #obj = self.world.map[x, y][-2]
        #obj = self.world.map[x, y][-1]
        obj = self.world.objects[self.world.upper(x, y)]
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
        elif key == ord('d'):
            self.inv.update(self, add=None)
            self.inv.set_drop()
            return self.inv
        elif key == ord('m'):
            return PotionMaker(self, self.mx, self.my)
        
        return None
        
        

    def move(self,vector):
        #wx = self.world.x + vector[0]
        #wy = self.world.y + vector[1]
        mx = self.mx//2 + vector[0]
        my = self.my//2 + vector[1]

        f = self.world.collision(mx, my)
        if f:
            #self.world.map.remove(self.player,self.x_w_cord,self.y_w_cord)
            #self.x_w_cord += vector[0]
            #self.y_w_cord += vector[1]
            #self.world.map.place(self.player,self.x_w_cord,self.y_w_cord)
            #self.update_map()
            self.world.x += vector[0]
            self.world.y += vector[1]
            self.world.map_update()
            

    def get_obj(self):
        x, y = self.world.x, self.world.y
        obj = self.obj_here()
        #self.logwrite("Got "+obj.descr())
        if obj.pickable:
            #self.world.map.remove(obj, x, y)
            self.inv.add_item(obj)
            #self.player.bp.append(obj)
            #self.logwrite("Got "+obj.descr())
            #self.logtext = "Got "+obj.descr()
            self.logwrite("Got "+obj.descr())
            self.world.delete(x, y)
            #self.world.world_map.remove(self.world.world_map[x][y][-1])
            self.world.map_update()

    def logwrite(self, text):
        self.log.append(text)
    
    def log_draw(self, stdscr):
        stdscr.addstr(self.my+2, 1, self.log[-3])
        stdscr.addstr(self.my+3, 1, self.log[-2])
        stdscr.addstr(self.my+4, 1, self.log[-1])
        
    


    def quiting(self):
        return self.menu
