from OpenGL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Grid import Grid
from abc import ABC

class Shape(ABC):
    def __init__(self, Grid, states, color):
        self.currentPosition =  [10, 5]  # top left Pos
        self.grid = Grid.grid
        self.states = states
        self.indexOfState = 0    # declares the index of current state
        self.currentState = states[self.indexOfState]
        self.color = color
        self.Update(1) 
        
        
    def Update(self, Set):
        '''
        Sets or clears current state and position in the grid\n
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
    

    def Transforme(self, key):
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
            self.indexOfState = index          # if rotation not valid, dont change index of state
        self.Update(1)
         
        
    
    
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
        gridRow = position[0]
        for stateRow in state:
            gridColumn = position[1]
            for stateColumn in stateRow:
                if stateColumn != 0:
                    if gridColumn >= len(self.grid[0]) or gridColumn < 0 or gridRow < 0: # out of bound
                        return False
                    if self.grid[gridRow][gridColumn] == 1:     # ones collide
                        return False
                gridColumn += 1
            gridRow -= 1
        return True
    
    
    
    
    
    
    
    
    

class ITetrominoe(Shape):
    def __init__(self, Grid):
        self.states = [
                [
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
                [
                    [0, 1, 0, 0],                
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0]
                ],
                [
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0]
                ],
                [
                    [0, 0, 1, 0],                
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0]
                ]
        ]
        self.color = (0.1, 0.9, 1)
        super(ITetrominoe, self).__init__(Grid, self.states, self.color)
        
        
    # def Draw(self):
    #     super().Draw()
        
    
                    

class OTetrominoe(Shape):
    def __init__(self, Grid):
        self.states = [
            [
                [1, 1],
                [1, 1]
            ]
        ]
        self.color = (1, .9, .2)
        super(OTetrominoe, self).__init__(Grid, self.states, self.color)
        
    


class TTetrominoe(Shape):
    def __init__(self, Grid):
        self.states = [
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
        self.color = (1, 0, .8)
        super(TTetrominoe, self).__init__(Grid, self.states, self.color)
    
    
    
class JTetrominoe(Shape):
    def __init__(self, Grid):
        self.states = [
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
        self.color = (0, 0, 1)
        super(JTetrominoe, self).__init__(Grid, self.states, self.color)



class LTetrominoe(Shape):
    def __init__(self, Grid):
        self.states = [
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
        self.color = (1, .7, .2)
        super(LTetrominoe, self).__init__(Grid, self.states, self.color)



class STetrominoe(Shape):
    def __init__(self, Grid):
        self.states = [
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
        self.color = (0, 1, 0)
        super(STetrominoe, self).__init__(Grid, self.states, self.color)
        
class ZTetrominoe(Shape):
    def __init__(self, Grid):
        self.states = [
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
        self.color = (1, 0, 0)
        super(ZTetrominoe, self).__init__(Grid, self.states, self.color)
        