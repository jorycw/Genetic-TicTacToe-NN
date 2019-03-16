from nn import Player
import numpy as np

class Population():

    def __init__(self):
        self.gen = np.array([Player() for i in range(100)])

    def get_pairs(self):
        arr = []
        for i in range(0, len(self.gen), 2):
            arr.append((self.gen[i], self.gen[i + 1]))
        return np.array(arr)

    def cull(self):
        self.gen = np.array()



if __name__ == '__main__':
    p = Population()
    print(p.gen)