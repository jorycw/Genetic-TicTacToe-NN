from nn import Player
import numpy as np
import torch

class Population():

    def __init__(self):
        self.gen = np.array([Player() for i in range(100)])

    def get_pairs(self):
        arr = []
        for i in range(0, len(self.gen), 2):
            arr.append((self.gen[i], self.gen[i + 1]))
        return np.array(arr)

    def cull(self):
        tied = [nn for nn in self.gen if nn.winner is None]
        self.gen = list(filter(lambda x: x.winner is True, self.gen))
        while len(self.gen) < 50:
            self.gen.append(tied.pop())

    def breed(self):
        if len(self.gen) == 100:
            pass
        children = []

        def make_child(nn1, nn2):
            child = Player()
            for key in nn1.state().keys():
                A = nn1.state()[key].numpy()
                B = nn2.state()[key].numpy()
                child.state_dict()[key].copy_(torch.tensor((A + B) / 2))
            return child

        while len(children) < 50:
            i = np.random.randint(len(self.gen), size=2)
            children.append(make_child(self.gen[i[0]], self.gen[i[1]]))

        self.gen = self.gen + children
        np.random.shuffle(self.gen)


if __name__ == '__main__':
    p = Population()
    p.gen[0].winner = True
    print(p.gen)
    p.cull()
    print(len(p.gen))
    p.breed()
    print(len(p.gen))








