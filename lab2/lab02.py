from base64 import decode
import random 
import numpy as np
from sklearn.model_selection import ParameterGrid
from tqdm import tqdm
import time
# import sys

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

def check_feasibile(individual, N):
    '''From np array of Lists and size of problem, returns if it provides a possible solution <type 'Bool'>'''
    goal = set(list(range(N)))
    coverage = set()
    for list_ in individual:
        for num in list_:
            coverage.add(num)
        if coverage == goal:
            return True
    return False

def createFitness(individual):
    ''' Fitness measurement '''
    fitness = 0
    for list_ in individual:
        fitness += len(list_)
    return fitness

def select_parent(population, tournament_size = 2):
    ''' Random parent selection by means of a tornament'''
    subset = random.choices(population, k = tournament_size)
    return min(subset, key=lambda i: i [0])
# genetic operators
def cross_over(g1,g2, len_):
    '''one cut crossover'''
    cut = random.randint(0,len_-1)
    return g1[:cut] + g2[cut:]

def mutation(g, len_):
    point = random.randint(0,len_-1)
    return g[:point] + [not g[point]] + g[point+1:]

def calculate_mutation_probability(best_candidate, N):
    distance = abs(N - best_candidate[0])
    return 1-(distance/N)

best_candidate_option = ""

def calculate_mutation_probabilityDet2(best_candidate, N, best_candidate_list):
    ''' In case of steady state detection the system is forced to change genetic operator in order to do again some exploration'''
    global best_candidate_option

    probability_selected = 0.5
    probability_reason = ""

    # check if best changed (based on fitness func)
    if not best_candidate[0] == best_candidate_list[-1][0]:
        best_candidate_list.clear()
        best_candidate_list.append(best_candidate)
    else:
        best_candidate_list.append(best_candidate)

    # if list is bigger than 10 select opositive of current best
    if len(best_candidate_list) > 10:

        if len(best_candidate_list) < 21:
            if best_candidate[2] == "mutation":
                probability_reason= "cross"
                probability_selected = 0.1
            else:
                probability_reason= "mutation"
                probability_selected = 0.9
        else:
            probability_reason = best_candidate_option

        if len(best_candidate_list) % 20 == 0:
            if best_candidate_option == "mutation":
                probability_reason= "cross"
                probability_selected = 0.1
            else:
                probability_reason= "mutation"
                probability_selected = 0.9
    else:
        # otherwise compute the probability with a scaling factor
        probability_reason = "distance-based"
        probability_selected = calculate_mutation_probability(best_candidate, N)

    best_candidate_option = probability_reason
    return probability_selected

# Parameters for the grid search
PARAMETERS = {
    "N":[20, 100, 500, 1000, 5000],
    "POPULATION_SIZE":[50, 200, 300, 500, 600, 1000, 2000, 3000, 5000],
    "OFFSPRING_SIZE":[int(50*2/3), int(200*2/3), int(300*2/3), int(500*2/3), int(600*2/3), int(1000*2/3), int(2000*2/3), int(3000*2/3), 5000*(2/3)]
}

# Parameter grid setup
configurations = {"configurations": []}
my_configs = ParameterGrid(PARAMETERS)
for config in my_configs:
    configurations["configurations"].append(config)


random.seed(42)

with open("results.csv", "a") as csvf:
    header="N,POPULATION_SIZE,OFFSPRING_SIZE,fitness\n"
    csvf.write(header)

    for idx in tqdm(range(len(configurations["configurations"]))):

        config = configurations["configurations"][idx]

        start = time.time()
        # initial population
        initial_formulation = problem(config['N'])
        initial_formulation_np = np.array(initial_formulation, dtype=object)

        mutation_probability_list = list()
        mutation_probability_list.append((None, None, ""))
        population = list()

        # we use a while since if the checks will give always false, i can also have a population that too little in size
        while len(population) != (config['POPULATION_SIZE']):
            # list of random indexes
            # this avoid duplicate samples of the same index when initializing the first individuals
            random_choices = random.choices([True, False], k=len(initial_formulation))
            # np array of lists based on random indexes
            individual_lists = initial_formulation_np[random_choices]
            if check_feasibile(individual_lists,config['N']) == True:
                population.append((createFitness(individual_lists), random_choices, ""))

        for _ in range(1000):
            # print(f"interation {_}; w:{population[0][0]}; best calculated:{population[0][2]}")
            sum_of_cross = 0
            sum_of_mut = 0
            offspring_pool = list()
            offspring_pool_mask = list()
            i = 0
            mutation_probability = calculate_mutation_probabilityDet2(population[0], config['N'], mutation_probability_list)
            while len(offspring_pool) != config['OFFSPRING_SIZE']:
                reason = ""
                if random.random() < mutation_probability:
                    # mutation (exploitation)
                    p = select_parent(population)
                    sum_of_mut += 1
                    offspring_mask = mutation(p[1], len(initial_formulation))
                    offspring_mask = mutation(offspring_mask, len(initial_formulation))
                    reason = "mutation"
                else:
                    # crossover (exploration)
                    p1 = select_parent(population)
                    p2 = select_parent(population)
                    sum_of_cross += 1
                    offspring_mask = cross_over(p1[1],p2[1], len(initial_formulation))
                    reason = "cross"
                
                offspring_lists = initial_formulation_np[offspring_mask]
                if check_feasibile(offspring_lists, config['N']) == True and offspring_mask not in offspring_pool_mask:
                    offspring_pool.append((createFitness(offspring_lists), offspring_mask, reason))
                    offspring_pool_mask.append(offspring_mask)
            # "filtered" plus strategy
            population = population + offspring_pool
            unique_population = list()
            unique_population_mask = list()
            # duplicates removal
            for ind in population:
                if ind[1] not in unique_population_mask:
                    unique_population.append(ind)
                    unique_population_mask.append(ind[1])
            unique_population=list(unique_population)
            unique_population.sort(key=lambda x: x[0])
            # take the fittest individual
            population = unique_population[:config['POPULATION_SIZE']]

        end = time.time()
        csvf.write(f"{config['N']},{config['POPULATION_SIZE']},{config['OFFSPRING_SIZE']},{population[0][0]},{end-start}\n")

# print("END")
# print(f"size of list {len(the_list)}")
# for ind, index in zip(population, range(0,5)):
#     print(f"{ind[0]} {ind[2]}")
# print("END")