#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import curses
import random
from tools import *
from objects import *

WSIZE = 100
MXSIZE = 31
MYSIZE = 21
MAP_MARG = 1 # 0 - 10

class Map(dict):

    def __init__(self, size):
        self.x, self.y = size
        self.screen = None
        for j in range(self.y):
            for i in range(self.x):
                self[i, j] = Field(i,j)
        self.aloop = []
        self.console = None
        #self.prng = ((0,self.x),(0,self.y))
        self.prng = ((self.x//2-MXSIZE,self.x//2+MXSIZE),(self.y//2-MYSIZE,self.y//2+MYSIZE))

    #__repr__ = object.__repr__
    #__str__ = object.__str__

    def print(self, COLORS):
        prng = self.prng
        m = MAP_MARG
        for j in range(prng[1][0],prng[1][1]):
            n = MAP_MARG
            for i in range(prng[0][0],prng[0][1]):
                obj = self[i, j]
                cc = obj.color()
                self.screen.addstr(m, n, str(obj), curses.color_pair(COLORS[cc]))
                n+=1
            m+=1
        x = prng[0][1]-MXSIZE//2
        y = prng[1][1]-MYSIZE//2
        #that = self[x, y]
        #self.screen.addstr(MSIZE, 0, that.descr(), curses.color_pair(0))



    def place(self, obj, x, y, actions=False):
        "Places obj on the map on x, y."
        self[x, y].append(obj)
        obj.pos = x, y
        obj.map = self
        if actions:
            self.aloop.append(obj)

    def distance(self, obj1, obj2):
        """Returns the distance between obj1 and obj2"""
        x1, y1 = obj1.pos
        x2, y2 = obj2.pos
        xdist = abs(x1 - x2)
        ydist = abs(y1 - y2)
        dist = max(xdist, ydist)
        return dist

    def remove(self, obj, x, y):
        field = self[x, y]
        field.remove(obj)

class World(object):
    def __init__(self):
        self.size = WSIZE
        self.init_world_obj()
        self.create_world()
        self.create_plants()
        self.create_objs()

    def init_world_obj(self):
        self.plants = {
                        Tree():0.1,
                        Bush():0.05,
                      }
        self.objects = {
                          Stone():0.005,
                          Mushroom():0.001
                        }


    def create_world(self):
        self.map = Map((WSIZE,WSIZE))
        for i in range(WSIZE):
            for j in range(WSIZE):
                if i<=MXSIZE//2 or i>=WSIZE-MXSIZE//2 \
                   or j<=MYSIZE//2 or j>=WSIZE-MYSIZE//2:
                    obj = Rock()
                else:
                    rndclr = (random.choice((\
                                               'GREEN',\
                                               'YELLOW',\
                                               'WHITE',\
                                               'RED')),'BLACK')
                    obj = Ground(rndclr)
                self.map.place(obj,i,j)
        st = Stick()
        self.map.place(st,WSIZE//2+3,WSIZE//2+3)

    def create_plants(self):
        for i in range(MXSIZE//2,WSIZE-MXSIZE//2):
            for j in range(MYSIZE//2,WSIZE-MYSIZE//2):
                for plant in self.plants:
                    if random.random()<self.plants[plant]:
                        self.map.place(plant,i,j)
                        break

    def create_objs(self):
        for i in range(MXSIZE//2,WSIZE-MXSIZE//2):
            for j in range(MYSIZE//2,WSIZE-MYSIZE//2):
                for obj in self.objects:
                    if random.random()<self.objects[obj]:
                        self.map.place(obj,i,j)
                        #break

class Game():
    
    def __init__(self):
        self.init_play()
    
    def preview(self, stdscr):
        key = 0
        height, width = stdscr.getmaxyx()
        curses.curs_set(0)
        self.back_scene = self.preview
        stdscr.clear()
        stdscr.refresh()
        title = "POTION MASTER RL"
        subtitle = "v0.0.3"
        info = "PMRL is roguelike about making potions and stuff."
        bar = "[C]ontinue   [H]elp   [Q]uit"
        startx_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        startx_subtitle = int((width // 2) - (len(subtitle) // 2) - len(title) % 2)
        startx_info = int((width // 2) - (len(info) // 2) - len(title) % 2)
        startx_bar = int((width // 2) - (len(bar) // 2) - len(title) % 2)
        while (True):
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(height//2-2, startx_title, title)
            stdscr.attroff(curses.A_BOLD)
            stdscr.addstr(height//2-1, startx_subtitle, subtitle)
            stdscr.addstr(height//2, startx_info, info)
            stdscr.addstr(height-1, startx_bar, bar)
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('h'):
                curses.wrapper(self.help_page)
                break
            elif key == ord('q'):
                break
            elif key == ord('c'):
                curses.wrapper(self.play)
        
    def init_play(self):
        
        self.world = World()
        self.x_w_cord = self.world.size//2
        self.y_w_cord = self.world.size//2
        self.create_map()
        self.player = Player()
        self.player.bp = ["Cauldron"]
        self.world.map.place(self.player,self.x_w_cord,self.y_w_cord)
        
        
    def play(self, stdscr):
        self.init_colors()
        curses.curs_set(0)
        self.world.map.screen = stdscr
        self.back_scene = self.play
        self.log = curses.newwin(10, 50)
        #stdscr.clear()
        #stdscr.refresh()
        while True:
            stdscr.clear()
            stdscr.refresh()
            self.world.map.print(self.COLORS)
            x, y = self.x_w_cord, self.y_w_cord
            self.panel_text = self.world.map[x, y].descr()
            #stdscr.addstr(MYSIZE, 1, self.panel_text)
            self.log.addstr(0,0,self.panel_text)
            self.log.refresh()
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_DOWN:
                self.move( [ 0,  1] )
            elif key == curses.KEY_LEFT:
                self.move( [-1,  0] )
            elif key == curses.KEY_UP:
                self.move( [ 0, -1] )
            elif key == curses.KEY_RIGHT:
                self.move( [ 1,  0] )
            elif key == ord('g'):
                self.get_obj()
            
            elif key == 27 or key == ord('q'):
                break
            elif key == ord('i'):
                curses.wrapper(self.inventory)
                break
            elif key == ord('h'):
                curses.wrapper(self.help_page)
                break
        
    
    def inventory(self, stdscr):
        key = 0
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        title = "Inventory (q or ESC to exit): "
        while True:
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(MAP_MARG, MAP_MARG, title)
            stdscr.attroff(curses.A_BOLD)
            i = MAP_MARG + 1 
            for item in self.player.bp:
                stdscr.addstr(i, MAP_MARG, item)
                i+=1
            stdscr.refresh()
            key = stdscr.getch()
            if key != 0:
                curses.wrapper(self.play)
                break
    
    def help_page(self, stdscr):
        key = 0
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        title = "Help page (any key to exit):"
        with open('help.txt', 'r') as f:
            read_data = f.readlines()
        while True:
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(MAP_MARG, MAP_MARG, title)
            stdscr.attroff(curses.A_BOLD)
            i = MAP_MARG + 1
            for line in read_data:
                stdscr.addstr(i, 2, line)
                i+=1
            key = stdscr.getch()
            stdscr.refresh()
            if key != 0:
                curses.wrapper(self.back_scene)
                break
    
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
            self.world.map.console.logwrite("Got " + obj.descr())
            self.player.bp.append(obj)
        else:
            #self.world.map.console.logwrite(obj.descr()+" isn't pickable!")
            self.world.map.console.logwrite("Nothing to pick!")
        self.world.map.console.refresh()

    def create_map(self):
        self.world.map.prng = ((self.x_w_cord-MXSIZE//2,self.x_w_cord+MXSIZE//2),\
                         (self.y_w_cord-MYSIZE//2,self.y_w_cord+MYSIZE//2))



    def init_colors(self):
            curses.start_color()
            color_names =     ['RED',
                               'GREEN',
                               'YELLOW',
                               'BLUE',
                               'MAGENTA',
                               'CYAN',
                               'WHITE',
                               'BLACK']
            color_list =      [curses.COLOR_RED,
                               curses.COLOR_GREEN,
                               curses.COLOR_YELLOW,
                               curses.COLOR_BLUE,
                               curses.COLOR_MAGENTA,
                               curses.COLOR_CYAN,
                               curses.COLOR_WHITE,
                               curses.COLOR_BLACK]
            COLORS = {}
            N = 1
            for n in range(len(color_list)):
                for m in range(len(color_list)):
                    curses.init_pair(N, color_list[n], color_list[m])
                    COLORS[(color_names[n],color_names[m])]=N
                    N+=1
            self.COLORS = COLORS
                
def draw_scene(scene):
    curses.wrapper(scene)

if __name__ == "__main__":

    g1 = Game()
    draw_scene(g1.preview)
