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
        self.currentState = states[0]
        self.color = color
        self.Draw() 
        
        
    def Draw(self):
        gridRow = self.currentPosition[0]
        for stateRow in self.currentState:
            gridColumn = self.currentPosition[1]
            for stateColumn in stateRow:
                if stateColumn != 0:
                    self.grid[gridRow][gridColumn] = [1, (self.color)]
                gridColumn += 1
            gridRow -= 1
    




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
                [
                    [1, 0, 0],
                    [1, 1, 0],
                    [0, 1, 0]
                ]
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
        