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
    gameOver = False
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
        try: # tries to spawn a new shape. if it fail, game ends
            self.currentShape = self.shapeBag[-1](self.Grid) 
        except ValueError as err:
            self.gameOver = True
            self.EndGame()
        self.shapeBag.pop(-1)
        
        self.Grid.next3Shapes = self.shapeBag[-1: -4: -1]        # last 3 shapes of shape bag
        
        
    def Draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.Grid.DrawBackground(None, None, None) # make sure to draw this first
        self.Grid.DrawGrid()
        self.Grid.DrawNextBackground()
        self.Grid.DrawNextGrid()
        self.RenderScore()
        glutSwapBuffers()
    
    def userInput(self, key, x, y):
        if self.gameOver:
            return
        locked, currentPos = self.currentShape.HandleInput(key)
        if locked:
            self.score += self.Grid.ClearLines(currentPos, self.Level, self)
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
    

    def RenderScore(self, x = 22, y = 15):
        glMatrixMode(GL_MODELVIEW)
        glColor(0, 1, 0)
        glLoadIdentity()
        glTranslate(x, y, 0)
        glScale(.009, .009, 1)
        score = "Score: " + str(self.score)
        level = "Level: " + str(self.Level)
        score = score.encode()
        level = level.encode()
        for c in score:
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, c) 
        glLoadIdentity()
        glTranslate(x, y-2, 0)
        glScale(.009, .009, 1)
        for c in level:
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, c) 
        
    def EndGame(self):
        glutDisplayFunc(self.EndGame)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.RenderScore(10, 20)
        glColor3f(1, 0, 0)
        glLoadIdentity()
        glTranslate(10, 22, 0)
        glScale(.009, .009, 1)
        for c in 'game over :('.encode():
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, c)
        glutSwapBuffers()
        pygame.mixer.stop()
        pygame.mixer.music.load("end.mp3")
        pygame.mixer.music.play(1)
        glutTimerFunc(3000, sys.exit, 1)
        glutMainLoop()
               
if __name__ == "__main__":
    g = Game()