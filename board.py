class Board:
    def __init__(self):
        self.state = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def apply_move(self, player, pos):
        ''' applies given move by given player to board state

        Args:
            player (int in {-1, 1}) : player making move
            pos    (int in [0, 8])  : position of move being made
        '''
        self.state[pos] = player

    def is_valid(self, pos):
        ''' returns whether given position is valid choice of applyng a move

        Args:
            pos (int in [0, 8])  : position of move being made

        Returns:
            bool: the return value. True for valid, False otherwise
        '''
        return self.state[pos] == 0

    def is_over(self):
        ''' returns whether game in current board state is over

        Returns:
            bool: the return value. True for game is over, False otherwise
        '''
        return self.game_state_helper() != 2

    # return 0: tie, -1,1: winner
    def winner(self):
        ''' returns winner of current game state

        Returns:
            int: the return value. 1 for player1, -1 for player2, 0 for tie
        '''
        return self.game_state_helper()

    def to_string(self):
        ''' returns current board state in string format

        Returns:
            String: the return value. format: O for player1, X for player2, - for open space 
        '''
        tmp = []
        for i in range(len(self.state)):
            if self.state[i] == 1:
                tmp.append('O')
            elif self.state[i] == -1:
                tmp.append('X')
            else:
                tmp.append('-')
        return f'\n{tmp[0]}{tmp[1]}{tmp[2]}\n{tmp[3]}{tmp[4]}{tmp[5]}\n{tmp[6]}{tmp[7]}{tmp[8]}'

################################## helpers ####################################

    # HELPER # return: -1: -1 won, 1: 1 won, 0: tie, 2: game not over
    def game_state_helper(self):
        # horizontal + vertical
        for i in range(3):
            for player in [-1, 1]:
                if self.state[0 + (3 * i)] == player and \
                   self.state[1 + (3 * i)] == player and \
                   self.state[2 + (3 * i)] == player:
                    return player
                if self.state[0 + i] == player and \
                   self.state[3 + i] == player and \
                   self.state[6 + i] == player:
                    return player
        # diags
        for player in [-1, 1]:
            if self.state[0] == player and \
               self.state[4] == player and \
               self.state[8] == player:
                return player
            if self.state[2] == player and \
               self.state[4] == player and \
               self.state[6] == player:
                return player
        # tie
        for i in range(len(self.state)):
            if self.state[i] == 0: return 2
        return 0

################################### testing ######################################

def test():
    player = [1, -1, 1, -1, 1]
    pos = [0, 8, 6, 4, 3]
    b = Board()

    for i in range(5):
        if b.is_over(): print('is_over = True')
        if not b.is_valid(pos[i]): print('is_valid = False')
        b.apply_move(player[i], pos[i])
        print(b.to_string())

    if not b.is_over(): print('is_over = False')
    print('\nwinner = ',b.winner(), '\n')

if __name__ == '__main__':
    test()