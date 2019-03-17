from nn import Player
import numpy as np
import torch

class Population():
    """ Class to represent the current generation of neural networks

    """

    def __init__(self):
        self.gen = np.array([Player() for i in range(100)])

    def get_pairs(self):
        """ Returns:
                list[list[Player]] : The current generation in pairwise tuples.

        """
        arr = []
        for i in range(0, len(self.gen), 2):
            arr.append((self.gen[i], self.gen[i + 1]))
        return np.array(arr)

    def cull(self):
        """ Culls the current generation, killing all losing players.
            If there were draws, selects enough tying players to fill
            the current generation up to half capacity.

        """

        tied = [nn for nn in self.gen if nn.winner is None]
        self.gen = list(filter(lambda x: x.winner is True, self.gen))
        while len(self.gen) < 50:
            self.gen.append(tied.pop())

    def breed(self):
        """ Repopulates the current generation through breeding of
            pairs of random players.

        """

        if len(self.gen) == 100:
            return
        children = []

        def make_child(nn1, nn2):
            """ Breeds two neural network players.

                Returns:
                    Player: A new neural network Player object formed from the 
                            result of averaging all weights and biases of the 
                            parents neural networks.

            """

            child = Player()
            for key in nn1.state().keys():
                A = nn1.state()[key].numpy()
                B = nn2.state()[key].numpy()
                child.state_dict()[key].copy_(torch.tensor((A + B) / 2))
            return child

        while len(children) < 40:
            i = np.random.randint(len(self.gen), size=2)
            children.append(make_child(self.gen[i[0]], self.gen[i[1]]))

        self.gen = self.gen + children
        self.gen = self.gen + [Player() for i in range(10)]
        np.random.shuffle(self.gen)


if __name__ == '__main__':
    # Testing population functions
    p = Population()
    p.gen[0].winner = True
    print(p.gen)
    p.cull()
    print(len(p.gen))
    p.breed()
    print(len(p.gen))








