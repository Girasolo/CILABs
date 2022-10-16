# LAB 1: Set Covering
### Francesco Scalera, Giuseppe Esposito, Filippo Maria Cardano (s292113)

Given a number N and some lists of integers P = (L_0, L_1, L_2, ..., L_n),
determine, if possible, S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n}),
such that each number between 0 and N-1 appears in at least one list.

We decided to use the A* searching algorithm that professor showed us during the lectures,
adapting it to the problem provided.

In particular, our implementation concerns:
 - The choice of an appropriate priority function for the frontier,
   based on the summation of length of subset of list (our current state) and the number of element that we need to complete the task assigned
 - We chose the length of a list as a unit cost
 - We sorted the list set by the length of each list
 - Since we sorted the list set by the length of each list, we decided to set as initial state the first element of the randomly generated list
 - After generating the initial block (list of lists) we just kept the unique values 

## Results

Here we display the execution times of the A* algorithm we developed

| **Iteration \ N** | **5** | **10** | **20** | **100**           | **500**           | **1000**          |
|-------------------|-------|--------|--------|-------------------|-------------------|-------------------|
| w                 | 5     | 10     | 23     | could not compute | could not compute | could not compute |
| 1                 | 4 steps; 60 states   | 6 steps; 1,096 states   | 6 steps; 470,898 states   |                   |                   |                   |
| 2                 | 5 steps; 42 states   | 6 steps; 1,126 states    | 6 steps; 437,832 states   |                   |                   |                   |
| 3                 | 5 steps; 33 states   | 5 steps; 748 states    | 6 steps; 469,067 states   |                   |                   |                   |
| 4                 | 5 steps; 42 states   | 5 steps; 1,715 states    | 6 steps; 538,164 states   |                   |                   |                   |
| 5                 | 5 steps; 59 states   | 5 steps; 1,287 states   | 6 steps; 477,490 states   |                   |                   |                   |
| 6                 | 5 steps; 33 states   | 5 steps; 1,021 states    | 6 steps; 438,632 states   |                   |                   |                   |
| 7                 | 5 steps; 42 states   | 4 steps; 749 states    | 6 steps; 517,984 states   |                   |                   |                   |
| 8                 | 4 steps; 35 states   | 5 steps; 2,025 states   | 6 steps; 433,693 states   |                   |                   |                   |
| 9                 | 6 steps; 81 states   | 5 steps; 1,171 states    | 6 steps; 483,435 states   |                   |                   |                   |
| 10                | 5 steps; 33 states   | 6 steps; 1,235 states    | 6 steps; 446,306 states   |                   |                   |                   |
| Average           | 5 steps; 46 states   | 5 steps; 1217 stetes    | 6 steps; 471,350 states  |                   |                   |                   |
