from base64 import decode
import random 
import numpy as np
from tkinter import N
import sys

# Function for the problem 
def problem(N, seed=42):
    """Generates the problem, also makes all blocks generated unique"""
    random.seed(seed)
    blocks_not_unique = [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]
    blocks_unique = np.unique(np.array(blocks_not_unique, dtype=object))
    return blocks_unique.tolist()

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
    point = random.randint(0,len_-1)
    return g[:point] + [not g[point]] + g[point+1:]

def calculateMutationProbability(best_candidate, N, thr):
    distance = abs(N - best_candidate[0])
    return 1-(distance/N)
    if distance < thr:
        # print("hi prob")
        # probabilty of mutation 0.9
        # probability of cross 0.1
        p=0.9
    else:
        # probabilty of mutation 0.1
        # probability of cross 0.9
        p = 0.4
    return p

the_list = list()
the_list.append((None, None, "initial"))
the_list_counter = 0
the_list_current_option = "initial"

def calculateMutationProbabilityDet2(best_candidate, N, thr):
    global the_list, the_list_current_option

    probability_selected = 0.5
    probability_reason = ""

    # check if best changed (based on fitness func)
    if not best_candidate[0] == the_list[-1][0]:
        the_list = list()
        the_list.append(best_candidate)
    else:
        the_list.append(best_candidate)

    # if list is bigger than 10 select opositive of current best
    if len(the_list) > 10:

        if len(the_list) < 21:
            if best_candidate[2] == "mutation":
                probability_reason= "cross"
                probability_selected = 0.1
            else:
                probability_reason= "mutation"
                probability_selected = 0.9
        else:
            probability_reason = the_list_current_option

        if len(the_list) % 20 == 0:
            # print("switch")
            if the_list_current_option == "mutation":
                probability_reason= "cross"
                probability_selected = 0.1
            else:
                probability_reason= "mutation"
                probability_selected = 0.9
    else:
        probability_reason = "normal"
        probability_selected = calculateMutationProbability(best_candidate, N, thr)

    the_list_current_option = probability_reason
    # print(f"{the_list_current_option} selected")
    return probability_selected

N = 50
POPULATION_SIZE = 50
OFFSPRING_SIZE = 50

#Inital list of lists

initial_formulation = problem(N)


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
    if checkFeasible_initial(individual_lists,N) == True:
        individual = createIndividual_initial(individual_random_indexes, len(initial_formulation))
        population.append((createFitness(individual_lists),individual,"initial"))

initial_formulation_np = np.array(initial_formulation, dtype=object)

# print("STARTING")
# for ind in population:
#     print(ind[0])
# print("STARTING")

for _ in range(1000):
    # print("iteration: ", _)
    # print(f"interation {_} with {population[0][0]} because {population[0][2]}")
    sum_of_cross = 0
    sum_of_mut = 0
    offspring_pool = list()
    # print("pop length 1: ", len(population))
    i = 0
    mutation_probability = calculateMutationProbabilityDet2(population[0], N, 5)
    while len(offspring_pool) != OFFSPRING_SIZE:
        reason = ""
        if random.random() < mutation_probability:
            p = select_parent(population)
            sum_of_mut += 1
            offspring_mask = mutation(p[1], len(initial_formulation))
            offspring_mask = mutation(offspring_mask, len(initial_formulation))
            reason = "mutation"
        else:
            p1 = select_parent(population)
            p2 = select_parent(population)
            sum_of_cross += 1
            offspring_mask = cross_over(p1[1],p2[1], len(initial_formulation))
            reason = "cross"
        
        offspring_lists = initial_formulation_np[offspring_mask]
        if checkFeasible_initial(offspring_lists, N) == True:
            offspring_pool.append((createFitness(offspring_lists), offspring_mask, reason))

    # print("mut", sum_of_mut)
    # print("cross", sum_of_cross)

    population = population + offspring_pool
    unique_population = list()
    for ind in population:
        if ind not in unique_population:
            unique_population.append(ind)
    unique_population=list(unique_population)
    
    # print("pop length 2: ", len(unique_population))
    unique_population.sort(key=lambda x: x[0])
    # take the fittest individual
    population = unique_population[:POPULATION_SIZE]

    # print("next population ", population)
    
    # print("pop length 3: ", len(population))
    
print("END")
print(f"size of list {len(the_list)}")
for ind, index in zip(population, range(0,5)):
    print(f"{ind[0]} {ind[2]}")
    # print(initial_formulation_np[ind[1]])
print("END")

#for _ in range(200):

# for _ in range(200):
# p = select_parent(population)
# offspring_mask = mutation(p[1], len(initial_formulation))
# for i, j in zip(p[1], offspring_mask):
#     if i != j:
#         print("we have a difference")
    
#     print(f"i: {i} and j:{j}")

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