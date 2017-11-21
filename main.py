#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import curses

MXSIZE, MYSIZE = 20, 20

class Map(dict):
    
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.screen = None
        for i in range(self.x):
            for j in range(self.y):
                self[i, j] = "."
        

class Console(object):

    def __init__(self):
        self.init_curses()

    def init_curses(self):

        self.fullwin = curses.initscr()
        self.init_colors()
        self.x, self.y = MXSIZE, MYSIZE
        self.screen = curses.newwin(MXSIZE, MYSIZE)
        self.log = curses.newwin(5, MXSIZE, 0, MYSIZE)
        self.panel = curses.newwin(MYSIZE, 10, MXSIZE, 0)
        self.inv = curses.newwin(0, 0)
        self.panel.scrollok(False)
        self.log.scrollok(True)
        curses.noecho()
        curses.cbreak()
        orig = curses.curs_set(0)
        self.screen.keypad(1)
            #self.update()

    def init_colors(self):
        curses.start_color()
        color_names =     ['r',
                           'g',
                           'y',
                           'b',
                           'm',
                           'c',
                           'w',
                           'b']
        color_list =      [curses.COLOR_RED,
                           curses.COLOR_GREEN,
                           curses.COLOR_YELLOW,
                           curses.COLOR_BLUE,
                           curses.COLOR_MAGENTA,
                           curses.COLOR_CYAN,
                           curses.COLOR_WHITE,
                           curses.COLOR_BLACK]
        self.cp = {}
        N = 1
        for n in range(len(color_list)):
            for m in range(len(color_list)):
                curses.init_pair(N, color_list[n], color_list[m])
                self.cp[(color_names[n],color_names[m])]=N
                N+=1
                
    def deinit_curses(self):
        curses.nocbreak()
        try:
            pad.keypad(0)
        except NameError:
            pass
        curses.echo()
        try:
            curses.curs_set(orig)
        except:
            pass
        curses.endwin()
    
    
    def update(self, map):
        self.screen_print(map)
        self.screen.refresh()
        self.log.refresh()
        self.panel.refresh()

    def screen_print(self,m1):
        for j in range(self.x):
            for i in range(self.y):
                self.screen.addstr(0, 0, m1[i, j], curses.color_pair(self.cp[('r','g')]))

class Game(object):
    def __init__(self):
        self.init_game()
        
    def init_game(self):
        m1 = Map(MXSIZE, MYSIZE)
        self.console = Console()
        self.console.update(m1)

if __name__ == '__main__':
    g1 = Game()
    #g1.console.deinit_curses()
