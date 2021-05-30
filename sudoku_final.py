import numpy as np


def initialise_units_and_buddies():
    """The initialise_units_and_buddies function creates two constants which are later used to set the domain
    of positions across the puzzle."""
    for position in POSITIONS:
        col = []
        row = []
        square = []
        buddy_set = set()
        for i in range(9):
            buddy_set.add((position[0], i))
            buddy_set.add((i, position[1]))
            col.append((position[0], i))
            row.append((i, position[1]))
        square_top_x, square_top_y = 3 * (position[0] // 3), 3 * (position[1] // 3)
        for x in range(square_top_x, square_top_x + 3):
            for y in range(square_top_y, square_top_y + 3):
                buddy_set.add((x, y))
                square.append((x, y))
        buddy_set.remove(position)
        BUDDIES[position] = buddy_set
        UNITS[position] = [col, row, square]


# Constants

POSITIONS = [(r, c) for r in range(9) for c in range(9)]
UNITS = {}
BUDDIES = {}
initialise_units_and_buddies()


def sudoku_solver(sudoku):
    """The sudoku_solver function takes sudokus represented as 9x9 numpy arrays (with empties as 0) as inputs and outputs
    completed 9x9 numpy arrays or -1 if failed."""
    sudoku = convert_to_string(sudoku)
    sudoku = convert_to_dict(sudoku)
    sudoku = depth_first_search(sudoku)
    if sudoku is False:
        return np.full((9, 9), -1)
    solved_sudoku = np.array([int(value) for value in sudoku.values()]).reshape((9, 9))
    return solved_sudoku


def depth_first_search(sudoku):
    if sudoku is False:
        return False
    if is_goal(sudoku):
        return sudoku
    new_position = order_values(sudoku)
    return find_possible_path(depth_first_search(set_num(sudoku.copy(), new_position, num)) for num in sudoku[new_position])


def find_possible_path(searches):
    """The find_possible_path function checks if some element of the input sequence is true."""
    for search in searches:
        if search:
            return search
    return False


def order_values(sudoku):
    """The order_values function sets up the 'minimum-remaining-values' (MRV) heuristic which is used
    when searching."""
    length = 9
    new_position = False
    for position, nums in sudoku.items():
        if 2 <= len(nums) < length:
            length = len(nums)
            new_position = position
    return new_position


def is_goal(sudoku):
    """The is_goal function returns True or False depending on whether sudoku in goal state."""
    goal_state = True
    for position in POSITIONS:
        if len(sudoku[position]) != 1:
            goal_state = False
    if goal_state is True:
        return True
    else:
        return False


def set_num(sudoku, position, num):
    """The set_num function sets a num into a particular position by eliminating all other nums from that position"""
    flag = True
    for other_num in sudoku[position]:
        if other_num != num:
            if remove_num(sudoku, position, other_num) is False:
                flag = False
    if flag is False:
        return False
    else:
        return sudoku


def convert_to_dict(sudoku):
    empty_sudoku = dict((pos, '123456789') for pos in POSITIONS)
    sudoku = dict(zip(POSITIONS, sudoku))
    for pos, num in sudoku.items():
        if num in '123456789' and set_num(empty_sudoku, pos, num) is False:
            return False
    return empty_sudoku


def convert_to_string(sudoku):
    string = ''
    for row in sudoku:
        for value in row:
            string += str(value)
    return string


def remove_num(sudoku, position, num):
    """The remove_num function removes a number from the domain of a position and checks if that number can
    be set elsewhere."""
    # if the number has already been removed return sudoku
    if num not in sudoku[position]:
        return sudoku
    sudoku[position] = sudoku[position].replace(num, '')
    # if we now have only 1 remaining possible num see if we can eliminate it from its buddies if we can't return False
    if len(sudoku[position]) == 1:
        if all(remove_num(sudoku, buddy_num, sudoku[position]) for buddy_num in BUDDIES[position]) is False:
            return False
    # if there is now no possible number for that position return False
    elif not sudoku[position]:
        return False
    # looping position's rows, columns and squares, find the possible positions for num
    for unit in UNITS[position]:
        possible_num_positions = []
        for pos in unit:
            if num in sudoku[pos]:
                possible_num_positions.append(pos)
        # if only one possible position try and set that position to num.
        if len(possible_num_positions) == 1:
            if set_num(sudoku, possible_num_positions[0], num) is False:
                return False
        # if not possible position for num return False
        elif not possible_num_positions:
            return False
    return sudoku