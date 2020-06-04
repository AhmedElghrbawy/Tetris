from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from Shapes import *
from Grid import Grid
import random
import sys


class Game:
    Grid = Grid()          # Grid objects to be renderd
    currentShape = None    # shape that the user has access to currently
    shapeBag = []          # Random bag of shapes to be used next
    Level = 1
    score = 0
    gameOver = False       # used to disable functionality when game ends
    Holded = False         # indicates if current shape is holded (can be swaped or not)
    Lines = 0              # number of cleard lines
    def __init__(self):
        self.main()
        
    def main(self):
        glutInit() 
        pygame.mixer.init()
        pygame.mixer.music.load("Tetris_GameBoy.mp3")
        pygame.mixer.music.play(-1)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(600,0) 
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
        glOrtho(-14, 34, 0, 40, -1, 1)
        
    def getShape(self):
        '''
        Defines shapes Bag and updates currentShape
        '''
        if len(self.shapeBag) <= 3:  # make sure 3 next Shapes exist
            tempList = [ITetrominoe, OTetrominoe, JTetrominoe, TTetrominoe, LTetrominoe, STetrominoe, ZTetrominoe]
            random.shuffle(tempList)
            self.shapeBag = [*tempList, *self.shapeBag]  # prepend tempList to shapeBag
        try: # tries to spawn a new shape. if it fail, game ends
            self.currentShape = self.shapeBag[-1](self.Grid) 
        except ValueError as err:
            self.gameOver = True
            self.EndGame()
        self.shapeBag.pop(-1)
        self.Grid.next3Shapes = self.shapeBag[-1: -4: -1]        # last 3 shapes of shape bag to render in next grid
        
        
    def Draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.Grid.DrawBackground(None, None, None) 
        self.Grid.DrawGrid()
        self.Grid.DrawNextBackground()
        self.Grid.DrawNextGrid()
        self.Grid.DrawHoldBackGround()
        self.Grid.DrawHoldGrid()
        self.RenderScore()
        glutSwapBuffers()
    
    def userInput(self, key, x, y):
        if self.gameOver:  # ignore user input
            return
        if key == b'c':
            self.Hold()
        locked, currentPos = self.currentShape.HandleInput(key)
        if locked:
            n = self.Grid.ClearLines(currentPos, self)
            self.Lines += n
            self.score += 100 * self.Level * n  # added score based on cleared lines
            self.score += 50 * self.Level       # added score based on locked
            self.getTime()   # adjust score and time
            self.getShape()
            if self.Holded:
                self.Holded = False     # inhold shape can be swaped now
        self.Draw()
        
    def Hold(self):
        if self.Holded:   # cant make swap
            return
        self.currentShape.Update(0)
        if self.Grid.inHold == None:    #  inhold is empty, put current shape in it and get new shape
            self.Grid.inHold = type(self.currentShape)
            self.getShape()
            self.Holded = True
        else:                        # inhold no empty, swap
            self.Grid.inHold, self.currentShape = type(self.currentShape), self.Grid.inHold(self.Grid)
            self.Holded = True
              
    
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
        Lines = "Lines: " + str(self.Lines)
        score = score.encode()
        level = level.encode()
        Lines = Lines.encode()
        for c in score:
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, c) 
        glLoadIdentity()
        glTranslate(x, y-2, 0)
        glScale(.009, .009, 1)
        for c in level:
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, c) 
        glLoadIdentity()
        glTranslate(x, y-4, 0)
        glScale(.009, .009, 1)
        for c in Lines:
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, c) 
        
        
    def EndGame(self):
        glutDisplayFunc(self.EndGame)   # change the seen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.RenderScore(4, 20)
        glColor3f(1, 0, 0)
        glLoadIdentity()
        glTranslate(4, 22, 0)
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