from board import Board
from population import Population
import numpy as np
from tqdm import trange

POP_SIZE = 100
WEIGHTS = [-1, 1, 2] # [loss, tie, win]

def best_valid_move(board, weights):
	max_index = np.argmax(weights)
	max_index = max_index if isinstance(max_index, np.int64) else max_index[0]
			
	while (not board.is_valid(max_index)): # inf loop if all moves are invalid or prob is filled w/ 0s and is_valid(0) == false
		weights[max_index] = 0
		max_index = np.argmax(weights)
		max_index = max_index if isinstance(max_index, np.int64) else max_index[0]

	return max_index


def play_game(player1, player2):
	players = [player1, player2]
	turn = 0;
	board = Board()

	while not board.is_over():
		weights = players[turn % 2](board.state)
		
		best_move = best_valid_move(board, weights)

		board.apply_move((((turn + 1) % 2) * 2) - 1, best_move)
	
		turn += 1

	res = board.winner()
	set_player_results(players[0], res)
	set_player_results(players[1], res * -1)

def set_player_results(player, res):
	if res == 0:
		player.winner = None
	else:
		player.winner = (res == 1)

def elim_pop_to_winner(pop):
	pair = [pop.gen.pop(), pop.gen.pop()]

	while len(pair) == 2:
		play_game(pair[0], pair[1])
		if (pair):
			pair.pop(0)
		else:
			pair.pop(1)

		if len(pop.gen) != 0:
			pair.append(pop.gen.pop())

	return pair[0]


def unparallized_train(output_fn, epoch=1000):
	pop = Population()
	for e in trange(epoch):

		pop.breed()
		for pair in pop.get_pairs():
			play_game(pair[0], pair[1])

		pop.cull()
	elim_pop_to_winner(pop).save_model(output_fn)


if __name__ == '__main__':
	unparallized_train('winner.model')

