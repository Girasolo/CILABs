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

# def nim_sum(state: Nim) -> int:
#     *_, result = accumulate(state.rows, xor)
#     return result

def optimal_strategy(state: Nim) -> Nimply:
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
    cooked["random"] = random.choice([r for r, c in enumerate(state.rows) if c > 0])
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
        take = 9999

        if random.random() < 0.5:
            take = 1

        if data["completion"] < 0.5:
            ply = Nimply(data["shortest_row"], min(take, state.rows[data["shortest_row"]]))
        else:
            ply = Nimply(data["longest_row"], min(take, state.rows[data["longest_row"]]))
        return ply
    return evolvable

def E2longestVSshortest_allVS1(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)

        if random.random() < genome["p1"]:
            if random.random() < genome["p2"]:
                ply = Nimply(data["longest_row"], state.rows[data["longest_row"]])
            else:
                ply = Nimply(data["longest_row"], 1)
        else:
            if random.random() < genome["p2"]:
                ply = Nimply(data["shortest_row"], state.rows[data["shortest_row"]])
            else:
                ply = Nimply(data["shortest_row"], 1)

        return ply
    return evolvable

def completion_strategy_with_min2(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)
        
        safety = []
        can_be_safety = []
        counter = 0
        for r in state.rows:
            if r > 2:
                can_be_safety.append(counter)
            if r >= 2:
                safety.append(counter)
            counter += 1

        if data["active_rows_number"] == 1:
            # take the whole last row
            ply = Nimply(data["longest_row"], state.rows[data["longest_row"]])
        elif len(safety) < genome["p1"] and len(can_be_safety) > 0:
            # need safety, make a safety
            row_choice = random.choice(can_be_safety)
            ply = Nimply(row_choice, state.rows[row_choice] - 2)
        elif data["completion"] < genome["p2"] and len(safety) > 0:
            # use safety
            row_choice = random.choice(safety)
            ply = Nimply(row_choice, 1)
        else:
            # do normal
            # ply = Nimply(data["longest_row"], state.rows[data["longest_row"]])
            ply = Nimply(data["random"], state.rows[data["random"]])
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

def randomSmartNim() -> Callable: 
    def randomSmart(state: Nim) -> Nimply:
        data = cook_status(state)
        if data["active_rows_number"]==1:
           return Nimply(data["random"], state.rows[data["random"]])
        else: 
            row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
            num_objects = random.randint(1, state.rows[row])
            return Nimply(row, num_objects)
    return randomSmart

def evaluate(strategy: Callable) -> float:
    opponent = (strategy, randomSmartNim())
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

random.seed(42)
NUM_MATCHES = 100
logging.getLogger().setLevel(logging.DEBUG)
best_of_best = []
p=[2,0.5]
inc_p1=1
inc_p2=0.05
NIM_SIZE=11
for i in range (0,1000):
    nWin=[]
    for p1 in [p[0] + inc_p1, p[0], p[0] - inc_p1]:
        for p2 in [p[1] - inc_p2, p[1], p[1] + inc_p2]:
            nWin.append((evaluate(completion_strategy_with_min2({"p1":p1,"p2":p2})), [p1, p2]))

    best = max(nWin, key=lambda k: k[0])
    best_of_best.append(best)
    p = best[1]
    logging.debug(f"nwin={best[0]}\t\tp={best[1]}")

best_of_best.sort(key=lambda x: x[0], reverse = True)

for ind, index in zip(best_of_best, range(0,5)):
    print(f"{ind[0]} {ind[1]}")
