import pickle
import numpy as np
from colorama import Fore, Back, Style
from sklearn.neural_network import MLPRegressor, MLPClassifier
from itertools import product
import copy
import pickle

def abcd2num(char):
    if char in ['a', 'b', 'c', 'd']:
        d = {'a':10, 'b':11, 'c':12, 'd':13}
        return d[char]
    elif char in '0123456789':
        return int(char)
    else:
        return char

def num2abcd(num):
    if num in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        return num
    else:
        d = {10:'a', 11:'b', 12:'c', 13:'d'}
        return d[num]
    
class Alak:
    def __init__(self, moveX = 'random', moveO = 'random', print_result = False, clf=None):
        self.board = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, -1, -1, -1, -1, -1], dtype=np.int8)
        self.board_size = len(self.board)
        self.boards = []

        self.x_pos = np.asarray(self.board>0).nonzero()[0]
        self.__pos = np.asarray(self.board==0).nonzero()[0]
        self.o_pos = np.asarray(self.board<0).nonzero()[0]
        
        self.print_result = print_result
        self.moveX = moveX
        self.moveO = moveO
        
        self.clf = clf
        
    def update_location(self):
        self.x_pos = np.asarray(self.board>0).nonzero()[0]
        self.__pos = np.asarray(self.board==0).nonzero()[0]
        self.o_pos = np.asarray(self.board<0).nonzero()[0]
        
    def move(self, turn):
        if turn == 1:
            if self.moveX == 'interactive':
                original_loc, next_loc, capture = self.move_interactive(turn)
            if self.moveX == 'model':
                original_loc, next_loc, capture = self.move_model(turn)
            if self.moveX == 'random':
                original_loc, next_loc, capture = self.move_random(turn)
                
        else:
            if self.moveO == 'interactive':
                original_loc, next_loc, capture = self.move_interactive(turn)
            if self.moveO == 'model':
                original_loc, next_loc, capture = self.move_model(turn)
            if self.moveO == 'random':
                original_loc, next_loc, capture = self.move_random(turn)

        self.board[next_loc] = self.board[original_loc]
        self.board[original_loc] = 0

        self.update_location()

        if self.print_result:
            if turn == 1:
                print(Fore.WHITE + 'x : {}->{}'.format(num2abcd(original_loc), num2abcd(next_loc)))
            else:
                print(Fore.WHITE + 'o : {}->{}'.format(num2abcd(original_loc), num2abcd(next_loc)))
            
        return original_loc, next_loc, capture
    
    def get_ori_loc(self, turn):
        if turn == 1:
            pos = self.x_pos
            inputStr = 'x from: '
        else:
            pos = self.o_pos
            inputStr = 'o from: '
            
        original_loc = abcd2num(input(inputStr))
        while original_loc not in pos:
            print(Fore.WHITE + 'Invalid move: try again')
            original_loc = abcd2num(input(inputStr))
        return original_loc
    
    def get_next_loc(self):
        next_loc = int(abcd2num(input('move to: ')))
        while next_loc not in self.__pos:
            print(Fore.WHITE + 'Invalid move: try again')
            next_loc = abcd2num(input('move to: '))
        return next_loc
    
    def move_interactive(self, turn):
        original_loc = self.get_ori_loc(turn)
        next_loc = self.get_next_loc()

        b, capture = self.checkCapture(self.board, original_loc, next_loc, turn)
        if capture == 0 and self.isSuicide(original_loc, next_loc, turn):
            print(Fore.WHITE + '{}->{} is a suicide move'.format(num2abcd(original_loc), num2abcd(next_loc)))
            self.takeSuicide(original_loc, next_loc, turn)
            self.update_location()

        return original_loc, next_loc, capture
    
    def move_model(self, turn):
        clf = self.clf

        if turn == -1:
            # generate all kinds of board I can make after the input board
            moves = list(product(self.o_pos, self.__pos))

            # delete suicide moves
            dels = []
            for move in moves:
                b, capture = self.checkCapture(self.board, move[0], move[1], turn, change=False)
                if capture == 0 and self.isSuicide(move[0], move[1], turn):
                    dels.append(move)
            for d in dels:
                moves.remove(d)
                
            boards = []
            for move in moves:
                new_board = copy.deepcopy(self.board)
                new_board, capture = self.checkCapture(new_board, move[0], move[1], turn)
                new_board[move[1]] = new_board[move[0]]
                new_board[move[0]] = 0
                boards.append(np.append(np.append(self.board, 2), new_board))

            proba = clf.predict_proba(boards)
            max_idx = np.argmax(proba[:, 0])

        else:
            moves = list(product(self.x_pos, self.__pos))
            
            # delete suicide moves
            dels = []
            for move in moves:
                b, capture = self.checkCapture(self.board, move[0], move[1], turn, change=False)
                if capture == 0 and self.isSuicide(move[0], move[1], turn):
                    dels.append(move)
            for d in dels:
                moves.remove(d)
            
            probas = []
            for move in moves:
                new_board = copy.deepcopy(self.board)
                new_board, capture = self.checkCapture(new_board, move[0], move[1], turn)
                new_board[move[1]] = new_board[move[0]]
                new_board[move[0]] = 0
                
                __pos1 = np.asarray(self.board==0).nonzero()[0]
                o_pos1 = np.asarray(self.board<0).nonzero()[0]

                next_moves = list(product(__pos1, o_pos1))

                extended_boards = []
                for nm in next_moves:
                    next_board = copy.deepcopy(new_board)
                    next_board, capture = self.checkCapture(next_board, nm[0], nm[1], turn)
                    new_board[nm[1]] = new_board[nm[0]]
                    new_board[nm[0]] = 0
                    extended_boards.append(np.append(np.append(new_board, 2), next_board))

                proba = clf.predict_proba(extended_boards).sum(0)
                probas.append(proba)

            probas = np.array(probas)
            max_idx = np.argmax(probas[:, 1])
        
        original_loc, next_move = moves[max_idx][0], moves[max_idx][1]
        b, capture = self.checkCapture(self.board, original_loc, next_move, turn)
        self.update_location()
        return original_loc, next_move, capture
    
    def isSuicide(self, original_loc, next_move, turn):
        # EDGE
        if next_move == 0 or next_move == self.board_size - 1:
            return False
        
        # RIGHT
        right_enemy = False
        right = next_move + 1
        
        while right < self.board_size-1 and self.board[right] == turn:
            if right == original_loc:
                return False
            right += 1
            
        if self.board[right] == turn * -1:
            right_enemy = True

        # LEFT
        left_enemy = False
        left = next_move - 1
        
        while left > 0 and self.board[left] == turn:
            if left == original_loc:
                return False
            left -= 1
            
        if self.board[left] == turn * -1:
            left_enemy = True
        
        # BOTH
        if left_enemy and right_enemy:
            return True
        else:
            return False
        
    def takeSuicide(self, original_loc, next_move, turn):
        self.board[next_move] = 0
        self.board[original_loc] = 0
        # RIGHT
        right = next_move + 1

        while right < self.board_size-1 and self.board[right] == turn:
            self.board[right] = 0
            right += 1
            
        # LEFT
        left = next_move - 1

        while left > 0 and self.board[left] == turn:
            self.board[left] = 0
            left -= 1
    
    def checkCapture(self, board, original_loc, next_move, turn, change=True):
        capture = 0
        size = len(board)
        # capture left
        if next_move > 0:
            left = next_move - 1

            while left > 0 and board[left] == -1 * turn:
                left -= 1

            if board[left] == turn:
                if left == original_loc:
                    return board, 0
                for i in range(left+1, next_move):
                    if change:
                        board[i] = 0
                    capture += 1
                    
        if next_move < size - 1:
            right = next_move + 1

            while right < size-1 and board[right] == -1 * turn:
                right += 1

            if board[right] == turn:
                if right == original_loc:
                    return board, 0
                for i in range(next_move + 1, right):
                    if change:
                        board[i] = 0
                    capture += 1
        
        return board, capture
        
    def one_round(self):
        Board = np.zeros(self.board_size * 2 + 1, dtype=np.int8)
        
        # x move
        turn = 1
        original_loc, next_loc, gain = self.move(turn)
        
        board1 = self.board.copy()
        Board[:self.board_size] = board1
        Board[self.board_size] = 2
        
        if self.print_result:
            self.print_board(board1)
            if gain > 0:
                print(Fore.WHITE + 'gain:{}\n'.format(gain))
            else:
                print(Fore.BLUE + 'gain:{}\n'.format(gain))
        if self.won() == 1:
            if self.print_result:
                print(Fore.RED + "x won!")
            self.boards.append(Board)
            return original_loc, next_loc, gain
        
        # o move
        turn = -1
        original_loc, next_loc, gain = self.move(turn)
        
        board2 = self.board.copy()
        Board[self.board_size+1:] = board2

        if self.print_result:
            self.print_board(board2)
            if gain > 0:
                print(Fore.RED + 'gain:{}\n'.format(gain))
            else:
                print(Fore.BLUE + 'gain:{}\n'.format(gain))
            if self.won() == -1:
                print(Fore.RED + "o won!")
            
        self.boards.append(Board)
        
        return original_loc, next_loc, gain
        
    def won(self): # 1 -> x won, 0 -> keep playing, -> -1 -> o won
        if len(self.o_pos) <= 1:
            return 1
        elif len(self.x_pos) <= 1:
            return -1
        else:
            return 0
    
    def play(self):
        self.__init__(self.moveX, self.moveO, self.print_result, self.clf)
        
        if self.print_result:
            self.print_board(self.board)
        
        round_count = 0
        gain = 0
        while self.won() == 0:
            original_loc, next_loc, gain = self.one_round()
            round_count += 1
        
        # Need to be change
        suicide = False
        # gain
        old_position = original_loc
        new_position = next_loc
        board = self.board

        return suicide, gain, old_position, new_position, board, self.won()
    
    def print_board(self, Board):
        boardStr = ''.join([str(i) for i in Board])
        boardStr = boardStr.replace('0', '_').replace('-1', 'o').replace('1', 'x').replace('2', ' ')
        index = '0123456789abcd'
        print()
        print(Fore.WHITE + boardStr)
        print(Fore.WHITE + index)
        print()

def official_games(side):
    with open('my_training_model', 'rb') as file:
        clf = pickle.load(file)
    
    if side == 'x':
        game = Alak(moveX='model', moveO='interactive', print_result=True, clf=clf)
    elif side == 'o':
        game = Alak(moveX='interactive', moveO='model', print_result=True, clf=clf)

    game.play()
    
# official_games('o', clf)

def getJson(old, new):
    suicide = False
    captures = []
    old_position = 0
    new_position = 7
    board = []
    win = False
    jsonStr = jsonify({
            'suicide': suicide,
            'captured': captures,
            'olg_position': old_position,
            'new_position': new_position,
            'board': board,
            'win': win
    })
    return jsonStr