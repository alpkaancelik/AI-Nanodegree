# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propogation is a strategy in AI where instead of searching through the entire solution space, we apply certain constraints/heuristics to the problem over and over again to narrow the options that we need to search, so that we can find a solution in reasonable time.
We apply this technique to solve this sudoku board. We take an initial board, and instead of trying to solve it right away, we apply Elimination, Naked Twins, and Only Choice strategies repeatedly until we find a solution or say that the board is unsolvable. For the naked twins specifically, we look at each unit, and if there are two boards that have the same two values, we remove twose two values from the possible values of all the other empty boxes.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Normally, in a sudoku, you need to have digits from 1 to 9 once in each square box, row and column. In a diagonal sudoku, the problem gets even harder as each of the two diagonals also need to have each such digit only once. This adds more complexity to the problem as it increases the solution space that we need to search. However, by applyting the constraint propogation technique as defined in the previous question, we can solve the diagonal sudoku.
The way I solved it was very simple: just like we defined square units, row units and column units early in the program, I defined "diagonal units", and added it to the unit list. Therefore, the program checked for solutions in the diagonals just like it checked the rows, colums, and squares in each time it applied one of our three heuristics. As in usual constraint propogation, we do this cycle multiple times until we reach a solution or the conclusion that the board is not possible to solve.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

