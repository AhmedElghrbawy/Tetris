from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Shapes import *
from Grid import Grid
import random

class Game:
    Grid = Grid()
    currentShape = None
    def __init__(self):
        self.main()
        
    def main(self):
        glutInit( ) 
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(400, 800)
        glutInitWindowPosition(1000,0) 
        glutCreateWindow(b'Tetris')
        glEnable(GL_DEPTH_TEST) 
        self.SetView()
        self.getShape()  # initial shape
        glutDisplayFunc(self.Draw) 
        glutSpecialFunc(self.userInput)
        glutKeyboardFunc(self.userInput)
        # glutIdleFunc(self.Draw)
        glutMainLoop()     
    
    def SetView(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 20, 0, 44, -1, 1)
        
    def getShape(self):
        self.currentShape = random.choice([ITetrominoe, OTetrominoe, JTetrominoe, TTetrominoe, LTetrominoe, STetrominoe, ZTetrominoe])(self.Grid)
        # self.currentShape = ITetrominoe(self.Grid)
        # self.currentShape = OTetrominoe(self.Grid)
        # self.currentShape = JTetrominoe(self.Grid)
        # self.currentShape = TTetrominoe(self.Grid)
        # self.currentShape = LTetrominoe(self.Grid)
        # self.currentShape = STetrominoe(self.Grid)
        # self.currentShape = ZTetrominoe(self.Grid)
        
        
    def Draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.Grid.DrawBackground() # make sure to draw this first
        self.Grid.DrawGrid()
        glutSwapBuffers()
    
    def userInput(self, key, x, y):
        locked = self.currentShape.Transform(key)
        if locked:
            self.getShape()
        self.Draw()
        
        
if __name__ == "__main__":
    g = Game()