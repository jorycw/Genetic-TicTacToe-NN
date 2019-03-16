from board import Board
from population import Population
import numpy as np

if __name__ == '__main__':

	pop = Population()

	for pair in pop.get_pairs():

		board = Board()
		player = 1

		while (not board.is_over()):
			prob = pair[player](board.)
