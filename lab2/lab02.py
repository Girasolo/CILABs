from base64 import decode
import random 
import numpy as np
from tkinter import N
import sys

# Function for the problem 
def problem(N, seed=42):
    """Creates an instance of the problem"""

    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

def checkFeasible_initial(individual, N):
    '''From np array of Lists and size of problem, returns if it provides a possible solution <type 'Bool'>'''
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


def createIndividual_initial(indexes,len_):
    '''From list of Indexes, returns mask of the individual <type 'List'>'''
    individual = np.zeros(len_, dtype=bool)
    individual[indexes] = True
    return list(individual)

def createFitness(individual):
    fitness = 0
    for list_ in individual:
        fitness += len(list_)
    return fitness

def select_parent(population, tournament_size = 2):
    subset = random.choices(population, k = tournament_size)
    return min(subset, key=lambda i: i [0])

def cross_over(g1,g2, len_):
    cut = random.randint(0,len_-1)
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
POPULATION_SIZE = 50

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
while len(population) != (POPULATION_SIZE):
    # list of random indexes
    # this avoid duplicate samples of the same index when initializing the first individuals
    individual_random_indexes = random.sample(gap, (len(initial_formulation)//2)+1)
    # np array of lists based on random indexes
    individual_lists = np.array(initial_formulation, dtype=object)[individual_random_indexes]
    # #print(individual_random_indexes)
    # #print(individual_lists)
    if checkFeasible_initial(individual_lists,5) == True:
        individual = createIndividual_initial(individual_random_indexes, len(initial_formulation))
        population.append((createFitness(individual_lists),individual))

initial_formulation_np = np.array(initial_formulation, dtype=object)

print("STARTING")
for ind in population:
    print(ind[0])
print("STARTING")

for _ in range(10):
    print("iteration: ", _)
    offspring_pool = list()
    # print("initial population: ", population)
    print("pop length 1: ", len(population))
    i = 0
    while len(offspring_pool) != 50:
        if random.random() < 0.3:
            p = select_parent(population)
            offspring_mask = mutation(p[1], len(initial_formulation))
        else:
            p1 = select_parent(population)
            p2 = select_parent(population)
            offspring_mask = cross_over(p1[1],p2[1], len(initial_formulation))
        
        offspring_lists = initial_formulation_np[offspring_mask]
        if checkFeasible_initial(offspring_lists, 5) == True:
            offspring_pool.append((createFitness(offspring_lists), offspring_mask))

    population = population + offspring_pool
    print("pop length 2: ", len(population))
    population.sort(key=lambda x: x[0])
    # take the fittest individual
    population = population[:POPULATION_SIZE]

    # print("next population ", population)
    
    print("pop length 3: ", len(population))
    
print("END")
for ind, index in zip(population, range(0,5)):
    print(ind[0])
    print(initial_formulation_np[ind[1]])
print("END")

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