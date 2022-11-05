import random 
import numpy as np
from sklearn.model_selection import ParameterGrid
from tqdm import tqdm
import time

#We discard duplicate elements
def problem(N, seed=42):
    """Generates the problem, also makes all blocks generated unique"""
    random.seed(seed)
    blocks_not_unique = [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]
    blocks_unique = np.unique(np.array(blocks_not_unique, dtype=object))
    return blocks_unique.tolist()

def fitness(individual):
    return sum([len(l) for l in individual])

def check_feasibility(individual, N):
    goal = set(list(range(N)))
    coverage = set()
    for list_ in individual:
        for num in list_:
            coverage.add(num)
        if coverage == goal:
            return True
    return False

def select_parent(population, tournament_size = 2):
    subset = random.choices(population, k = tournament_size)
    return min(subset, key=lambda i: i [0])

def mutation(g):
    point = random.randint(0,len(g)-1)
    return g[:point] + [not g[point]] + g[point+1:]

def cross_over(g1, g2):
    cut = random.randint(0,len(g1))
    return g1[:cut] + g2[cut:]

def calculate_mutation_probability(best_candidate, N):
    distance = abs(N - best_candidate[0])
    return 1-(distance/N)

best_candidate_option = ""

def calculate_mutation_probabilityDet2(best_candidate, N, best_candidate_list):
    global best_candidate_option

    probability_selected = 0.5
    probability_reason = ""

    # check if best changed (based on fitness func)
    if not best_candidate[0] == best_candidate_list[-1][0]:
        best_candidate_list = list()
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
        probability_reason = "distance-based"
        probability_selected = calculate_mutation_probability(best_candidate, N)

    best_candidate_option = probability_reason
    return probability_selected

PARAMETERS = {
    "N":[100, 500, 1000, 5000],
    "POPULATION_SIZE":[200, 300, 500, 600, 1000, 2000, 3000, 5000],
    "OFFSPRING_SIZE":[int(200*2/3), int(300*2/3), int(500*2/3), int(600*2/3), int(1000*2/3), int(2000*2/3), int(3000*2/3), 5000*(2/3)]
    # number of iterations? as 1000 is too small for some N values
}

configurations = {"configurations": []}
my_configs = ParameterGrid(PARAMETERS)
for config in my_configs:
    configurations["configurations"].append(config)

with open("results.csv", "a") as csvf:
    header="N,POPULATION_SIZE,OFFSPRING_SIZE,fitness,time\n"
    csvf.write(header)

    for idx in tqdm(range(len(configurations["configurations"]))):

        # for debug
        # config = {
        #     'N': 100,
        #     'POPULATION_SIZE': 50,
        #     'OFFSPRING_SIZE': 20
        # }
        config = configurations["configurations"][idx]

        start = time.time()

        problem_list = problem(config['N'])
        problem_list_np = np.array(problem_list, dtype=object)
        mutation_probability_list = list()
        mutation_probability_list.append((None, None, ""))

        population = list()
        while len(population) != config['POPULATION_SIZE']:
            random_choices = random.choices([True, False], k=len(problem_list))
            individual_lists = problem_list_np[random_choices]
            if check_feasibility(individual_lists, config['N']):
                population.append((fitness(individual_lists), random_choices, ""))

        for __ in range(1000):
            offspring_pool = list()
            while len(offspring_pool) != config['OFFSPRING_SIZE']:
                mutation_probability = calculate_mutation_probabilityDet2(population[0], config['N'], mutation_probability_list)
                if random.random() < mutation_probability:
                    p = select_parent(population)
                    new_individual = mutation(p[1])
                    type_tweak = "mutation"
                else:
                    p1, p2 = select_parent(population), select_parent(population)
                    new_individual = cross_over(p1[1], p2[1])
                    type_tweak = "cross"

                individual_lists = problem_list_np[new_individual]
                if check_feasibility(individual_lists, config['N']):
                    offspring_pool.append((fitness(individual_lists), new_individual, type_tweak))

            for o in offspring_pool:
                if o not in population:
                    population.append(o)
            population = sorted(population, key=lambda x: x[0])
            population = population[:config['POPULATION_SIZE']]

        end = time.time()
        csvf.write(f"{config['N']},{config['POPULATION_SIZE']},{config['OFFSPRING_SIZE']},{population[0][0]},{end-start}\n")
# history = ("mutation", fitness)

# if history[0] == "mutation": #se mutation (o crossover) è uguale per tutti
#     mutation_probability = 0.1