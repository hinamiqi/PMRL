#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import curses


import play

WSIZE = 100
MXSIZE = 31
MYSIZE = 21
MAP_MARG = 1 # 0 - 10

'''
Простые сцены.
Здесь при создании объекта класса инициализируются атрибуты (строки),
а в методе draw они просто выводятся на передаваемым ему экран.
Метод quiting вызывается в главном лупе если пользователь нажимает q.
Поэтому он должен возваращать значение сцены, к которой следует 
вернуться. Если метод возваращает None то главный луп просто 
прерывается.
'''
class Menu():
    def __init__(self):
        self.title = "POTION MASTER RL"
        self.subtitle = "v0.0.31"
        self.info = "PMRL is roguelike about making potions and stuff."
        self.bar = "[C]ontinue   [H]elp   [Q]uit"
        
    def draw(self, stdscr):
        height, width = MYSIZE, MXSIZE*2
        self.startx_title = int((width // 2) - (len(self.title) // 2) - len(self.title) % 2)
        self.startx_subtitle = int((width // 2) - (len(self.subtitle) // 2) - len(self.subtitle) % 2)
        self.startx_info = int((width // 2) - (len(self.info) // 2) - len(self.title) % 2)
        self.startx_bar = int((width // 2) - (len(self.bar) // 2) - len(self.title) % 2)
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(height//2-2, self.startx_title, self.title)
        stdscr.attroff(curses.A_BOLD)
        stdscr.addstr(height//2-1, self.startx_subtitle, self.subtitle)
        stdscr.addstr(height//2, self.startx_info, self.info)
        stdscr.addstr(height-1, self.startx_bar, self.bar)
    
    def inp_handler(self, key):
        pass
    
    def quiting(self):
        return None

class Help():
    def __init__(self, prev_secene):
        self.prev_scene = prev_secene
        self.title = "Help page (any key to exit):"
        with open('help.txt', 'r') as f:
            self.data = f.readlines()
        
        
        
    def draw(self,stdscr):
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(MAP_MARG, MAP_MARG, self.title)
        stdscr.attroff(curses.A_BOLD)
        i = MAP_MARG + 1
        for line in self.data:
            stdscr.addstr(i, 2, line)
            i+=1
    
    def inp_handler(self, key):
        pass
    
    def quiting(self):
        return self.prev_scene

   

'''
Главный объект, содержащий в себе основные переменные (созданный или
загруженный мир, координаты игрока в нем, состояние игрока и прочее),
а также текущую сцену self.scene. Это объект, который имеет атрибуты
содержащие в себе информацию, которая должна выводится в текущей сцене,
и по крайней мере один метод draw(screen). 
Главный объект содержит главный метод draw_all(screen). Этот метод
необходимо вызывать с помощью curses.wrapper(Game.draw_all), так как
для его работы должен быть инициализирован curses. 
В этом методе содержится главный (желательно, единственный) луп, в
котором screen (передающийся wrapper) очищается, затем вызывается 
функция .draw текущей сцены и экран обновляется. Таким образом на 
экране всегда существует то, что рисуется в методе draw() текущей сцены.
В этом лупе так же необходимо разместить обработчик нажатий клавиш.
Каждая сцена должна иметь свои методы обработки клавиш. В главном лупе
всё должно просто вызываться и всё.
'''
class Game(object):
    '''
    Объекты нужно создать один раз. Потом нужно переделать систему и 
    наследовать все объекты-сцены от главного объекта Scene.
    '''
    
    def __init__(self):
        #self.menu = Menu()
        #self.help_p = Help()
        self.play = play.Play(WSIZE, MXSIZE, MYSIZE, MAP_MARG, Menu())
        self.scene = Menu()
        self.run = True
    
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
            #self.COLORS = COLORS
            return COLORS
    
    def draw_all(self,stdscr):
        COLORS = self.init_colors()
        curses.curs_set(0)
        while self.run:
            stdscr.clear()
            #stdscr.refresh()
            self.scene.draw(stdscr)
            stdscr.refresh()
            k = stdscr.getch()
            if k == ord('q'):
                self.scene = self.scene.quiting()
            elif k == ord('h'):
                #self.scene = self.help_p
                self.scene = Help(self.scene)
            elif k == ord('c'):
                self.scene = self.play
            else:
                self.scene.inp_handler(k)
            if not self.scene:
                self.run = False
        curses.curs_set(1)
        
    
if __name__ == "__main__":
    g1 = Game()
    curses.wrapper(g1.draw_all)
