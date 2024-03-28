import copy


class Figure:

    def __init__(self, pos: str, color: str):
        self.pos = pos
        self.color = color

    def calculate_possible_moves(self, field: dict) -> list:
        """
        Метод просчитывает все возможные ходы для данной фигуры.
        :param field: игровое поле (словарь)
        :return: список возможных позиций фигуры после хода
        """
        pass

    def step(self, field: dict, move: str) -> (dict, str):
        """
        Метод перемещения фигуры на указанную клетку
        :param field: игровое поле (словарь)
        :param move: на какую клетку сходить
        :return: (поле после хода, цвет следующего игрока)
        """
        if field[self.pos[0]][''.join([i for i in self.pos if i.isdigit()])].__str__() in 'Kk' and move in ['C8', 'C1', 'G8', 'G1'] and ('0-0' in self.calculate_possible_moves(field) or '0-0-0' in self.calculate_possible_moves(field)):
            if move == 'C8':
                field['C']['8'] = 'k'
                field['D']['8'] = 'r'
                field['A']['8'] = ' '
                field['E']['8'] = ' '
                moves.append('0-0-0')
            if move == 'C1':
                field['C']['1'] = 'K'
                field['D']['1'] = 'R'
                field['A']['1'] = ' '
                field['E']['1'] = ' '
                moves.append('0-0-0')
            if move == 'G8':
                field['G']['8'] = 'k'
                field['F']['8'] = 'r'
                field['H']['8'] = ' '
                field['E']['8'] = ' '
                moves.append('0-0')
            if move == 'G1':
                field['G']['1'] = 'K'
                field['F']['1'] = 'R'
                field['H']['1'] = ' '
                field['E']['1'] = ' '
                moves.append('0-0')
        else:
            if not isinstance(field[move[0]][''.join([i for i in move if i.isdigit()])], Pawn):
                eaten_temp = field[move[0]][''.join([i for i in move if i.isdigit()])].__str__()
            else:
                eaten_temp = ''
            if not isinstance(self, Pawn):
                temp = self.__str__()
            else:
                temp = ''
            if field[move[0]][''.join([i for i in move if i.isdigit()])] == ' ':
                moves.append((temp+self.pos+'-'+eaten_temp+move).replace(' ',''))
            else:
                moves.append((temp+self.pos + ':' + eaten_temp+move).replace(' ', ''))
            field[self.pos[0]][''.join([i for i in self.pos if i.isdigit()])] = ' '
            field[move[0]][''.join([i for i in move if i.isdigit()])] = ' '
            self.pos = move
            field[move[0]][''.join([i for i in move if i.isdigit()])] = self

        return field, 'White' if self.color == 'Black' else 'Black'


class Pawn(Figure):

    def __init__(self, pos: str, color: str):
        super().__init__(pos, color)

    def calculate_possible_moves(self, field):
        possible_moves = []
        if self.color == 'White':
            temp = 1 if len(field['A']) == 8 else 2
        else:
            temp = -1 if len(field['A']) == 8 else -2
        try:
            if field[self.pos[0]][str(int(''.join([i for i in self.pos if i.isdigit()])) + temp)] == ' ':
                possible_moves.append(self.pos[0] + str(int(''.join([i for i in self.pos if i.isdigit()])) + temp))
        except (KeyError, IndexError):
            pass
        try:
            if field[ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) - 1]][str(int(''.join([i for i in self.pos if i.isdigit()])) + (1 if self.color =='White' else -1))].__str__() in ChessGame.figures[(1 if self.color =='White' else -1) * (-1)] and ChessGame.alphabet.index(self.pos[0]) - 1 >= 0:
                possible_moves.append(ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) - 1] + str(int(''.join([i for i in self.pos if i.isdigit()])) + (1 if self.color =='White' else -1)))
        except (KeyError, IndexError):
            pass
        try:
            if field[ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + 1]][str(int(''.join([i for i in self.pos if i.isdigit()])) + (1 if self.color =='White' else -1))].__str__() in ChessGame.figures[(1 if self.color =='White' else -1) * (-1)] and ChessGame.alphabet.index(self.pos[0]) + 1 <= 8:
                possible_moves.append(ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + 1] + str(int(''.join([i for i in self.pos if i.isdigit()]))  + (1 if self.color =='White' else -1)))
        except (KeyError, IndexError):
            pass
        try:
            if not (any([self.pos in move for move in moves])) and field[self.pos[0]][str(int(''.join([i for i in self.pos if i.isdigit()])) + (2*temp))] == ' ' and field[self.pos[0]][str(int(''.join([i for i in self.pos if i.isdigit()])) + temp)] == ' ':
                possible_moves.append(self.pos[0] + str(int(''.join([i for i in self.pos if i.isdigit()])) + (2*temp)))
        except (KeyError, IndexError):
            pass
        return possible_moves

    def __str__(self):
        return 'P' if self.color == 'White' else 'p'


