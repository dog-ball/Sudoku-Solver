# Sudoku Solver

### Choice of Algorithm

Inspired by the ability of constraint satisfaction to make a seemingly intractable problem tractable, I have chosen to model this sudoku puzzle solver using the constraint satisfaction algorithm.

### Implementation

Following some research into the many ways sudoku can be approached from an algorithmic standpoint [1], I began by writing a baseline sudoku solver (saved as baseline.py) in order to assess the performance of my constraint satisfaction model. This initial approach was implemented using a simple search function which recursively assigned numbers into the positions of the sudoku puzzle, backtracking if assigning a  number violated one of the three rules of the puzzle. I tested this model using the tests provided in the sudoku.ipynb file. The baseline was able to solve all of the medium graded puzzles in less than 0.1 seconds but was unable to solve any of the hard graded puzzles within the 20 seconds required to count as successful (taking longer than 180 seconds on hard sudoku number 10).

Next, I then turned my focus to my implementation of the constraint satisfaction algorithm with the goal of improving upon the performance of my baseline model and solving all of the hard graded sudoku puzzles in at least 20 seconds. This time, I kept track of the domain of each of the positions in the sudoku puzzle, updating the domain of all its 'buddies' (other positions which share either a row, column or square with the current position). Keeping track of the domain provided a number of significant speed gains by reducing the size of the search space [2]. For example, if the domain of one position is reduced to one number, that number can then be removed from the domains of all of its 'buddies'. 

Alongside this, by tracking and constantly reducing the domains of positions across the puzzles, the constraint satisfaction allows for other positions to be reduced to a domain of one position without ever having to search, in fact many puzzles can be solved this way without ever having to search. However, on harder puzzles, when tracking the domain alone proves insufficient, constraint satisfaction allows for an improved search function by searching for the next position with the smallest domain. In Russel and Norvig's Artificial intelligence: A Modern Approach, this improvement to the classic depth-first-search is called a 'minimum-remaining-values (MRV) heuristic' [3] (page 216). This allows for an informed approach when choosing the next position to try rather than blindly selecting the next unassigned position since it can be more efficient to pick the position which currently has the fewest options.

### Data structures 

I have chosen to use a dictionary to represent the Sudoku with the positions of the sudoku (e.g., (0, 0), ... , (8,8)) stored as keys and the possible values (e.g., '123456789') stored as corresponding values. I made use of the fact that dictionaries evaluate to True to track whether a search had failed or a problem was unsolvable. The 'truthy' [4] quality of the dictionary data structure allowed me to keep track of whenever a part of the algorithm had failed by setting returning false and evaluating the dictionaries Boolean value. If True the algorithm was working, if False it had failed. Next time, I could create a more elegant representation of the sudoku using an array instead of dictionary while still maintaining the beneficial functionality.

### Further Research

In order to further increase the speed of the sudoku solver, I could look into implementing constraint satisfaction using the programming language C. t-dillon has written an interesting blog post and produced some extremely impressive results going down this route [5].

Grover's algorithm, also known as the quantum search algorithm, appears to have to reduce the time complexity of this kind of search problem [6]. Thus, there is the potential for even faster sudoku solving programmes later down the line.

##### References:

[1] - https://en.wikipedia.org/wiki/Sudoku_solving_algorithms
[2] - https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-s095-programming-for-the-puzzled-january-iap-2018/puzzle-8-you-wont-want-to-play-sudoku-again/
[3] - Artificial intelligence: A Modern Approach, Russell, Stuart ; Norvig, Peter 
[4] - https://www.freecodecamp.org/news/truthy-and-falsy-values-in-python/
[5] - https://t-dillon.github.io/tdoku/#TheTseytinesqueTransformation
[6] - https://en.wikipedia.org/wiki/Grover%27s_algorithm
