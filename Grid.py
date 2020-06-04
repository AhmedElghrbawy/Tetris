from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import copy

class Grid:
    row = 22  # 2 extra invisible rows
    column = 10
    grid = []    # underlying data structure
    nextGrid = []
    next3Shapes = []
    holdGrid = []
    inHold = None   # shape in hold 
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
           
           
       
                 
    def DrawBackground(self, rows, columns, origin):
        '''
        Draws background grid (horizontal and vertical lines)\n
        parameters:\n
        rows: number of rows
        columns: number of columns
        origin: origin of grid
        '''
        if rows == None:      # Default grid is main graid
            rows = self.row
            columns = self.column
            origin = (0, 0)
        Xo, Yo = origin
        XL = (columns + 1) * 2
        YL = (rows + 1 ) * 2
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()                                     # block size 2 * 2
        glColor(1, 1, 1)                           
        glBegin(GL_LINES)                                     
        for y in range(Yo, Yo + YL, 2):            # Draw H lines
            glVertex2f(Xo, y)
            glVertex2f(Xo + columns * 2, y)             
        for x in range(Xo, Xo + XL, 2):         # Draw V lines
            glVertex2f(x, Yo)
            glVertex2f(x, Yo + rows * 2)
        glEnd()   

    def DrawGrid(self):
        '''
        Draws tetrominoes blocks using the color stored in the underlying array data structure
        '''
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
        
    def ClearLines(self, position, Game):
        '''
        Clears completed lines if exsit
        '''
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
        n = rowsToClear[1]          # number of rows to be cleared (for scoring system)
        while rowsToClear[1] > 0:
            # Animate
            x = 0
            while x < 1:
                color = (1, x, x)
                for cell in self.grid[rowsToClear[0]]:
                    cell[1] = color
                Game.Draw()
                x += .01
            
            # erase completed row
            self.grid.pop(rowsToClear[0])
            rowsToClear[0] -= 1
            rowsToClear[1] -= 1
            # make a new row
            self.grid.append([])         
            lis = [0, (0, 0, 0)]
            for j in range(self.column):
                self.grid[-1].append(copy.deepcopy(lis))    
        
        return n 
        
    def DrawNextBackground(self):
        self.DrawBackground(8, 4, (24, 20))
    
    def DrawNextGrid(self):
        '''
        updates the underlayin Data structure with the 3 next shapes
        '''
        self.ClearNextGrid()   # clear grid every time before drawing agian
        row = len(self.nextGrid) - 1
        for shape in self.next3Shapes:
            for r in range(len(shape.states[0])):
                for c in range(len(shape.states[0][0])):
                    if shape.states[0][r][c] == 1:
                        self.nextGrid[row - r][c] = shape.color
            row -= 3
        self.UpdateNextGridColors()  
        

    def ClearGrid(self, rows, columns):
        grid = [0] * rows
        for i in range(rows):
            grid[i] = []
            for j in range(columns):
                grid[i].append((0, 0, 0))
        return grid
    
    
    def ClearNextGrid(self):
        self.nextGrid = self.ClearGrid(8, 4)
        
    def UpdateGridColors(self, grid, origin):
        '''
        updates the color for the user
        '''
        Xo, Yo = origin
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glBegin(GL_QUADS)
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                color = grid[i][j]
                glColor(*color)
                x = j * 2 + Xo
                y = i * 2 + Yo
                blockLen = 2
                glVertex2f(x , y)
                glVertex2f(x , y + blockLen )
                glVertex2f(x + blockLen , y + blockLen)
                glVertex2f(x + blockLen , y )
        glEnd()
        
        
        
    def UpdateNextGridColors(self):
        self.UpdateGridColors(self.nextGrid, (24, 20))
        
                
    def DrawHoldBackGround(self):
        self.DrawBackground(2, 4, (-12, 30))
    
    def ClearHoldGrid(self):
        self.holdGrid = self.ClearGrid(2, 4)
        
    def DrawHoldGrid(self):
        if self.inHold == None:
            return
        self.ClearHoldGrid()
        for i in range(2):     # only two rows in intial state
            for j in range(len(self.inHold.states[0][0])):  
                if self.inHold.states[0][i][j] == 1:
                    self.holdGrid[i][j] = self.inHold.color
        self.UpdateGridColors(self.holdGrid, (-12, 30))
        