from board import Board
from population import Population
import numpy as np
from tqdm import trange
from nn import Player

if __name__ == '__main__':

    computer = Player()
    computer.load_model('winner.model')

    board = Board()

    print('computer playing first')

    computer_turn = True

    while not board.is_over():
        if computer_turn:
            prob = computer(board.state)
            max_index = np.argmax(prob)
            max_index = max_index if isinstance(max_index, np.int64) else max_index[0]
            
            while (not board.is_valid(max_index)):
                prob[max_index] = 0
                max_index = np.argmax(prob)
                max_index = max_index if isinstance(max_index, np.int64) else max_index[0]

            board.apply_move(1, max_index)
            print('computer played in ',  max_index)

        else:
            move = int(input('your turn, input number between 0-8'))
            if not board.is_valid(move): 
                print('invalid input')
            print('you input ', move)
            board.apply_move(-1, move)

        print(board.to_string())
        computer_turn = not computer_turn

    res = board.winner()

    if res == 0:
        print('NN bot lost')
    elif res == 1:
        print('NN bot won')
    elif res == -1:
        print('NN bot lost')
