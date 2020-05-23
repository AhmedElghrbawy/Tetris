from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from Shapes import *
from Grid import Grid
import random
import sys


class Game:
    Grid = Grid()
    currentShape = None
    shapeBag = []
    Level = 1
    score = 0
    def __init__(self):
        self.main()
        
    def main(self):
        glutInit() 
        pygame.mixer.init()
        pygame.mixer.music.load("Tetris_GameBoy.mp3")
        pygame.mixer.music.play(-1)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(600, 800)
        glutInitWindowPosition(800,0) 
        glutCreateWindow(b'Tetris')
        glEnable(GL_DEPTH_TEST) 
        self.SetView()
        self.getShape()  # initial shape
        glutDisplayFunc(self.Draw) 
        glutSpecialFunc(self.userInput)
        glutKeyboardFunc(self.userInput)
        glutTimerFunc(self.getTime(), self.Gravity, 1)
        glutMainLoop()     
    
    def SetView(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 34, 0, 40, -1, 1)
        
    def getShape(self):
        '''
        Defines shapes Bag and updates currentShape
        '''
        if len(self.shapeBag) <= 3:
            tempList = [ITetrominoe, OTetrominoe, JTetrominoe, TTetrominoe, LTetrominoe, STetrominoe, ZTetrominoe]
            random.shuffle(tempList)
            self.shapeBag = [*tempList, *self.shapeBag]
        try: # tries to make a new shape. if it fail, game ends
            self.currentShape = self.shapeBag[-1](self.Grid) 
        except ValueError as err:
            print(repr(err))
            sys.exit()
        self.shapeBag.pop(-1)
        
        self.Grid.next3Shapes = self.shapeBag[-1: -4: -1]        # last 3 shapes of shape bag
        
        
    def Draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.Grid.DrawBackground() # make sure to draw this first
        self.Grid.DrawGrid()
        self.Grid.DrawNextBackground()
        self.Grid.DrawNextGrid()
        self.RengerScore()
        glutSwapBuffers()
    
    def userInput(self, key, x, y):
        locked, currentPos = self.currentShape.HandleInput(key)
        if locked:
            self.score += self.Grid.ClearLines(currentPos, self.Level)
            self.score += 100 * self.Level
            self.getTime()   # adjust score and time
            self.getShape()
        self.Draw()
        
    def Gravity(self, value):
        '''
        auto transforms object down
        '''
        self.userInput(GLUT_KEY_DOWN, None, None)
        glutTimerFunc(self.getTime(), self.Gravity, 1)
        
    def getTime(self):
        '''
        returns Graity transformation time based on current level
        '''
        if self.score >= 2**(self.Level - 1) * 1000:
            self.Level += 1
        time = 1200 - 200 * self.Level
        if time < 200:
            time = 200
        return  time
    

    def RengerScore(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glScale(.12, .12, 1)
        score = "Score: " + str(self.score)
        level = "Level: " + str(self.Level)
        print(score, level)
        # for c in score:
        #     glutStrokeString(GLUT_STROKE_MONO_ROMAN, c) 
        
        
if __name__ == "__main__":
    g = Game()