import os
import keyboard
import msvcrt
import random
import time


class Point():
    def __init__(self, x, y, w, h, keys, symbol, screen):
        self.x = x
        self.y = y
        self.xOld = x
        self.yOld = y
        self.w = w
        self.h = h
        self.keys = keys
        self.symbol = symbol
        self.score = 0
        self.screen = screen

    def move(self):
            def ifMove():
                if (self.x>=0 and self.x<self.w) and (self.y>=0 and self.y<self.h) and (self.screen.arr[self.y][self.x] != self.screen.block):
                    return True
                else: 
                    return False
            self.xOld = self.x
            self.yOld = self.y
            if keyboard.is_pressed(self.keys[0]):#a 
                self.x -= 1
                if ifMove() == False:
                    self.x += 1  
            if keyboard.is_pressed(self.keys[1]):#d
                self.x += 1
                if ifMove() == False:
                    self.x -= 1
            if keyboard.is_pressed(self.keys[2]):#w
                self.y -= 1
                if ifMove() == False:
                    self.y += 1
            if keyboard.is_pressed(self.keys[3]):#s
                self.y += 1
                if ifMove() == False:
                    self.y -= 1
            

class Screen():
    def __init__(self, w, h, fill, n, block):
        self.w = w
        self.h = h
        self.fill = fill
        self.block = block
        self.n = n
        self.arr = [[self.fill]*w for i in range(h)] 

    def setBlocks(self):
        for i in range(self.n):
            while True:
                x = random.randint(0, self.w-1)
                y = random.randint(0, self.h-1)
                if self.arr[y][x] == self.fill:
                    self.setPoint(x, y, self.block)
                    break

    def show(self, texts):
        os.system('cls')
        for i in self.arr:
            for j in i:
                print(j, end='')
            print()
        for text in texts:
            print(text, end='')
        print()
    
    def setPoint(self, x, y, symbol):
        self.arr[y][x] = symbol

    def delPoint(self, xOld, yOld):
        self.arr[yOld][xOld] = self.fill

    def movePoint(self, x, y, xOld, yOld, symbol):
        self.delPoint(xOld, yOld)
        self.setPoint(x, y, symbol)


class Star():
    def __init__(self, w, h, screen, aim):
        self.w = w
        self.h = h
        self.screen = screen
        self.aim = aim
        self.setStar()
    
    def setStar(self):
        while True:
            self.x = random.randint(0, self.w-1)
            self.y = random.randint(0, self.h-1)
            if self.screen.arr[self.y][self.x] == self.screen.fill:
                self.screen.setPoint(self.x, self.y, self.aim)
                break


class Game():
    def __init__(self, DATA):
        self.screen = Screen(**DATA["screen"])
        self.points = []
        for pointName in DATA["points"]:
            self.points.append(Point(w = self.screen.w, h = self.screen.h, screen = self.screen, **DATA["points"][pointName]))
        if DATA["game"]["blocks"]:
            self.screen.setBlocks()
        self.star = Star(self.screen.w, self.screen.h, self.screen, DATA["star"]["aim"])

    
    def turn(self):
        self.texts = []
        for point in self.points:
            point.move()
            self.screen.movePoint(point.x, point.y, point.xOld, point.yOld, point.symbol)
            self.texts.append(f"{point.symbol}:{point.score} ")
            self.screen.show(self.texts)
            if (point.x == self.star.x) and (point.y == self.star.y):
                point.score += 1 
                self.star.setStar()


DATA = {
    "game" : {
        "blocks" : True
    },
    "screen" : {
        "w" : 10,
        "h" : 10,
        "fill" : ' ',
        "n" : 20,
        "block" : '#'
    },
    "star" : {
        "aim" : '*'
    },
    "points" : { 
        "point1" : {
            "x" : 1,
            "y" : 1,
            "keys" : ['a', 'd', 'w', 's'],
            "symbol" : 'X',
        },
        "point2" : {
            "x" : 1,
            "y" : 5,
            "keys" : ['j', 'l', 'i', 'k'],
            "symbol" : 'O',
        },
    }
}


game = Game(DATA)
while True:
    time.sleep(0.1)
    if msvcrt.getch() == b'\x1b': exit(0)
    game.turn()
