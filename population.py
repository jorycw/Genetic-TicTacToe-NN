from nn import Player
import numpy as np
import torch
from board import Board

class Population():
    """ Class to represent the current generation of neural networks

    """

    def __init__(self):
        self.gen = np.array([Player() for i in range(100)])
        self.first_gen = np.copy(self.gen)

    def get_pairs(self):
        """ Returns:
                list[list[Player]] : The current generation in pairwise tuples.

        """
        arr = []
        for i in range(0, len(self.gen), 2):
            arr.append((self.gen[i], self.gen[i + 1]))
        return np.array(arr)

    def cull(self):
        """ Culls the current generation, killing the bottom half
            of the generation in terms of score.

        """

        self.gen.sort()
        self.gen = self.gen[::-1]
        self.gen = self.gen[:50]


    def winner_based_cull(self):
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

        self.gen = np.append(self.gen, children)
        self.gen = np.append(self.gen, [Player() for i in range(10)])
        np.random.shuffle(self.gen)

    def eval(self):
        #### DELETE LATER ####
        def best_valid_move(board, weights):
            max_index = np.argmax(weights)
            max_index = max_index if isinstance(max_index, np.int64) else max_index[0]
            
            while (not board.is_valid(max_index)): # inf loop if all moves are invalid or prob is filled w/ 0s and is_valid(0) == false
                weights[max_index] = 0
                max_index = np.argmax(weights)
                max_index = max_index if isinstance(max_index, np.int64) else max_index[0]

            return max_index

        def eval_game(player1, player2):
            players = [player1, player2]
            turn = 0;
            board = Board()

            while not board.is_over():
                weights = players[turn % 2](board.state)
                
                best_move = best_valid_move(board, weights)

                board.apply_move((((turn + 1) % 2) * 2) - 1, best_move)
            
                turn += 1

            return 1 if board.winner() == 1 else 0 # 1 for player1 win, 0 otherwise

        win_percent = 0
        for player in self.gen:
            for i in self.first_gen:
                win_percent += eval_game(player, i)
        win_percent /= (len(self.gen) ** 2)
        return win_percent * 100




if __name__ == '__main__':
    # Testing population functions
    p = Population()
    p.gen[0].winner = True
    print(p.gen)
    p.cull()
    print(len(p.gen))
    p.breed()
    print(len(p.gen))








