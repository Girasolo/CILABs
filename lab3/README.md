# LAB 3.2: Evolution to solve NIM.
### Filippo Maria Cardano (S292113), Francesco Scalera (S292432), Giuseppe Esposito (S302179), Giuseppe Piombino (S280117)

## Sources
The professor's examples shown in class.

## Evolution vs Genetic Algorithm
We decided to try both ways to solve for the problem, we went more in depth with the evolution aspect, but we kept the genetic algorithm to keep things interesting.

## Evolutionary Approach: Benchmarking
We developed some strategies to benchmark our more advanced strategies, this usually includes lots of randomness, but some have a little logic to improve the finishing moves for example.
- randomNim: Random row, random number of elements
- gabrielleNim: Pick always the maximum possible number of the lowest row
- randomAllNim: Random row, but pick the maximum number of elements
- longestAllNim: Pick always the longest row
- randomSmartNim: Here the strategy improves on the pure random, where it improves the last move

## Evolutionary Approach: 2-parameters
This is the main topic of the lab assignment, the strategies designed to evolve when competing against the benchmarks. These are strategies that use 2 parameters to evolve, for simplicity they are called "p1" and "p2", but different strategies use this two differently.
- E2longestVSshortest_allVS1smart: Shortest row vs Longest Row and pick one element vs take the maximum number of elements
- E2randomVSshortest_allVS1smart: Random row vs Shortest Row and pick one elements vs take the maximum number of elements
- E2longestVSshortest_allVS1allsmart: Shortest row vs Longest Row and a complex selection of whether to take one element or a subset
- E2longestVSrandom_allVS1allsmart: Random row vs Longest Row and a complex selection of whether to take one element or a subset
- E2shortestVSrandom_allVS1allsmart: Random row vs Shortest Row and a complex selection of whether to take one element or a subset
- EsafetySmart: Safety strategy creates based on p1 "safety" nets to fall back on, as the game progresses. The idea is that creating rows with 2 elements can help this strategy win against more complex benchmarks as it uses the safety nets created at the beginning of the game to outsmart the opponent towards the end of the match

## Genetic Approach: Strategy
E3shortestVSlongest_percentage is the only strategy that uses the genetic approach with 3 paraments. Each parament is a chance of take the shortest or longest and how many elements in the row to pick.

## Genetic Approach: Initial Population
In the population individual are represented as a tuple which contains the value of the fitness of the individual, a mask of booleans which represents whether a list is part of the individual and a label that describes the tweak type (mutation, crossover or initial).
We randomly selected a viable individuals of the size of the population that we wanted, the viability is based on capability of an individual to provide a possible solution to the problem (with suboptimal fitness values). 

## Genetic Approach: Fitness Metric
Our fitness metric is based on reaped test (function evaluate) against a different strategy, usually a random strategy with a few tweaks to improve it.

## Genetic Approach: Mutation
The parent on which we apply the genetic operator are chosen with a tournament selection which basically consists in selecting two individuals randomly and selecting who has the best fitness.
Moreover we apply a random gaussian noise to the paramenters of the parent and add it to the offspring list.

## Reinforcement Learning:
The concept behind this algorithm is that an agent learn to take an action (in this case, play a move) with a "trial-and-error" method in a dynamic environment (i.e, the board at a certain state). In the Nim case, the agent is able to learn not only by its own moves, but even by the opponent ones, based on the optimal strategy (nimSum).

## Reinforcement Learning: Agent
The agent keep track of the history of all the states explored during trials, and even the possible actions it can do in a certain state: these possible actions are paired with a value. An action could be chosen by a random choice or based on the maximum value of an action.

## Reinforcement Learning: Policy to take an action
Basically, when the agent is taking an action, a random number is generated. If its value is less than the "random_factor" variable of the agent, a random possible move is performed. Otherwise, we select the best possible move (according to its value) between the enviroment's state possible moves.
- In a first stage, this random_factor variable is 0.8 (more random moves -> more exploration)
- When the algorithm reaches the 60% of number of trials, the random_factor is decreased at 0.2 (more "best" moves -> more exploitation)

## Reinforcement Learning: Learning algorithm
The learning algorithm consists simply in playing a game between the agent and an opponent player that plays with optimal strategy based on NimSum. If it win the game, it receives a reward of +1, otherwise it obtains -1. Based on the reward the agent has received, values of the moves played on a certain state in the history are updated. This update is based on the reward obtained and a parameter alpha. The learning algorithm takes into account also the opponent move and it is performed in two ways: when the agent take the first move, and when the agent doesn't.

## Some results: soon