class Rook(Figure):

    def __init__(self, pos: str, color: str):
        super().__init__(pos, color)

    def calculate_possible_moves(self, field):
        temp = 1 if len(field['A'].keys()) == 8 else 2
        possible_moves = []
        for index in range(int(''.join([i for i in self.pos if i.isdigit()])) + temp, len(field['A'].keys())+1, temp):
            if field[self.pos[0]][str(index)] == ' ':
                possible_moves.append(self.pos[0] + str(index))
            elif field[self.pos[0]][str(index)].__str__() in ChessGame.figures['All'] and field[self.pos[0]][str(index)].__str__() not in ChessGame.figures[self.color]:
                possible_moves.append(self.pos[0] + str(index))
                break
            else:
                break
        for index in range(int(''.join([i for i in self.pos if i.isdigit()])) - temp, 0, temp*(-1)):
            if field[self.pos[0]][str(index)] == ' ':
                possible_moves.append(self.pos[0] + str(index))
            elif field[self.pos[0]][str(index)].__str__() in ChessGame.figures['All'] and field[self.pos[0]][str(index)].__str__() not in ChessGame.figures[self.color]:
                possible_moves.append(self.pos[0] + str(index))
                break
            else:
                break
        for index in range(ChessGame.alphabet.index(self.pos[0])+temp, 8, temp):
            if field[ChessGame.alphabet[index]][''.join([i for i in self.pos if i.isdigit()])].__str__() == ' ':
                possible_moves.append(ChessGame.alphabet[index] + ''.join([i for i in self.pos if i.isdigit()]))
            elif field[ChessGame.alphabet[index]][''.join([i for i in self.pos if i.isdigit()])].__str__() in ChessGame.figures['All'] and field[ChessGame.alphabet[index]][''.join([i for i in self.pos if i.isdigit()])].__str__() not in ChessGame.figures[self.color]:
                possible_moves.append(ChessGame.alphabet[index] + ''.join([i for i in self.pos if i.isdigit()]))
                break
            else:
                break
        for index in range(ChessGame.alphabet.index(self.pos[0]) - temp, -1, -1*temp):
            if field[ChessGame.alphabet[index]][''.join([i for i in self.pos if i.isdigit()])].__str__() == ' ':
                possible_moves.append(ChessGame.alphabet[index] +''.join([i for i in self.pos if i.isdigit()]))
            elif field[ChessGame.alphabet[index]][''.join([i for i in self.pos if i.isdigit()])].__str__() in ChessGame.figures['All'] and field[ChessGame.alphabet[index]][''.join([i for i in self.pos if i.isdigit()])].__str__() not in ChessGame.figures[self.color]:
                possible_moves.append(ChessGame.alphabet[index] + ''.join([i for i in self.pos if i.isdigit()]))
                break
            else:
                break
        return possible_moves

    def __str__(self):
        return 'R' if self.color == 'White' else 'r'


class Knight(Figure):

    def __init__(self, pos: str, color: str):
        super().__init__(pos, color)

    def calculate_possible_moves(self, field):
        vectors = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        if len(field['A'].keys()) != 8:
            vectors = [(i[0],i[1]*2+(1 if i[1]> 0 else -1)) for i in vectors if abs(i[0]) == 1] + [(i[0]*2+(1 if i[0]> 0 else -1),i[1]) for i in vectors if abs(i[0]) == 2]
        possible_moves = []
        for vector in vectors:
            try:
                if field[ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + vector[0]]][str(int(''.join([i for i in self.pos if i.isdigit()])) + vector[1])] == ' ':
                    possible_moves.append(ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + vector[0]] + str(int(''.join([i for i in self.pos if i.isdigit()])) + vector[1]))
                elif field[ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + vector[0]]][str(int(''.join([i for i in self.pos if i.isdigit()])) + vector[1])].__str__() in ChessGame.figures['All'] and \
                        field[ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + vector[0]]][str(int(''.join([i for i in self.pos if i.isdigit()])) + vector[1])].__str__() not in ChessGame.figures[self.color]:
                    possible_moves.append(ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + vector[0]] + str(int(''.join([i for i in self.pos if i.isdigit()])) + vector[1]))
            except (KeyError, IndexError):
                pass
        return possible_moves

    def __str__(self):
        return 'N' if self.color == 'White' else 'n'


