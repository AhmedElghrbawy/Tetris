from OpenGL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Grid import Grid

class Shape():
    def __init__(self, Grid, states, color):
        self.currentPosition =  [Grid.row - 2, int(Grid.column / 2 - 2)]  # top left Pos # intial is at row 21 (index 20)
        self.grid = Grid.grid
        self.states = states
        self.indexOfState = 0    # declares the index of current state
        self.currentState = states[self.indexOfState]
        self.color = color
        self.locked = False
        self.Spawn() 
        
    def Spawn(self):
        '''
        try to spawn in row 21. if fail try row 22. if both fails, game ends
        '''
        first = self.ValidTransforamtion(self.currentPosition, self.currentState)  # first attempt
        if first:
            self.Update(1)
            return
        self.currentPosition = [Grid.row - 1, int(Grid.column / 2 - 2)] # second attempt
        second = self.ValidTransforamtion(self.currentPosition, self.currentState)
        if second:
            self.Update(1)
        else:
            raise ValueError("Can't spawn tetrominoe")    
        
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
    
    def HandleInput(self, key):
        gridRow, gridColumn = self.currentPosition
        tempPos = [gridRow, gridColumn]  # try tempPos as possible next position
        tempState = self.currentState    # try temps state as possible next state
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
        if key == b' ':  # hard drop
            while True:  # simulate key down input untill shape is locked
                self.HandleInput(GLUT_KEY_DOWN)
                if self.locked == True:
                    return (self.locked, self.currentPosition)

        return self.Transform(key, tempPos, tempState)

        

    def Transform(self, key, tempPos, tempState):
        '''
        tries to transform shape to new position and state
        '''
        self.Update(0) # clear previous state
        index = self.indexOfState 
        valid = self.ValidTransforamtion(tempPos, tempState)
        if valid:
            self.currentState = tempState
            self.currentPosition = tempPos
        else:
            if key == GLUT_KEY_DOWN:  # if last input was key down and transformation is invalid, lock shape
                self.locked = True
            self.indexOfState = index          # if Transformation not valid, dont change index of state
        self.Update(1)
        return (self.locked, self.currentPosition)
         
    def GetGhost(self):
        tempPos = self.currentPosition
        self.Update(0)
        while self.ValidTransforamtion(tempPos, self.currentState):
            tempPos = [tempPos[0] - 1, tempPos[1]]
        tempPos = [tempPos[0] + 1, tempPos[1]]
        self.Update(1)
        return (tempPos, self.currentState)         
    
    
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
        