import numpy as np

class Node:
    __num: int
    __x: float
    __y: float
    __loadX: float
    __loadY: float

    def __init__(self, x:float, y:float):
        self.__x = x
        self.__y = y
        self.__num = 0
        self.__loadX = 0
        self.__loadY = 0
        # print("A new node has been constructed.")
    # Setters
    def SetNumber(self, num:int):
        self.__num = num
    def SetPosition(self, x:float, y:float):
        self.__x = x
        self.__y = y
    def AddLoad(self, Force:float, theta:float):
        self.__loadX += Force*np.cos(theta)
        self.__loadY += Force*np.sin(theta)
    # Getters
    def GetX(self):
        return self.__x
    def GetY(self):
        return self.__y
    def GetNum(self):
        return self.__num
    def GetLoadX(self):
        return self.__loadX
    def GetLoadY(self):
        return self.__loadY
    # Printers
    def PrintNode(self):
        print("\n======================================================Node")
        print("The position of Node ", self.__num, " is (", self.__x, ",",self.__y, ").")
        print("The Force on the node is (", self.__loadX, ",", self.__loadY, ").")
        print("==========================================================\n")
