import numpy as np
class Tools:
    def __init__(self):
        print("costruttore")
    
    def MSE(self,l,p):
        return np.mean((l-p) ** 2)
