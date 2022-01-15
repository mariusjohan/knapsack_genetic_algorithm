import random
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from numpy.core.fromnumeric import mean

values = list({"kort": 150, "kompas": 35, "vand": 200, "sandwich":160, "sukker":60,"dåsemad": 45,"banan":60, "æble":40, "ost": 30, "øl": 10, "solcreme":70, "kamera":30, "T-shirt":15, "bukser":10, "paraply": 40, "vandtætte bukser": 70, "vandtæt overtøj": 75, "pung": 80, "solbriller": 20, "håndklæde":12, "sokker": 50, "bog":10, "notesbog": 1, "telt": 150}.values())
weights = list({"kort": 90, "kompas": 130, "vand": 1530, "sandwich":500, "sukker":150,"dåsemad": 680,"banan":270, "æble":390, "ost": 230, "øl": 520, "solcreme":110, "kamera":320, "T-shirt":240, "bukser":480, "paraply": 730, "vandtætte bukser": 420, "vandtæt overtøj": 430, "pung": 220, "solbriller": 70, "håndklæde":180, "sokker": 40, "bog":300, "notesbog": 900, "telt": 2000}.values())
# values = [random.randint(1,1000) for _ in range(100)]
# weights = [random.randint(1,1000) for _ in range(100)]


class Individual:
    def __init__(self, permsize, maxweight):
        self.perm = list(np.random.permutation(permsize))
        self.maxweight = maxweight

    def calculate_value(self):
        weight = 0
        value = 0
        # print("Perm", self.perm)
        for index in self.perm:
            if (weight + weights[index] <= self.maxweight):
                weight += weights[index]
                value += values[index]
        return value

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

    def __init__(self, populationSize, permSize, maxweight):
        self.population_size = populationSize
        self.perm_size = permSize
        self.maxweight = maxweight

    def create_population(self):
        for i in range(self.population_size):
            self.population.append(Individual(self.perm_size, self.maxweight))
    
    def get_values(self):
        values = []
        for ind in self.population:
            values.append(ind.calculate_value())
        return values
        
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
        self.population = self.mate_population(self.get_values())
        for ind in self.population:
            ind.mutate(0.0075)


agent = Agent(populationSize=100,permSize=24,maxweight=5000)
agent.create_population()
bestval = 0 

tm = time.time()
max_values = []
mean_values = []
min_values = []

for i in range(100):
    # if i % 10 == 0:
    print(i)
    vs = agent.get_values()
    max_values.append(max(vs))
    mean_values.append(mean(vs))
    min_values.append(min(vs))
    agent.evolve_one_generation()


window = tk.Tk()

fig = plt.Figure(figsize=(20,20), dpi=100)
plot1 = fig.add_subplot(121)
plot1.plot(max_values)
canvas =FigureCanvasTkAgg(fig, master = window)
canvas.draw()
canvas.get_tk_widget().pack()
window.title("plotoitenrsaeoitn")
window.geometry("500x500")
greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()
window.mainloop()


print(max_values)
print(max(max_values))

# plt.plot(max_values)
# plt.plot(mean_values)
# plt.plot(min_values)
# plt.axis([0,1000,0,max(max_values)])
# plt.show()
print(tm-time.time())
