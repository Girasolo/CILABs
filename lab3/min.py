import logging
from collections import namedtuple
import random
from typing import Callable
from copy import deepcopy
from itertools import accumulate
from operator import xor
import numpy as np

Nimply = namedtuple("Nimply", "row, num_objects")
value_to_keep = 0

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k
        self._total_elements = num_rows*num_rows

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    def spec(self):
        retval = ""
        count = 0
        for i in self._rows:
            for _ in range(0, ((len(self._rows) *2) - (count *2))):
                retval += " "
            for _ in range(0, i):
                retval += "| "
            if i < count * 2:
                for _ in range(0, (count * 2) - i):
                    retval += "  "
            for _ in range(0, ((len(self._rows) *2) - (count *2))):
                retval += " "
            retval += f"\t{count}\t{i}\n"
            count += 1
        return retval

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
    return cooked

def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

    
def completion_strategy_v2(state: Nim) -> Nimply:
    data = cook_status(state)

    if data["completion"] < 0.5:
        ply = Nimply(data["shortest_row"], state.rows[data["shortest_row"]])
    else:
        ply = Nimply(data["longest_row"], state.rows[data["longest_row"]])
    return ply


def completion_strategy_with_min(state: Nim) -> Nimply:
    data = cook_status(state)
    
    safety = []
    can_be_safety = []
    counter = 0
    for r in state.rows:
        if r > 2:
            can_be_safety.append(counter)
        if r == 2:
            safety.append(counter)
        counter += 1

    if len(safety) < 2 and len(can_be_safety) > 0:
        # need safety, make a safety
        print("safe")
        row_choice = random.choice(can_be_safety)
        ply = Nimply(row_choice, state.rows[row_choice] - 2)
    elif data["completion"] < 0.3 and len(safety) > 0:
        # use safety
        print("use")
        row_choice = random.choice(safety)
        ply = Nimply(row_choice, 1)
    else:
        # do normal
        print("normal")
        if data["completion"] < 0.5:
            ply = Nimply(data["shortest_row"], state.rows[data["shortest_row"]])
        else:
            ply = Nimply(data["longest_row"], state.rows[data["longest_row"]])
    return ply


NIM_SIZE = 6

nim = Nim(NIM_SIZE)
player = 0
while nim:
    print(nim.spec())
    if player == 0:
        print(f"PLAYER {player}")
        row = int(input("row:"))
        num = int(input("num:"))
        ply = Nimply(row, num)
    else:
        print("BOT")
        ply = completion_strategy_with_min(nim)
        print(ply)
    nim.nimming(ply)
    player = 1 - player
    # print(f"{nim.rows}")
    # for _ in range(0, NIM_SIZE * 2):
    #     CURSOR_UP_ONE = '\x1b[1A'
    #     ERASE_LINE = '\x1b[2K'
    #     print(CURSOR_UP_ONE + ERASE_LINE)