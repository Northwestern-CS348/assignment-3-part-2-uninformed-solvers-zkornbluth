from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg1 = []
        peg2 = []
        peg3 = []

        list_of_pegs = self.kb.kb_ask(parse_input("fact: (inst ?peg peg)"))

        for p in list_of_pegs:
            if not Fact(instantiate(Statement(("empty", "?peg")), p)) in self.kb.facts:
                list_of_disks = self.kb.kb_ask(Fact(instantiate(Statement(("on", "?disk", "?peg")), p)))
                list_of_disk_vals = []
                for d_b in list_of_disks:
                    disk_val = int(d_b.bindings_dict["?disk"][4])
                    list_of_disk_vals.append(disk_val)
                peg_val = int(p.bindings_dict["?peg"][3])
                if peg_val == 1:
                    if list_of_disk_vals:
                        while list_of_disk_vals:
                            small = min(list_of_disk_vals)
                            peg1.append(small)
                elif peg_val == 2:
                    if list_of_disk_vals:
                        while list_of_disk_vals:
                            small = min(list_of_disk_vals)
                            peg2.append(small)
                            list_of_disk_vals.remove(small)
                else:
                    if list_of_disk_vals:
                        while list_of_disk_vals:
                            small = min(list_of_disk_vals)
                            peg3.append(small)
                            list_of_disk_vals.remove(small)

        ret = (tuple(peg1), tuple(peg2), tuple(peg3))
        return ret


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        d = terms[0]
        old = terms[1]
        new = terms[2]
        new_top_of_old = self.kb.kb_ask(Fact(Statement(("onTop", d, "?obj"))))[0]
        old_top_of_new = self.kb.kb_ask(Fact(Statement(("top", "?obj", new))))[0]
        to_retract_1 = Fact(instantiate(Statement(("onTop", d, "?obj")), new_top_of_old))
        to_assert_1 = Fact(instantiate(Statement(("top", "?obj", old)), new_top_of_old))
        to_retract_2 = Fact(instantiate(Statement(("top", "?obj", new)), old_top_of_new))
        to_assert_2 = Fact(instantiate(Statement(("onTop", d, "?obj")), old_top_of_new))
        self.kb.kb_retract(Fact(Statement(("on", d, old))))
        self.kb.kb_retract(Fact(Statement(("top", d, old))))
        self.kb.kb_retract(to_retract_1)
        self.kb.kb_retract(to_retract_2)
        self.kb.kb_assert(to_assert_1)
        self.kb.kb_assert(to_assert_2)
        self.kb.kb_assert(Fact(Statement(("on", d, new))))
        self.kb.kb_assert(Fact(Statement(("top", d, new))))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        rows = {"pos1": ("pos1", "pos2", "pos3"),
                "pos2": ("pos1", "pos2", "pos3"),
                "pos3": ("pos1", "pos2", "pos3")}

        s = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for y in rows:
            y_val = int(y[3]) - 1
            for x in rows[y]:
                x_val = int(x[3]) - 1
                ask = Fact(Statement(["coord", "?tile", x, y]))
                b = self.kb.kb_ask(ask)[0]
                t = b.bindings_dict["?tile"][4]
                if t == "y":
                    tile_val = -1
                else:
                    tile_val = int(t)
                s[y_val][x_val] = tile_val
        return tuple([tuple(state[0]), tuple(state[1]), tuple(state[2])])

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        t = terms[0]
        old_x = terms[1]
        old_y = terms[2]
        new_x = terms[3]
        new_y = term[4]
        self.kb.kb_retract(Fact(Statement(("coord", t, old_x, old_y))))
        self.kb.kb_retract(Fact(Statement(("coord", "empty", new_x, new_y))))
        self.kb.kb_assert(Fact(Statement(("coord", t, new_x, new_y))))
        self.kb.kb_assert(Fact(Statement(("coord", "empty", old_x, old_y))))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