class Bishop(Figure):

    def __init__(self, pos: str, color: str):
        super().__init__(pos, color)

    def calculate_possible_moves(self, field):
        possible_moves = []
        temp = 1 if len(field['A'].keys()) == 8 else 2
        try:
            for pos in enumerate(ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + 1:], int(''.join([i for i in self.pos if i.isdigit()])) + 1):
                if field[pos[-1]][str(pos[0])] == ' ':
                    possible_moves.append(pos[-1] + str(pos[0]))
                elif field[pos[-1]][str(pos[0])].__str__() in ChessGame.figures['All'] and field[pos[-1]][str(pos[0])].__str__() not in ChessGame.figures[self.color]:
                    possible_moves.append(pos[-1] + str(pos[0]))
                    break
                else:
                    break
        except (KeyError, IndexError):
            pass
        try:
            for pos in enumerate(ChessGame.alphabet[:ChessGame.alphabet.index(self.pos[0])][::-1], int(''.join([i for i in self.pos if i.isdigit()])) + 1):
                if field[pos[-1]][str(pos[0])] == ' ':
                    possible_moves.append(pos[-1] + str(pos[0]))
                elif field[pos[-1]][str(pos[0])].__str__() in ChessGame.figures['All'] and field[pos[-1]][str(pos[0])].__str__() not in ChessGame.figures[self.color]:
                    possible_moves.append(pos[-1] + str(pos[0]))
                    break
                else:
                    break
        except (KeyError, IndexError):
            pass
        try:
            for pos in enumerate(ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + 1:], int(''.join([i for i in self.pos if i.isdigit()])) - 1):
                number = pos[0]
                if number > int(''.join([i for i in self.pos if i.isdigit()])) - 1:
                    number = (int(''.join([i for i in self.pos if i.isdigit()])) + int(int(''.join([i for i in self.pos if i.isdigit()])) - 2)) - pos[0]
                if field[pos[-1]][str(number)] == ' ':
                    possible_moves.append(pos[-1] + str(number))
                elif field[pos[-1]][str(number)].__str__() in ChessGame.figures['All'] and field[pos[-1]][str(number)].__str__() not in ChessGame.figures[self.color]:
                    possible_moves.append(pos[-1] + str(number))
                    break
                else:
                    break
        except (KeyError, IndexError):
            pass
        try:
            for pos in enumerate(ChessGame.alphabet[:ChessGame.alphabet.index(self.pos[0])][::-1], int(''.join([i for i in self.pos if i.isdigit()])) - 1):
                number = pos[0]
                if number > int(''.join([i for i in self.pos if i.isdigit()])) - 1:
                    number = (int(''.join([i for i in self.pos if i.isdigit()])) + int(int(''.join([i for i in self.pos if i.isdigit()])) - 2)) - pos[0]
                if field[pos[-1]][str(number)] == ' ':
                    possible_moves.append(pos[-1] + str(number))
                elif field[pos[-1]][str(number)].__str__() in ChessGame.figures['All'] and field[pos[-1]][str(number)].__str__() not in ChessGame.figures[self.color]:
                    possible_moves.append(pos[-1] + str(number))
                    break
                else:
                    break
        except (KeyError, IndexError):
            pass

        return possible_moves

    def __str__(self):
        return 'B' if self.color == 'White' else 'b'


class Queen(Figure):

    def __init__(self, pos: str, color: str):
        super().__init__(pos, color)

    def calculate_possible_moves(self, field):
        return Rook(self.pos, self.color).calculate_possible_moves(field)+Bishop(self.pos,self.color).calculate_possible_moves(field)

    def __str__(self):
        return 'Q' if self.color == 'White' else 'q'


class King(Figure):

    def __init__(self, pos: str, color: str):
        super().__init__(pos, color)

    def calculate_possible_moves(self, field):
        possible_moves = []
        for first in range(-1, 2):
            for second in range(-1, 2):
                try:
                    if field[ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + first]][str(int(''.join([i for i in self.pos if i.isdigit()])) + second)] == ' ':
                        possible_moves.append(ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + first] + str(int(''.join([i for i in self.pos if i.isdigit()])) + second))
                    elif field[ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + first]][str(int(''.join([i for i in self.pos if i.isdigit()])) + second)].__str__() in ChessGame.figures['All'] and field[ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + first]][str(int(''.join([i for i in self.pos if i.isdigit()])) + second)].__str__() not in ChessGame.figures[self.color]:
                        possible_moves.append(ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + first] + str(int(''.join([i for i in self.pos if i.isdigit()])) + second))
                except (KeyError, IndexError):
                    pass
        possible_moves += (ChessGame.check_castling(field, self.color))
        return possible_moves

    def __str__(self):
        return 'K' if self.color == 'White' else 'k'


