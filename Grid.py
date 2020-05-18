from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import copy

class Grid:
    row = 20
    column = 10
    grid = []
    def __init__(self):
        self.grid = [0] * (self.row + 2)              # [full, (RGBcolor)]        
        for i in range(0, self.row + 2):    # 2 extra rows
            self.grid[i] = []
            lis = [1, (0, 0, 0)]
            for j in range(10):
                self.grid[i].append(copy.deepcopy(lis)) 
        # print(self.grid[3][3])
            
    def DrawBackground(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()                                     # block size 2 * 2
        glColor(1, 1, 1)                           
        glBegin(GL_LINES)                                     # visible Columns 20 --> 0 
        for y in range(0, (self.row + 1) * 2, 2):            # Draw H lines
            glVertex2f(0, y)
            glVertex2f((self.column) * 2, y)             
        for x in range(0, (self.column + 1) * 2, 2):         # Draw V lines
            glVertex2f(x, 0)
            glVertex2f(x, (self.row + 2) * 2)
        glEnd()   

    def DrawGrid(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glBegin(GL_QUADS)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                cell = self.grid[i][j]
                if cell[0] != 0:
                    glColor(*cell[1])
                    x = j * 2
                    y = i * 2
                    blockLen = 2
                    glVertex2f(x , y)
                    glVertex2f(x , y + blockLen )
                    glVertex2f(x + blockLen , y + blockLen)
                    glVertex2f(x + blockLen , y )
        glEnd()