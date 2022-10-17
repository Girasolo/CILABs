# LAB 1: Set Covering
### Francesco Scalera(S...), Giuseppe Esposito(S302179), Filippo Maria Cardano (S292113)

Given a number N and some lists of integers P = (L_0, L_1, L_2, ..., L_n),
determine, if possible, S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n}),
such that each number between 0 and N-1 appears in at least one list.

We decided to use the A* searching algorithm that professor showed us during the lectures,
adapting it to the problem provided.

In particular, our implementation concerns:
 - The choice of an appropriate priority function for the frontier,
   based on the summation of length of subset of list (our current state) and the number of elements that we need to complete the task assigned
 - We chose the length of a list as a unit cost of an action
 - We sorted the list set by the length of each list
 - In order to reduce the computation complexity, we discarded the list duplicates from the initial state
 - After generating the initial block (list of lists) we just kept the unique values 

## Results

Here we display for our A* algorithm the number of steps it took to find a solution, the number of visited states and the 'w' of the final solution.
The tests were repeated 10 times.

| **Test \ N** | **5** | **10** | **20** | **100**           | **500**           | **1000**          |
|-------------------|-------|--------|--------|-------------------|-------------------|-------------------|
|  Average w                 | 5     | 10     | 23     | 90 | 1264 | 300,470 |
| 1                 | 4 solution steps; 60 visited states   | 6 solution steps; 1,096 visited states   | 6 solution steps; 470,898 visited states   |6 solution steps; 1,056 visited states|6 solution steps; 2,126 visited states| 9 solution steps; 28,925 visited states| 
| 2                 | 5 solution steps; 42 visited states   | 6 solution steps; 1,126 visited states    | 6 solution steps; 437,832 visited states   |5 solution steps; 847 visited states; w: 80|6 solution steps; 2,126 visited states; w: 173|9 solution steps; 28,925 visited states; w: 3077|
| 3                 | 5 solution steps; 33 visited states   | 5 solution steps; 748 visited states    | 6 solution steps; 469,067 visited states   |5 solution steps; 847 visited states|6 solution steps; 2,126 visited states|9 solution steps; 28,925 visited states|
| 4                 | 5 solution steps; 42 visited states   | 5 solution steps; 1,715 visited states    | 6 solution steps; 538,164 visited states   |6 solution steps; 1,056 visited states|6 solution steps; 2,126 visited states|9 solution steps; 28,925 visited states|
| 5                 | 5 solution steps; 59 visited states   | 5 solution steps; 1,287 visited states   | 6 solution steps; 477,490 visited states   |5 solution steps; 847 visited states|6 solution steps; 2,126 visited states|9 solution steps; 28,925 visited states|
| 6                 | 5 solution steps; 33 visited states   | 5 solution steps; 1,021 visited states    | 6 solution steps; 438,632 visited states   |5 solution steps; 847 visited states; w: 80|6 solution steps; 2,126 visited states; w: 184|9 solution steps; 28,925 visited states; w: 2954|
| 7                 | 5 solution steps; 42 visited states   | 4 solution steps; 749 visited states    | 6 solution steps; 517,984 visited states   |5 solution steps; 847 visited states|6 solution steps; 2,126 visited states| 9 solution steps; 28,925 visited states|
| 8                 | 4 solution steps; 35 visited states   | 5 solution steps; 2,025 visited states   | 6 solution steps; 433,693 visited states   |5 solution steps; 847 visited states|6 solution steps; 2,126 visited states|9 solution steps; 28,925 visited states|
| 9                 | 6 solution steps; 81 visited states   | 5 solution steps; 1,171 visited states    | 6 solution steps; 483,435 visited states   |5 solution steps; 847 visited states| 6 solution steps; 2,126 visited states|9 solution steps; 28,925 visited states|
| 10                | 5 solution steps; 33 visited states   | 6 solution steps; 1,235 visited states    | 6 solution steps; 446,306 visited states   |5 solution steps; 847 visited states| 6 solution steps; 2,126 visited states|9 solution steps; 28,925 visited states|
| Average           | 5 solution steps; 46 visited states   | 5 solution steps; 1217 visited states    | 6 solution steps; 471,350 visited states  |5 solution steps; 888 visited states|6 solution steps; 2,126 visited states|9 solution steps; 28,925 visited states|

For N = [100, 500, 1000] we were not able to find a proper optimization of the algorithm to find the optimal solution in a reasonable amount of time so we tried to use a unitary cost for all (uninformed strategy) the edges and we noticed that, as expected the algorithm was really fast but the solution was not the optimal one in fact we have an exponential increasing of the bloat as we can see from the results reported in the table. A possible approach for further and future implementation could be the pruning of the graph in terms of depth. 
