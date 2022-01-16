import random
import sys
import time
import numpy as np

from numpy.core.fromnumeric import mean

class Individual:
    def __init__(self, permsize, maxweight):
        self.perm = list(np.random.permutation(permsize))
        self.maxweight = maxweight

    def calculate_value(self, getItems=False):
        global values, weights

        weight = 0
        value = 0
        itemList = []
        itemString = ""
        for index in self.perm:
            if (weight + weights[index] <= self.maxweight):
                weight += weights[index]
                value += values[index]
                itemList.append(item_names[index])
        itemList.sort()
        for st in itemList:
            itemString += (st + ", ")
        return [itemString, weight] if getItems else value
        
    def mutate(self, percentage_chance):
        for _ in range(10):
            if random.random() < percentage_chance:
                a = random.randrange(0,len(self.perm))
                b = random.randrange(0,len(self.perm)-1)
                if a == b:
                    b += 1
                self.perm[a], self.perm[b] = self.perm[b], self.perm[a]

class Agent:
    population = []
    population_size = 0
    perm_size = 0
    maxweight = 0
    mutation_prob = 0

    def __init__(self, populationSize, permSize, maxweight, mutation_prob):
        self.population_size = populationSize
        self.perm_size = permSize
        self.maxweight = maxweight
        self.mutation_prob = mutation_prob

    def create_population(self):
        for i in range(self.population_size):
            self.population.append(Individual(self.perm_size, self.maxweight))
    
    def get_values(self):
        values = []
        for ind in self.population:
            values.append(ind.calculate_value())
        items_in_backpack, weightTotal = self.population[values.index(max(values))].calculate_value(True) #bedste indi
        return [values, weightTotal, items_in_backpack]

        
    def mate_population(self, values):
        minval = min(values)
        values = [x - minval+1 for x in values]
        total_value = sum([x**3 for x in values])
        normalized_values = [i**3 / total_value for i in values]
        new_population = []
        for _ in range(self.population_size):
            parents = random.choices(self.population, normalized_values, k=2)
            new_individual_perm = []
            idx = [0, 0]
            gene_switches = [0]*self.perm_size+[1]*self.perm_size
            random.shuffle(gene_switches)
            for elem in gene_switches:
                if parents[elem].perm[idx[elem]] not in new_individual_perm:
                    new_individual_perm.append(parents[elem].perm[idx[elem]])
                idx[elem] += 1
            child = Individual(self.perm_size, self.maxweight)
            child.perm = new_individual_perm
            new_population.append(child)
        return new_population

    def evolve_one_generation(self):
        self.population = self.mate_population(self.get_values()[0])
        for ind in self.population:
            ind.mutate(self.mutation_prob)


pre_defined_vals = list({"kort": 150, "kompas": 35, "vand": 200, "sandwich":160, "sukker":60,"dåsemad": 45,"banan":60, "æble":40, "ost": 30, "øl": 10, "solcreme":70, "kamera":30, "T-shirt":15, "bukser":10, "paraply": 40, "vandtætte bukser": 70, "vandtæt overtøj": 75, "pung": 80, "solbriller": 20, "håndklæde":12, "sokker": 50, "bog":10, "notesbog": 1, "telt": 150}.values())
pre_defined_weights = list({"kort": 90, "kompas": 130, "vand": 1530, "sandwich":500, "sukker":150,"dåsemad": 680,"banan":270, "æble":390, "ost": 230, "øl": 520, "solcreme":110, "kamera":320, "T-shirt":240, "bukser":480, "paraply": 730, "vandtætte bukser": 420, "vandtæt overtøj": 430, "pung": 220, "solbriller": 70, "håndklæde":180, "sokker": 40, "bog":300, "notesbog": 900, "telt": 2000}.values())
pre_defined_item_names = list({"kort": 90, "kompas": 130, "vand": 1530, "sandwich":500, "sukker":150,"dåsemad": 680,"banan":270, "æble":390, "ost": 230, "øl": 520, "solcreme":110, "kamera":320, "T-shirt":240, "bukser":480, "paraply": 730, "vandtætte bukser": 420, "vandtæt overtøj": 430, "pung": 220, "solbriller": 70, "håndklæde":180, "sokker": 40, "bog":300, "notesbog": 900, "telt": 2000}.keys())

agent = None
values = []
weights = []
item_names = []

def create_agent(population_size, mutation_prob, max_weight, fvals = pre_defined_vals, fweights = pre_defined_weights):
    global agent
    global weights
    global values
    global item_names

    weights = fweights
    values = fvals
    item_names = pre_defined_item_names

    agent = Agent(populationSize=population_size, permSize=len(weights), maxweight=max_weight, mutation_prob = mutation_prob)
    agent.create_population()

def get_next_valueset():
    global agent
    vs = agent.get_values()
    agent.evolve_one_generation()
        
    return [max(vs[0]), min(vs[0]), mean(vs[0]), vs[1], vs[2]]

if __name__ == "__main__":
    create_agent(200, 0.005, 5000)

    for i in range(100):
        print(get_next_valueset())
    