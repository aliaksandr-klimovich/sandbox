from random import randint


class Ship(object):
    """
    Abstract class
    """
    is_on_board = False
    is_alive = False


class Battleship(Ship):
    length = 4


class Cruiser(Ship):
    length = 3


class Destroyer(Ship):
    length = 2


class Submarine(Ship):
    length = 1


class Cell(object):
    """
    Cell class to represent cell on board

    position - tuple with cell coordinates
    """
    is_available = True

    def __init__(self, position):
        self.position = position

    def __str__(self):
        LETTERS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
        DIGITS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        return "<Cell {}{}>".format(LETTERS[self.position[0]],
                                    DIGITS[self.position[1]])


class Board(object):
    def __init__(self):
        self.populate()

    def populate(self):
        self._create_cells()
        self._create_ships()
        # self._place_ships_on_cells()

    def _create_cells(self):
        self.cells = [[Cell((i, j)) for i in range(10)] for j in range(10)]

    def _create_ships(self):
        self.ships = []
        for i in range(1):
            self.ships.append(Battleship())
        for i in range(2):
            self.ships.append(Cruiser())
        for i in range(3):
            self.ships.append(Destroyer())
        for i in range(4):
            self.ships.append(Submarine())

    def _place_ships_on_cells(self):
        ships_to_place = [ship for ship in self.ships]
        while ships_to_place:
            ship = ship[0]
            r = randint(0, 9)
