from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import copy

class Grid:
    row = 20
    column = 10
    grid = []
    nextGrid = []
    next3Shapes = []
    def __init__(self):
        # main grid init
        self.grid = [0] * (self.row + 2)  # to avoid index out of range   # [full, (RGBcolor)]        
        for i in range(0, self.row + 2):    # 2 extra rows
            self.grid[i] = []
            lis = [0, (0, 0, 0)]
            for j in range(self.column):
                self.grid[i].append(copy.deepcopy(lis))
        # next grid init        
        self.ClearNextGrid()
           
           
    def ClearNextGrid(self):
        self.nextGrid = [0] * 8 
        for i in range(8):
            self.nextGrid[i] = []
            for j in range(4):
                self.nextGrid[i].append((0, 0, 0))   
                 
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
        
    def ClearLines(self, position, level):
        rowsToClear = [-1, 0] # stores the index of the top-most completed row (if exists) and number of rows
        row = position[0]
        for row in range(row, row - 4, -1):
            if row < 0: # out of range
                break
            full = True
            for cell in self.grid[row]:
                if cell[0] == 0:
                    full = False
                    break
            if full == True:
                rowsToClear[0] = max(rowsToClear[0], row)  # store top most
                rowsToClear[1] += 1 # increase number of rows
        n = rowsToClear[1]          # number of rows to be cleared (for scoring)
        while rowsToClear[1] > 0:
            # erase completed row
            self.grid.pop(rowsToClear[0])
            rowsToClear[0] -= 1
            rowsToClear[1] -= 1
            # make a new row
            self.grid.append([])         
            lis = [0, (0, 0, 0)]
            for j in range(self.column):
                self.grid[-1].append(copy.deepcopy(lis))    
        
        return n * 100 * level
        
    def DrawNextBackground(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()                                     # block size 2 * 2
        glColor(0, 0, 1)                           
        glBegin(GL_LINES)
        for x in range(24, 34, 2):
            glVertex2f(x, 20)
            glVertex2f(x, 36)
        for y in range(20, 38, 2):
            glVertex2f(24, y)
            glVertex2f(32, y)
        glEnd()
    
    def DrawNextGrid(self):
        self.ClearNextGrid()
        row = len(self.nextGrid) - 1
        for shape in self.next3Shapes:
            for r in range(len(shape.states[0])):
                for c in range(len(shape.states[0][0])):
                    if shape.states[0][r][c] == 1:
                        self.nextGrid[row - r][c] = shape.color
            row -= 3
        self.UpdateNextGridColors()


        
    def UpdateNextGridColors(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glBegin(GL_QUADS)
        for i in range(len(self.nextGrid)):
            for j in range(len(self.nextGrid[i])):
                color = self.nextGrid[i][j]
                glColor(*color)
                x = j * 2 + 24
                y = i * 2 + 20
                blockLen = 2
                glVertex2f(x , y)
                glVertex2f(x , y + blockLen )
                glVertex2f(x + blockLen , y + blockLen)
                glVertex2f(x + blockLen , y )
        glEnd()
                
