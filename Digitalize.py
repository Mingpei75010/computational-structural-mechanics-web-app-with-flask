import numpy as np
from Node import Node
from Rod import Rod

def SetBasicData(n: int, m: int , nc: int, nForce: int):
    baseData = [n, m, nc, nForce]
    baseData = np.array(baseData)
    return baseData

def SetNodes(x:float, y:float):
    tempNode = Node(x, y)
    return tempNode

def SetRods(left:Node, right:Node):
    tempRod = Rod(left, right)
    return tempRod

def SetForces(force:float, theta:float, node:Node):
    node.AddLoad(force, theta)