class Infantry(Figure):

    def __init__(self, pos, color):
        super().__init__(pos, color)

    def calculate_possible_moves(self, field: dict) -> list:
        possible_moves = []
        vectors = [(0,1), (-1,1),(1,1)] if self.color == 'White' else [(0, -1), (-1,-1), (1,-1)]
        enemy_color = 'Black' if self.color == 'White' else 'White'
        for vector in vectors:
            try:
                if ChessGame.alphabet.index(self.pos[0]) + vector[0]>=0 and field[ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + vector[0]]][str(int(''.join([i for i in self.pos if i.isdigit()])) + vector[1])].__str__() in ''.join([' ', ChessGame.figures[enemy_color]]):
                    possible_moves.append(ChessGame.alphabet[ChessGame.alphabet.index(self.pos[0]) + vector[0]]+str(int(''.join([i for i in self.pos if i.isdigit()])) + vector[1]))
            except (IndexError, KeyError):
                pass
        return possible_moves

    def __str__(self):
        return 'I' if self.color == 'White' else 'i'


class Archbishop(Figure):

    def __init__(self, pos, color):
        super().__init__(pos, color)

    def calculate_possible_moves(self, field: dict) -> list:
        possible_moves = Knight(self.pos, self.color).calculate_possible_moves(field) + Bishop(self.pos, self.color).calculate_possible_moves(field)
        return possible_moves

    def __str__(self):
        return 'S' if self.color == 'White' else 's'


class Chancellor(Figure):

    def __init__(self, pos, color):
        super().__init__(pos, color)

    def calculate_possible_moves(self, field: dict) -> list:
        possible_moves = Knight(self.pos, self.color).calculate_possible_moves(field) + Rook(self.pos, self.color).calculate_possible_moves(field)
        return possible_moves

    def __str__(self):
        return 'E' if self.color == 'White' else 'e'


class Game:

    def __init__(self, type_game):
        self.type_game = type_game

    def start_game(self):
        if self.type_game in '123':
            ChessGame(self.type_game).play([], 'White')


