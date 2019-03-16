from board import Board
from population import Population
import numpy as np
from tqdm import trange

if __name__ == '__main__':

	epoch = 500

	pop = Population()
	for e in trange(epoch):

		pop.breed()
		for pair in pop.get_pairs():

			board = Board()
			player = 1

			while (not board.is_over()):
				prob = pair[player](board.state)
				max_index = np.argmax(prob)[0]
				
				while (not board.is_valid(max_index)): # inf loop if all moves are invalid or prob is filled w/ 0s and is_valid(0) == false
					prob[max_index] = 0
					max_index = np.argmax(prob)[0]

				board.apply_move(player, max_index)
				player = player * -1

			res = board.winner()

			if res != 0:
				pair[(res - 1) // (-2)].winner = True
				pair[(res + 1) //   2 ].winner = False
			else:
				pair[0].winner = None
				pair[1].winner = None

		pop.cull()
		
	pop.gen[0].save_model('winner.model')

