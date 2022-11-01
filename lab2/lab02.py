from base64 import decode
import random 
import numpy as np
from tkinter import N

# Function for the problem 
def problem(N, seed=42):
    """Creates an instance of the problem"""

    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

def checkFeasible_initial(individual, N):
    goal = set(list(range(N)))
    coverage = set()
    for list_ in individual:
        for num in list_:
            coverage.add(num)
        if coverage == goal:
            return True
    return False

def checkFeasible_offspring(individual01, N, initial_formulation):
    goal = set(list(range(N)))
    mask = np.array(individual01, dtype=int) == 1
    problem_arr = np.array(initial_formulation, dtype=object)
    #print("problem, ", problem_arr)
    #print("mask: ", mask)
    decoded_formulation = problem_arr[mask]
    #decoded_formulation = problem_arr[mask]
    #print("decode: ", decoded_formulation)
    coverage = set()
    for lst in decoded_formulation:
        coverage.update(lst)
        if coverage == goal:
            return True
    return False


def createIndividual(indexes,len_):
    individual01 = np.zeros(len_, dtype=int)
    individual01[indexes] = 1
    return list(individual01)

def createFitness(induvual):
    fitness = 0
    for list_ in induvual:
        fitness += len(list_)
    return fitness 



def select_parent(population, tournament_size = 2):
    subset = random.choices(population, k = tournament_size)
    return min(subset, key=lambda i: i [0])

def cross_over(g1,g2, len_):
    cut = random.randint(0,len_)

    return g1[:cut] + g2[cut:]
# cross_over con più tagli

def mutation(g, len_):
    #print("g: ", g)
    point = random.randint(0,len_-1)
    #print("len(g): ", len(g))
    #print("cut: ", point)
    #print("new g: ", g[:point] + [1-g[point]] + g[point+1:])
    #print("len(new_g): ", len(g[:point] + [1-g[point]] + g[point+1:]))
    return g[:point] + [1-g[point]] + g[point+1:]

N = [5]

#Inital list of lists
for i in N:
    initial_formulation = problem(i)


random.seed(42)
"""
TODO:
    indexs = random_choice(0,len(initial_formulation), (len(initial_formulation)//2) +1)
    check feasiable 
    save
    creation of initial population -> len( ) = (len(initial_formulation)//2) +1
    mutation with p = 0.3
    check feasiable
    crossover
    check feasiable
    parent select
"""
gap = list(range(0,len(initial_formulation)))
population = list()

# we use a while since if the checks will give always false, i can also have a population that too little in size
while len(population) != ((len(initial_formulation)//2)+1):
    indexes = np.random.choice(gap, (len(initial_formulation)//2)+1)
    individual = np.array(initial_formulation, dtype=object)[indexes]
    if checkFeasible_initial(individual,5) == True:
        individual01 = createIndividual(indexes, len(initial_formulation))
        population.append((createFitness(individual),individual01))

for _ in range(3):
    print("iteration: ", _)
    offspring_pool = list()
    print("initial population: ", population)
    i = 0
    while len(offspring_pool) != 50:
        print(i)
        if random.random() < .3:
            p = select_parent(population) 
            offspring = mutation(p[1], len(initial_formulation))
        else:
            p1 = select_parent(population)
            p2 = select_parent(population)
            offspring = cross_over(p1[1],p2[1], len(initial_formulation))
        if checkFeasible_offspring(offspring, 5, initial_formulation) == True:
            offspring01 = createIndividual(indexes, len(initial_formulation))
            offspring_pool.append((createFitness(offspring01), offspring01))
        i = i + 1
    population = population + offspring_pool
    population.sort(key=lambda x: x[0])
    population = population[:(len(initial_formulation)//2)+1]

    print("next population ", population)


# for _ in range(200):
#     p1 = select_parent(population)
#     p2 = select_parent(population)
#     offspring = cross_over(p1[1],p2[1], len(initial_formulation))
#     print(checkFeasible_offspring(offspring, 5, initial_formulation))
#     print(checkFeasible_offspring(p2[1], 5, initial_formulation))
"""
popolazione --> p1 p2 
101010
111000
o1 = p1[:x]+p2[x:]
o1 = 101000  -->  fitness
02 = 111010  -->  fitness
chekFeasibile
addPopulation 
"""