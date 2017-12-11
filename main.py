#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import curses

from scenes import *

VERSION = '0.35'

WORLD_SIZE = 300
MAP_SIZE = 80
SCR_XSIZE = 60
SCR_YSIZE = 25
#MAP_MARG = 1 # 0 - 10

PAR = (     VERSION,     \
            WORLD_SIZE,  \
            MAP_SIZE,    \
            SCR_XSIZE,   \
            SCR_YSIZE    )

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
        #self.play = play.Play(WSIZE, MXSIZE, MYSIZE, MAP_MARG, Menu())
        self.scene = Menu(PAR)
        self.run = True

    def init_colors(self):
            curses.start_color()
            color_names =     ['red',
                               'green',
                               'yellow',
                               'blue',
                               'mag',
                               'cyan',
                               'white',
                               'black']
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
                    COLORS[(color_names[n],color_names[m])]=curses.color_pair(N)
                    N+=1
            #self.COLORS = COLORS
            return COLORS

    def draw_all(self,stdscr):
        COLORS = self.init_colors()
        curses.curs_set(0)
        while self.run:
            stdscr.clear()
            #stdscr.refresh()
            self.scene.draw(stdscr, COLORS)
            stdscr.refresh()
            k = stdscr.getch()
            if k == ord('q'):
                self.scene = self.scene.quiting()
            elif k == ord('h'):
                #self.scene = self.help_p
                self.scene = Help(self.scene)
            #elif k == ord('c'):
            #    self.scene = self.play
            else:
                smth = self.scene.inp_handler(k)
                '''
                If scene.inp_handler returns smth that is not None
                Switch to that scene
                '''
                if smth:
                    self.scene = smth
            if not self.scene:
                self.run = False
        curses.curs_set(1)


if __name__ == "__main__":
    g1 = Game()
    curses.wrapper(g1.draw_all)