class ChessGame(Game):
    base_field = {
        'A': {
            '1': Rook('A1', 'White'),
            '2': Pawn('A2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('A7', 'Black'),
            '8': Rook('A8', 'Black'),
        },
        'B': {
            '1': Knight('B1', 'White'),
            '2': Pawn('B2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('B7', 'Black'),
            '8': Knight('B8', 'Black'),
        },
        'C': {
            '1': Bishop('C1', 'White'),
            '2': Pawn('C2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('C7', 'Black'),
            '8': Bishop('C8', 'Black'),
        },
        'D': {
            '1': Queen('D1', 'White'),
            '2': Pawn('D2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('D7', 'Black'),
            '8': Queen('D8', 'Black'),
        },
        'E': {
            '1': King('E1', 'White'),
            '2': Pawn('E2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('E7', 'Black'),
            '8': King('E8', 'Black'),
        },
        'F': {
            '1': Bishop('F1', 'White'),
            '2': Pawn('F2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('F7', 'Black'),
            '8': Bishop('F8', 'Black'),
        },
        'G': {
            '1': Knight('G1', 'White'),
            '2': Pawn('G2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('G7', 'Black'),
            '8': Knight('G8', 'Black'),
        },
        'H': {
            '1': Rook('H1', 'White'),
            '2': Pawn('H2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('H7', 'Black'),
            '8': Rook('H8', 'Black'),
        },
    }
    hex_field = {
        'A': {
            '1':'-',
            '2':'-',
            '3':'-',
            '4': '-',
            '5': Rook('A5', 'White'),
            '6': '█',
            '7': Pawn('A7','White'),
            '8': '█',
            '9': ' ',
            '10': '█',
            '11': ' ',
            '12': '█',
            '13': Pawn('A13','Black'),
            '14': '█',
            '15': Rook('A15','Black'),
            '16': '-',
            '17': '-',
            '18': '-',
            '19': '-',
        },
        'B': {
            '1': '-',
            '2': '-',
            '3': '-',
            '4': Knight('B4','White'),
            '5': '█',
            '6': Pawn('B6','White'),
            '7': '█',
            '8': ' ',
            '9': '█',
            '10': ' ',
            '11': '█',
            '12': ' ',
            '13': '█',
            '14': Pawn('B14','Black'),
            '15': '█',
            '16': Bishop('B16','Black'),
            '17': '-',
            '18': '-',
            '19': '-',
        },
        'C': {
            '1': '-',
            '2': '-',
            '3': Bishop('C3', 'White'),
            '4': '█',
            '5': Pawn('C5','White'),
            '6': '█',
            '7': ' ',
            '8': '█',
            '9': ' ',
            '10': '█',
            '11': ' ',
            '12': '█',
            '13': ' ',
            '14': '█',
            '15': Pawn('C15','Black'),
            '16': '█',
            '17': Knight('C17','Black'),
            '18': '-',
            '19': '-',
        },
        'D': {
            '1': '-',
            '2': Queen('D2','White'),
            '3': '█',
            '4': Pawn('D4','White'),
            '5': '█',
            '6': ' ',
            '7': '█',
            '8': ' ',
            '9': '█',
            '10': ' ',
            '11': '█',
            '12': ' ',
            '13': '█',
            '14': ' ',
            '15': '█',
            '16': Pawn('D16','Black'),
            '17': '█',
            '18': Bishop('D18','Black'),
            '19': '-',
        },
        'E': {
            '1': King('E1','White'),
            '2': '█',
            '3': Pawn('E3', 'White'),
            '4': '█',
            '5': ' ',
            '6': '█',
            '7': ' ',
            '8': '█',
            '9': ' ',
            '10': '█',
            '11': ' ',
            '12': '█',
            '13': ' ',
            '14': '█',
            '15': ' ',
            '16': '█',
            '17': Pawn('E17', 'Black'),
            '18': '█',
            '19': King('E19','Black'),
        },
        'F': {
            '1': '-',
            '2': Bishop('F2', 'White'),
            '3': '█',
            '4': Pawn('F4', 'White'),
            '5': '█',
            '6': ' ',
            '7': '█',
            '8': ' ',
            '9': '█',
            '10': ' ',
            '11': '█',
            '12': ' ',
            '13': '█',
            '14': ' ',
            '15': '█',
            '16': Pawn('F16', 'Black'),
            '17': '█',
            '18': Queen('F18','Black'),
            '19': '-',
        },
        'G': {
            '1': '-',
            '2': '-',
            '3': Knight('G3','White'),
            '4': '█',
            '5': Pawn('G5','White'),
            '6': '█',
            '7': ' ',
            '8': '█',
            '9': ' ',
            '10': '█',
            '11': ' ',
            '12': '█',
            '13': ' ',
            '14': '█',
            '15': Pawn('G15','Black'),
            '16': '█',
            '17': Bishop('G17','Black'),
            '18': '-',
            '19': '-',
        },
        'H': {
            '1': '-',
            '2': '-',
            '3': '-',
            '4': Bishop('H4','White'),
            '5': '█',
            '6': Pawn('H6', 'White'),
            '7': '█',
            '8': ' ',
            '9': '█',
            '10': ' ',
            '11': '█',
            '12': ' ',
            '13': '█',
            '14': Pawn('H14','Black'),
            '15': '█',
            '16': Knight('H16','Black'),
            '17': '-',
            '18': '-',
            '19': '-',
        },
        'I': {
            '1': '-',
            '2': '-',
            '3': '-',
            '4': '-',
            '5': Rook('I5', 'White'),
            '6': '█',
            '7': Pawn('I7', 'White'),
            '8': '█',
            '9': ' ',
            '10': '█',
            '11': ' ',
            '12': '█',
            '13': Pawn('I13','Black'),
            '14': '█',
            '15': Rook('I15','Black'),
            '16': '-',
            '17': '-',
            '18': '-',
            '19': '-',
        },
    }

    mod_field = copy.deepcopy(base_field)
    mod_field['G']['2'] = Infantry('G2', 'White')
    mod_field['G']['7'] = Infantry('G7', 'Black')
    mod_field['B']['2'] = Infantry('B2', 'White')
    mod_field['B']['7'] = Infantry('B7', 'Black')
    mod_field['F']['1'] = Archbishop('F1', 'White')
    mod_field['F']['8'] = Archbishop('F8', 'Black')
    mod_field['B']['1'] = Chancellor('B1', 'White')
    mod_field['B']['8'] = Chancellor('B8', 'Black')

    figures = {
        1: 'RNBQKPI',
        -1: 'rnbqkpi',
        'White': 'RNBQKPIES',
        'Black': 'rnbqkpies',
        'All': 'RNBQKPIrnbqkpi',
    }
    alphabet = ''.join(letter for letter in base_field.keys())
    def __init__(self, type_game):
        self.game_over = False
        super().__init__(type_game)
        if type_game == '1':
            self.field = ChessGame.base_field
        elif type_game == '2':
            self.field = ChessGame.mod_field
        elif type_game == '3':
            self.field = ChessGame.hex_field

    def print_field(self, green: list or None = None, red: list or None=None) -> None:
        """
        Метод отрисовывает поле в консоль
        :param green: массив позиций фигур, которые могут быть съедены игроком
        :param red: массив позиций фигур, которые могут быть съедены противником в следующий ход
        :return: None
        """
        green = [] if green is None else green
        red = [] if red is None else red
        print('   ', end=' ')
        for key in self.field.keys():
            print('\033[37m' + key + '\033[0m', end=' ')
        print()
        for number in range(len(self.field['A'].keys()), 0, -1):
            print('\033[37m' + (' ' * (-1*(len(str(number))-2)))+ str(number) + '\033[0m', end='')
            print('\033[37m' + '|' + '\033[0m', end=' ')
            for key in self.field.keys():
                if key + str(number) in green:
                    print('\033[32m' + self.field[key][str(number)].__str__() + '\033[0m', end=' ')
                elif key + str(number) in red:
                    if self.field[key][str(number)].__str__() in 'Kk':
                        print('\033[35m' + self.field[key][str(number)].__str__() + '\033[0m', end=' ')
                    else:
                        print('\033[31m' + self.field[key][str(number)].__str__() + '\033[0m', end=' ')
                else:
                    print(self.field[key][str(number)], end=' ')
            print('\033[37m' + '|' + '\033[0m', end='')
            print('\033[37m' + str(number) + '\033[0m')
        print('   ', end=' ')
        for key in self.field.keys():
            print('\033[37m' + key + '\033[0m', end=' ')
        print()

    def under_fire(self, color: str) -> list:
        """
        Метод просчитывает все фигуры игрока, переданного цвета, который могут быть съедены противником
        :param color: цвет игрока, который ходит
        :return: список фигур, который находиться под атакой
        """
        enemy_color = 'Black' if color == 'White' else 'White'
        under_fire_figures = []
        for ally_key in self.field.keys():
            for ally_number in self.field[ally_key].keys():
                if self.field[ally_key][ally_number].__str__() in self.figures[color]:
                    for key in self.field.keys():
                        for number in self.field[key].keys():
                            if self.field[key][number].__str__() in self.figures[enemy_color]:
                                if (ally_key + ally_number) in self.field[key][number].calculate_possible_moves(self.field):
                                    under_fire_figures.append(ally_key + ally_number)
        return under_fire_figures

    def check_check(self, color: str) -> bool:
        """
        Метод проверяет находиться ли король игрока переданного цвета под шахом
        :param color: цвет игрока
        :return: True - король под шахом, False - шаха нет
        """
        pos_king = self.find_king(color)
        if pos_king in self.under_fire(color):
            return True
        return False

    def find_king(self, color: str) -> str:
        """
        Метод находит позицию короля игрока, переданного цвета, на игровом поле
        :param color: цвет игрока
        :return: позиция короля на игровом поле
        """
        figure = 'K' if color == 'White' else 'k'
        pos_king = ''
        for key in self.field.keys():
            for number in self.field[key].keys():
                if self.field[key][number].__str__() == figure:
                    pos_king = key + number
        return pos_king

    def check_mate(self, color: str) -> bool:
        """
        Метод проверяет стоит ли мат игроку, переданного цвета
        :param color: цвет игрока
        :return: True - мат, False - нет мата
        """
        temp = True
        for key in self.field.keys():
            for number in self.field[key].keys():
                if self.field[key][number].__str__() in self.figures[color]:
                    tmp = self.field[key][number].calculate_possible_moves(self.field)
                    for possible_move in tmp:
                        self.field = self.field[key][number].step(self.field, possible_move)[0]
                        if not self.check_check(color):
                            temp = False
                            self.return_steps(1, color)
                            break
                        else:
                            self.return_steps(1, color)
                if not temp:
                    break
            if not temp:
                break

        return temp

    def tips(self, possible_moves: list, color: str) -> None:
        """
        Выводит в консоль поле с подсказками для ходящего игрока
        :param possible_moves: все возможные ходы для выбранной фигуры
        :param color: цвет игрока
        :return: None
        """
        green = []
        for step in possible_moves:
            if step == '0-0':
                if color == 'White':
                    self.field['G']['1'] = '*'
                else:
                    self.field['G']['8'] = '*'
            elif step == '0-0-0':
                if color == 'White':
                    self.field['C']['1'] = '*'
                else:
                    self.field['C']['8'] = '*'
            else:
                if self.field[step[0]][''.join([i for i in step if i.isdigit()])] == ' ':
                    self.field[step[0]][''.join([i for i in step if i.isdigit()])] = '*'
                else:
                    green.append(step)
        self.print_field(green, None)
        self.clear_tips()

    def clear_tips(self) -> None:
        """
        Удаляет подсказки с поля
        :return: None
        """
        for key in self.field.keys():
            for number in self.field[key].keys():
                if self.field[key][number] == '*':
                    self.field[key][number] = ' '

    @staticmethod
    def get_figure_by_str(name):
        name = name.upper()
        if name == 'Q':
            return Queen
        elif name == 'B':
            return Bishop
        elif name =='I':
            return Infantry
        elif name == 'R':
            return Rook
        elif name == 'N':
            return Knight
        elif name == 'S':
            return Archbishop
        elif name == 'E':
            return Chancellor
        elif name == 'K':
            return King

    def return_steps(self, count, color):
        steps = moves[::-1]
        if count > len(moves):
            print('\033[31m' + 'Такого кол-ва ходов не было разыграно' + '\033[0m')
            return color
        for step in range(count):
            if steps[step] == '0-0':
                if color == 'Black':
                    self.field['G']['1'] = ' '
                    self.field['F']['1'] = ' '
                    self.field['H']['1'] = Rook('H1', 'White')
                    self.field['E']['1'] = King('E1', 'White')
                else:
                    self.field['G']['8'] = ' '
                    self.field['F']['8'] = ' '
                    self.field['H']['8'] = Rook('H8', 'Black')
                    self.field['E']['8'] = King('E8', 'Black')
            elif steps[step] == '0-0-0':
                if color == 'Black':
                    self.field['C']['1'] = ' '
                    self.field['D']['1'] = ' '
                    self.field['A']['1'] = Rook('A1', 'White')
                    self.field['E']['1'] = King('E', 'White')
                else:
                    self.field['C']['8'] = ' '
                    self.field['D']['8'] = ' '
                    self.field['A']['8'] = Rook('A8', 'Black')
                    self.field['E']['8'] = King('E8', 'Black')
            else:
                if '-' in steps[step]:
                    current, expected = steps[step].split('-')
                    if len(expected) == 2:
                        self.field[expected[0]][''.join([i for i in expected if i.isdigit()])].pos = current if len(current) == 2 else current[1:]
                        if len(current) == 2:
                            self.field[current[0]][''.join([i for i in current if i.isdigit()])], \
                            self.field[expected[0]][''.join([i for i in expected if i.isdigit()])] = \
                            self.field[expected[0]][''.join([i for i in expected if i.isdigit()])], \
                            self.field[current[0]][''.join([i for i in current if i.isdigit()])]
                        else:
                            self.field[current[1]][''.join([i for i in current if i.isdigit()])], \
                            self.field[expected[0]][
                                ''.join([i for i in expected if i.isdigit()])] = self.field[expected[0]][
                                ''.join([i for i in expected if i.isdigit()])], self.field[current[1]][
                                ''.join([i for i in current if i.isdigit()])]
                    else:
                        self.field[expected[1]][''.join([i for i in expected if i.isdigit()])].pos = current if len(
                            current) == 2 else current[1:]
                        if len(current) == 2:
                            self.field[current[0]][''.join([i for i in current if i.isdigit()])], \
                            self.field[expected[1]][''.join([i for i in expected if i.isdigit()])] = \
                            self.field[expected[1]][''.join([i for i in expected if i.isdigit()])], \
                            self.field[current[0]][''.join([i for i in current if i.isdigit()])]
                        else:
                            self.field[current[1]][''.join([i for i in current if i.isdigit()])], \
                            self.field[expected[1]][
                                ''.join([i for i in expected if i.isdigit()])] = self.field[expected[1]][
                                ''.join([i for i in expected if i.isdigit()])], self.field[current[1]][
                                ''.join([i for i in current if i.isdigit()])]
                elif ':' in steps[step]:
                    current, expected = steps[step].split(':')
                    self.field[expected[0]][''.join([i for i in expected if i.isdigit()])].pos = current if len(current) == 2 else current[1:]
                    if len(expected) == 2:
                        self.field[expected[0]][''.join([i for i in expected if i.isdigit()])] = Pawn(expected, 'Black' if color == 'White' else 'White')
                    else:
                        self.field[expected[1]][''.join([i for i in expected if i.isdigit()])] = ChessGame.get_figure_by_str(expected[0])(expected if len(expected) == 2 else expected[1:], 'Black' if color == 'White' else 'White')
                    if len(current) == 2:
                        self.field[current[0]][''.join([i for i in current if i.isdigit()])] = Pawn(current, 'White' if color == 'White' else 'Black')
                    else:
                        self.field[current[1]][current[-1]] = ChessGame.get_figure_by_str(current[0])(current if len(current) == 2 else current[1:], 'White' if color == 'White' else 'Black')
            color = 'Black' if color == 'White' else 'White'
            moves.pop(-1)
        return color

    def play(self, notation, color):
        global moves
        moves = notation
        flag = color
        while not self.game_over:
            self.print_field(green=None, red=self.under_fire(flag))
            if self.check_check(flag) and self.check_mate(flag):
                self.game_over = True
                previous_color = 'чёрных' if flag == 'White' else 'белых'
                print(f'Игра окончена! Мат! Победа {previous_color}')
                continue
            if flag == 'White':
                print('Ход белых')
            else:
                print('Ход чёрных')
            operand = input('Введите позицию фигуры, которой будет сделан ход: ').upper()
            if str(len(operand)) not in '23':
                print('\033[31m' + 'Введена несуществующая позиция' + '\033[0m')
                self.play(moves, flag)
            if operand == '<-':
                count = int(input('Введите количество ходов для отмены:'))
                flag = self.return_steps(count, flag)
            else:
                try:
                    figure = self.field[operand[0]][''.join([i for i in operand if i.isdigit()])]
                    if figure == ' ':
                        print('\033[31m' + 'На выбранной клетке нет фигуры' + '\033[0m')
                        self.play(moves, flag)
                    elif figure.color != flag:
                        print('\033[31m' + 'Сейчас ход фигур другого цвета' + '\033[0m')
                        self.play(moves, flag)
                    else:
                        possible_moves = figure.calculate_possible_moves(self.field)
                        if not possible_moves:
                            print('\033[31m' + 'Этой фигурой некуда сходить' + '\033[0m')
                        self.tips(possible_moves, flag)
                        step = input('Введите позицию для перемещения фигуры: ').upper()
                        if ChessGame.can_move(possible_moves, step, flag):
                            self.field, flag = figure.step(self.field, step)
                            enemy_color = 'White' if flag == 'Black' else 'Black'
                            if self.check_check(enemy_color):
                                temp = 'Белым' if flag == 'White' else 'Чёрным'
                                print('\033[31m' + f'Шах {temp}! Введите ход заново' + '\033[0m')
                                flag = self.return_steps(1, flag)
                            moves = list(filter(lambda x: x != '', moves))
                        else:
                            print('\033[31m' + 'Эта фигура не может сходить туда' + '\033[0m')
                            self.play(moves, flag)
                except KeyError:
                    print('\033[31m' + 'Такой клетки нет на поле' + '\033[0m')
                    self.play(moves, flag)

    @staticmethod
    def check_castling(field, color):
        possible_castling = []
        if color == 'White':
            if field['F']['1'] == field['G']['1'] == ' ' and not ChessGame.check_in_moves('RH1') and not ChessGame.check_in_moves('KE1'):
                possible_castling.append('0-0')
            if field['B']['1'] == field['C']['1'] == ' ' and not ChessGame.check_in_moves('RA1') and not ChessGame.check_in_moves('KE1'):
                possible_castling.append('0-0-0')
        elif color == 'Black':
            if field['F']['8'] == field['G']['8'] == ' ' and not ChessGame.check_in_moves('rH8') and not ChessGame.check_in_moves('kE8'):
                possible_castling.append('0-0')
            if field['B']['8'] == field['C']['8'] == ' ' and not ChessGame.check_in_moves('rA8') and not ChessGame.check_in_moves('kE8'):
                possible_castling.append('0-0-0')
        return possible_castling

    @staticmethod
    def check_in_moves(position):
        flag = False
        for step in moves:
            if position in step:
                flag = True
                break
        return flag

    @staticmethod
    def can_move(possible_moves, expected, color):
        if color == 'White':
            possible_moves = (' '.join(possible_moves).replace('0-0-0', 'C1').replace('0-0', 'G1')).split(' ')
        else:
            possible_moves = (' '.join(possible_moves).replace('0-0-0', 'C8').replace('0-0', 'G8')).split(' ')
        if expected in possible_moves:
            return True
        return False


def main():
    type_game = input('Введите номер игры, в которую хотите сыграть (1-классические шахматы, 2-модифицированные шахматы, 3 - гексагональные шахматы): ')
    if (type_game == '3'):
        ChessGame.alphabet += 'I'
    game = Game(type_game)
    game.start_game()


if __name__ == '__main__':
    main()
