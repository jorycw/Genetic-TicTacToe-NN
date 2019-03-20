from board import Board
from population import Population
import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt
from multiprocessing import Process

POP_SIZE = 100
WEIGHTS = [-1, 0, 1] # [loss, tie, win]

EVAL_VS_FIRST_GEN = []

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
		player = (((turn + 1) % 2) * 2) - 1 ## player = 1 for player 1, -1 for player 2
		bd = board.state[:]
		if turn % 2 == 1:
			bd = [x * -1 for x in bd]

		weights = players[turn % 2](bd) ## flips the board for player two
		best_move = best_valid_move(board, weights)
		board.apply_move(player, best_move)
		turn += 1

	res = board.winner()
	set_player_results(players[0], res)
	set_player_results(players[1], res * -1)

def set_player_results(player, res):
	'''
	if res == 0:
		player.winner = None
	else:
		player.winner = (res == 1)
	'''
	if res == -1:
		player.update_score(WEIGHTS[0])
	elif res == 0:
		player.update_score(WEIGHTS[1])
	else:
		player.update_score(WEIGHTS[2])

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

def gen_pairs_play(pop):
	for pair in pop.get_pairs():
			 play_game(pair[0], pair[1])


def unparallized_train(output_fn, epoch=1001, games_per_gen=5):
	pop = Population()

	breed = []
	game = []
	pop1 = []


	for e in trange(epoch):
		pop.breed()

		if e % 50 == 0:
			EVAL_VS_FIRST_GEN.append(pop.eval())

#		processes = []

		for i in range(games_per_gen):
#			p = Process(target=gen_pairs_play, args=(pop,))
#			p.start()
#			processes.append(p)
			gen_pairs_play(pop)

#		for p in processes:
#			p.join()




		pop.cull()

	#elim_pop_to_winner(pop).save_model(output_fn)


if __name__ == '__main__':
	unparallized_train('winner.model')

	X = range(len(EVAL_VS_FIRST_GEN))
	Y = EVAL_VS_FIRST_GEN
	Y_win = []
	Y_wintie = []
	for i in Y:
		Y_win.append(i[0])
		Y_wintie.append(i[1])

	plt.plot(X, Y_win)
	plt.plot(X, Y_wintie)
	plt.savefig("wins_vs_iteration")
	plt.show()




