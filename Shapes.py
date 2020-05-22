from OpenGL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Grid import Grid
from abc import ABC

class Shape(ABC):
    def __init__(self, Grid, states, color):
        self.currentPosition =  [Grid.row, int(Grid.column / 2 - 2)]  # top left Pos
        self.grid = Grid.grid
        self.states = states
        self.indexOfState = 0    # declares the index of current state
        self.currentState = states[self.indexOfState]
        self.color = color
        self.locked = False
        self.Spawn() 
        
    def Spawn(self):
        '''
        try to spawn in row 21. if fail then try row 22. if both fails, game ends
        '''
        first = self.ValidTransforamtion(self.currentPosition, self.currentState)
        if first:
            self.Update(1)
            return
        self.currentPosition = [Grid.row + 1, int(Grid.column / 2 - 2)]
        second = self.ValidTransforamtion(self.currentPosition, self.currentState)
        if second:
            self.Update(1)
        else:
            raise ValueError("Can't spawn tetrominoe, Game is quitting...")    
        
    def Update(self, Set):
        '''
        Sets or clears current shape state and position in the grid\n
        Attributes:\n
            Set: 1 to set, 0 to clear
        '''
        gridRow = self.currentPosition[0]
        for stateRow in self.currentState:
            gridColumn = self.currentPosition[1]
            for stateColumn in stateRow:
                if stateColumn != 0:
                    if Set == 1:
                        self.grid[gridRow][gridColumn] = [1, (self.color)]
                    else:
                        self.grid[gridRow][gridColumn] = [0, (0, 0, 0)]
                        
                gridColumn += 1
            gridRow -= 1
    

    def Transform(self, key):
        '''
        takes user input or gravity input and tries to transform shape to new position and state
        '''
        self.Update(0) # clear previous state
        gridRow, gridColumn = self.currentPosition
        tempPos = [gridRow, gridColumn]
        tempState = self.currentState
        index = self.indexOfState
        if key == GLUT_KEY_RIGHT:
            tempPos = [gridRow, gridColumn + 1]
        if key == GLUT_KEY_LEFT:
            tempPos = [gridRow, gridColumn - 1]
        if key == GLUT_KEY_DOWN:
            tempPos = [gridRow - 1, gridColumn]
            
        if key == GLUT_KEY_UP:
            tempState = self.getState(1)
        if key == b'z':
            tempState = self.getState(0)
            
        valid = self.ValidTransforamtion(tempPos, tempState)
        if valid:
            self.currentState = tempState
            self.currentPosition = tempPos
        else:
            if key == GLUT_KEY_DOWN:
                self.locked = True
            self.indexOfState = index          # if rotation not valid, dont change index of state
        self.Update(1)
        return (self.locked, self.currentPosition)
         
        
    
    
    def getState(self, next):
        '''
        returns next or previous state\n
        Atributes:\n
            next: 1 for next, 0 for previous
        '''
        if next:
            self.indexOfState += 1
        else:
            self.indexOfState -= 1
        if self.indexOfState >= len(self.states):
            self.indexOfState = 0
        if self.indexOfState < 0:
            self.indexOfState = len(self.states) - 1
        return self.states[self.indexOfState]
    
    
    def ValidTransforamtion(self, position, state):
        '''
        indicates if Transformation is valid or not
        '''
        gridRow = position[0]
        for stateRow in state:
            gridColumn = position[1]
            for stateColumn in stateRow:
                if stateColumn != 0:
                    if gridColumn >= len(self.grid[0]) or gridColumn < 0 or gridRow < 0: # out of bound
                        return False
                    if self.grid[gridRow][gridColumn][0] == 1:     # ones collide
                        return False
                gridColumn += 1
            gridRow -= 1
        return True
    
    
    
    
    
    
    
    
    

class ITetrominoe(Shape):
    states = [
            [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 1, 0],                
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0]
            ],
            [
                [0, 1, 0, 0],                
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]
            ]
    ]
    color = (0.1, 0.9, 1)
    def __init__(self, Grid):
        super(ITetrominoe, self).__init__(Grid, self.states, self.color)
        
        
    # def Draw(self):
    #     super().Draw()
        
    
                    

class OTetrominoe(Shape):
    states = [
        [
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
    ]
    color = (1, .9, .2)
    def __init__(self, Grid):
        super(OTetrominoe, self).__init__(Grid, self.states, self.color)
        
    


class TTetrominoe(Shape):
    states = [
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
        ]
    color = (1, 0, .8)
    def __init__(self, Grid):
        super(TTetrominoe, self).__init__(Grid, self.states, self.color)
    
    
    
class JTetrominoe(Shape):
    states = [
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 1],
                [0, 1, 0],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0]
            ]
        ]
    color = (0, 0, 1)
    def __init__(self, Grid):
        super(JTetrominoe, self).__init__(Grid, self.states, self.color)



class LTetrominoe(Shape):
    states = [
            [
                [0, 0, 1],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 1]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [1, 0, 0]
            ],
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ]
        ]
    color = (1, .7, .2)
    def __init__(self, Grid):
        super(LTetrominoe, self).__init__(Grid, self.states, self.color)



class STetrominoe(Shape):
    states = [
            [
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 0, 0],
                [0, 1, 1],
                [1, 1, 0]
            ],
            [
                
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0]
                
            ]
        ]
    color = (0, 1, 0)
    def __init__(self, Grid):
        super(STetrominoe, self).__init__(Grid, self.states, self.color)
        
class ZTetrominoe(Shape):
    states = [
            [
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 0, 1],
                [0, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 0],
                [0, 1, 1]
            ],
            [
              [0, 1, 0],
              [1, 1, 0],
              [1, 0, 0]  
            ]
        ]
    color = (1, 0, 0)
    def __init__(self, Grid):
        super(ZTetrominoe, self).__init__(Grid, self.states, self.color)
        