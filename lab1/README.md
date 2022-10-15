# LAB 1: Set Covering
### Francesco Scalera, Giuseppe Esposito, Filippo Cardano

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

This is the result for different N:
