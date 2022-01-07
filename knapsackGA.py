import random
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(100000)

class KnapSack:
    def __init__(self, v, w, c, mw):
        self.values = v
        self.weights = w
        self.gene_len = len(v)
        self.population_size = c
        self.startpopulation = self.startPopulation(self.population_size, self.gene_len)
        
        self.max_weight = mw

        self.fitness_history = []

    def startPopulation(self, children, n):
        population = []
        for child in range(children):
            child_list = []
            for i in range(n):
                child_list.append(random.randint(0,1))
            population.append(child_list)
        return population
    
    def evaluate_fitness(self, population):
        """ Evaluate fitness scores for all genes """
        fitness_scores = []
        for single_population in population:
            total_sum = 0
            total_value = 0
            for idx, gene in enumerate(single_population):
               total_sum += self.weights[idx]*gene
               total_value += self.values[idx]*gene
            if total_sum <= self.max_weight:
                fitness_scores.append(total_value)
            else:
                fitness_scores.append(0)
        return fitness_scores

    def mating_pool(self, fitness_scores, population):
        """ Returns the new population """
        total_fitness = sum(fitness_scores)

        normalized_fitness = [i / total_fitness for i in fitness_scores]
        
        new_population = []
        for i in range(self.population_size):
            parents = random.choices(population, normalized_fitness, k=2)
            midpoint = random.randint(0,self.gene_len-1)
            random.shuffle(parents)
            child = parents[0][:midpoint] + parents[1][midpoint:]
            new_population.append(child)
        return new_population
    
    def mutate(self, population):
        mutated_population = []
        for gene in population:
            for idx, single_gene in enumerate(gene):
                if random.randint(0,1000) == 1:
                    gene[idx] = 1-single_gene
            mutated_population.append(gene)
        return(mutated_population)
                
    
    def run(self):
        return self.new_population(self.startpopulation, 10000)

    
    def new_population(self, population, n):
        if n == 0:
            return population
        fitness = self.evaluate_fitness(population)
        mating_pool = self.mating_pool(fitness, population)
        population = self.mutate(mating_pool)
        self.fitness_history.append(population)
        return self.new_population(population, n-1)
    
    def return_result(self, population):
        fitness = self.evaluate_fitness(population)
        population_fitness = list(zip(fitness, population))
        population_fitness.sort(reverse=True)
        jeans = population_fitness[0][1]
        total_v = 0
        total_w = 0
        for idx, gene in enumerate(jeans):
            if gene:
                total_v += self.values[idx]
                total_w += self.weights[idx]

        print("value", total_v)
        print("weights", total_w)
    
    def create_graph(self):
        mean_fitness = []
        max_fitness = []
        
        for population in self.fitness_history:
            fitness = self.evaluate_fitness(population)
            mean_fitness.append(sum(fitness)/len(population))
            
            fitness_population = list(zip(fitness, population))
            fitness_population.sort(reverse=True)
            max_fitness.append(fitness_population[0][0])

        plt.plot(mean_fitness, label = 'mean fitness')
        plt.plot(max_fitness, label = 'max fitness')
        plt.plot()
        plt.show()

            









values = {"kort": 150, "kompas": 35, "vand": 200, "sandwich":160, "sukker":60,"dåsemad": 45,"banan":60, "æble":40, "ost": 30, "øl": 10, "solcreme":70, "kamera":30, "T-shirt":15, "bukser":10, "paraply": 40, "vandtætte bukser": 70, "vandtæt overtøj": 75, "pung": 80, "solbriller": 20, "håndklæde":12, "sokker": 50, "bog":10, "notesbog": 1, "telt": 150}
weights = {"kort": 90, "kompas": 130, "vand": 1530, "sandwich":500, "sukker":150,"dåsemad": 680,"banan":270, "æble":390, "ost": 230, "øl": 520, "solcreme":110, "kamera":320, "T-shirt":240, "bukser":480, "paraply": 730, "vandtætte bukser": 420, "vandtæt overtøj": 430, "pung": 220, "solbriller": 70, "håndklæde":180, "sokker": 40, "bog":300, "notesbog": 900, "telt": 2000}


k = KnapSack(list(values.values()), list(weights.values()), 20, 5000)

test = k.run()
k.return_result(test)
k.create_graph()
# print(test[0])

# total_v = 0
# total_w = 0
# for idx, gene in enumerate(test[0]):
#     if gene:
#         total_v += k.values[idx]
#         total_w += k.weights[idx]

# print("value", total_v)
# print("weights", total_w)

# population = k.startpopulation
# print("start pop:", population)
# fitness = k.evaluate_fitness(population)
# print(fitness)
# mating_pool = k.mating_pool(fitness, population)
# print("new pop:", mating_pool)

