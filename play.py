from board import Board
from population import Population
import numpy as np
from tqdm import trange
from nn import Player

if __name__ == '__main__':

    computer = Player()
    computer.load_model('winner.model')

    board = Board()

    print('computer goes first cuz hes not very smart')

    computer_turn = True

    while not board.is_over():
        if computer_turn:

            prob = computer(board.state)
            max_index = np.argmax(prob)
            max_index = max_index if isinstance(max_index, np.int64) else max_index[0]
            
            while (not board.is_valid(max_index)): # inf loop if all moves are invalid or prob is filled w/ 0s and is_valid(0) == false
                prob[max_index] = 0
                max_index = np.argmax(prob)
                max_index = max_index if isinstance(max_index, np.int64) else max_index[0]

            board.apply_move(1, max_index)
            print('computer played in ',  max_index)

        else:

            move = int(input('your turn, input number between 0-8'))
            if not board.is_valid(move): print('youre dum')
            print('you input ', move)
            board.apply_move(-1, move)

        print(board.to_string())
        computer_turn = not computer_turn

    res = board.winner()

    if res == 0:
        print('you couldnt beat a tictactoe bot made with 3 lines of code')
    elif res == 1:
        print('you lost to a tictactoe bot made with 3 lines of code')
    elif res == -1:
        print('nice! you beat a tictactoe bot made with 3 lines of code!')
    else:
        print('somebody screwed up their board.winner() method')