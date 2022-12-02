import logging
from collections import namedtuple
import random
from typing import Callable
from copy import deepcopy
from itertools import accumulate
from operator import xor
import numpy as np

Nimply = namedtuple("Nimply", "row, num_objects")

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k
        self._total_elements = num_rows*num_rows

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    @property
    def total_elements(self) -> int:
        return self._total_elements

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))


def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.rows, xor)
    return result

def optimal_startegy(state: Nim) -> Nimply:
    data = cook_status(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]

def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
    ]
    cooked["active_rows_number"] = sum(o > 0 for o in state.rows)
    cooked["shortest_row"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    cooked["longest_row"] = max((x for x in enumerate(state.rows)), key=lambda y: y[1])[0]
    cooked["completion"] = sum(o for o in state.rows) / state.total_elements
    cooked["random"]=random.choice([r for r, c in enumerate(state.rows) if c > 0])
    # cooked["nim_sum"] = nim_sum(state)

    # brute_force = list()
    # for m in cooked["possible_moves"]:
    #     tmp = deepcopy(state)
    #     tmp.nimming(m)
    #     brute_force.append((m, nim_sum(tmp)))
    # cooked["brute_force"] = brute_force

    return cooked

def completion_strategy(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)

        if data["completion"] < genome["p"]:
            ply = Nimply(data["shortest_row"], state.rows[data["shortest_row"]])
        else:
            ply = Nimply(data["longest_row"], state.rows[data["longest_row"]])

        return ply

    return evolvable

def completion_strategy_v2(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)

        take = 19999

        if random.random() < genome["p"]:
            take = 1

        if data["completion"] < 0.5:
            ply = Nimply(data["shortest_row"], min(take, state.rows[data["shortest_row"]]))
        else:
            ply = Nimply(data["longest_row"], min(take, state.rows[data["longest_row"]]))

        return ply

    return evolvable

def random_giuseppe(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)
        if random.random() < genome["p"]:
            ply = Nimply(data["random"], 1)
        else:
            ply = Nimply(data["random"], state.rows[data["random"]])
        return ply
    return evolvable

NUM_MATCHES = 1000
NIM_SIZE = 10

def evaluate(strategy: Callable) -> float:
    opponent = (strategy, random_giuseppe({"p" : 0.5}))
    won = 0

    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            ply = opponent[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES

# random.seed(42)
# print(evaluate(make_strategy({"p" : 0.7})))

# random.seed(42)
# eval_list = []
# for i in range(0, 100):
#     van = evaluate(make_strategy({"p": 0.4}))
#     print(van)
#     eval_list.append(van)
# print(np.average(eval_list))
# sorted(eval_list)[int(len(eval_list) / 2)]

# logging.getLogger().setLevel(logging.DEBUG)
# strategy = (make_strategy({"p": 0.1}), optimal_startegy)
# nim = Nim(11)
# logging.debug(f"status: Initial board  -> {nim}")
# player = 0
# while nim:
#     ply = strategy[player](nim)
#     nim.nimming(ply)
#     logging.debug(f"status: After player {player} -> {nim}")
#     player = 1 - player
# winner = 1 - player
# logging.info(f"status: Player {winner} won!")

# nim = Nim(11)
# data = cook_status(nim)
# move = Nimply(data["random"], nim.rows[data["random"]])
# nim.nimming(move)
# data = cook_status(nim)
# print(data)
# print(nim)

logging.getLogger().setLevel(logging.DEBUG)
p=0.5
random.seed(42)
nWin=0
previousNWin=0
lastAction=0.01
for i in range (0,100):
    nWin = evaluate(completion_strategy_v2({"p" : p}))
    if(nWin>previousNWin):
        p+=lastAction
    else:
        if nWin>0.5:
            p+=lastAction
        elif nWin<0.5:
            lastAction=-lastAction
            p+=lastAction
    nWin_format = format(nWin, ".2f")
    p_format = format(p,".2f")
    logging.debug(f"\t\twin={nWin_format}\t\tp={p_format}\t\tlast={lastAction}")
    previousNWin = nWin
    nWin = 0
print(p)