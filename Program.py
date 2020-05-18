from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Shapes import *
from Grid import Grid
import random

class Program:
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
        glutDisplayFunc(self.SetView) 
        # glutIdleFunc(SetView)
        glutMainLoop()     
    
    def SetView(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 20, 0, 40, -1, 1)
        self.Draw()
    def Draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        currentShape = random.choice([ITetrominoe, OTetrominoe, JTetrominoe, TTetrominoe, LTetrominoe, STetrominoe, ZTetrominoe])(self.Grid)
        self.Grid.DrawBackground() # make sure to draw this first
        self.Grid.DrawGrid()
        glutSwapBuffers()
        
        
if __name__ == "__main__":
    P = Program()