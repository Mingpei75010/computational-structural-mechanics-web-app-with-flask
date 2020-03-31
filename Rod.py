import numpy as np
from Node import Node

class Rod:
    __num: int
    __leftNode: Node
    __rightNode: Node
    __youngsModulus: float
    __crossSection: float

    def __init__(self, nodeL:Node, nodeR:Node):
        self.__leftNode = nodeL
        self.__rightNode = nodeR
        self.__num = 0
        self.__youngsModulus = 20000000000.0;
        self.__crossSection = 0.24
    # Setters
    def SetNum(self, num:int):
        self.__num = num
    def SetRod(self, nodeL:Node, nodeR:Node):
        self.__leftNode = nodeL
        self.__rightNode = nodeR
    def SetE(self, E:float):
        self.__youngsModulus = E;
    def SetA(self, A:float):
        self.__crossSection = A;
    # Printers
    def PrintRod(self):
        print("\n=======================================================Rod")
        print("The left node is", self.__leftNode.GetNum(),
              ", and the right node is", self.__rightNode.GetNum(),".")
        print("Number is", self.__num)
        print("E = ", self.__youngsModulus, ", A = ", self.__crossSection)
        print("==========================================================\n")
    # Calculation
    def CalLength(self):
        xDis = self.__rightNode.GetX() - self.__leftNode.GetX()
        yDis = self.__rightNode.GetY() - self.__leftNode.GetY()
        return np.sqrt(np.power(xDis,2)+np.power(yDis,2))
    def CalCos(self):
        return (self.__rightNode.GetX() - self.__leftNode.GetX())/self.CalLength()
    def CalSin(self):
        return (self.__rightNode.GetY() - self.__leftNode.GetY())/self.CalLength()
    def Calrd(self):
        return self.__youngsModulus*self.__crossSection/self.CalLength()
    def CalStif(self):
        di = 2  # Dimension of the matrix and the vector
        # Initialize
        c = []
        t = []
        for i in range(di):
            c.append([])
            t.append(0.0)
            for j in range(di):
                c[i].append(0.0)
        c = np.array(c)
        t[0] = self.CalCos()
        t[1] = self.CalSin()
        t = np.array(t)
        for i in range(di):
            for j in range(di):
                c[i][j]=t[i]*t[j]*self.Calrd()
        return c
    def Cali0j0(self, nc:int):
        i0 = []
        i0.append(2*(self.__leftNode.GetNum()-nc))
        i0.append(2*(self.__rightNode.GetNum()-nc))
        i0 = np.array(i0)
        return i0
