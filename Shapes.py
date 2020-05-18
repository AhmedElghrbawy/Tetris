from OpenGL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self):
        self.states = []
        self.currentState = []
        self.color = (1, 0, 0)
        self.currentPosition =  [4, 5]  # top left Pos
    




class IShape(Shape):
    def __init__(self):
        super().__init__()
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
        self.color = (0.1, 0.8, 0.9)