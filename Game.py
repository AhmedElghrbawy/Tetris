from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
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
        glutInit( ) 
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
        glutSwapBuffers()
    
    def userInput(self, key, x, y):
        locked, currentPos = self.currentShape.Transform(key)
        if locked:
            self.score += self.Grid.ClearLines(currentPos, self.Level)
            self.score += 100 * self.Level
            print("score", self.score)
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
        
        
if __name__ == "__main__":
    g = Game()