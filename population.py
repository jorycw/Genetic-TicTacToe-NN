from nn import Player
import numpy as np

class Population():

    def __init__(self):
        self.gen = np.array([Player() for i in range(100)])

    def get_pairs(self):
        pass



if __name__ == '__main__':
    p = Population()
    print(p.gen[0].weights()['fc1.weight'])
    print()
    print(p.gen[1].weights()['fc1.weight'])
    print()
    print(p.gen[2].weights()['fc1.weight'])
