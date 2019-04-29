import random
import numpy as np

RANGE_OF_X = [-10 , 10]
POPULATION_SIZE = 10
GENES = "01"
TARGET_LENGTH = None
h = 1e-4


def f1(x):
    return x**2

def f2(x):
    return (x-2)**2

def d(f , x):
    global h
    return (f(x+h) - f(x-h))/(2*h)

def g(x):
    return f1(x) + f2(x)

def determine_target_length(range_of_x):
    n = max(range_of_x)
    return int(np.ceil(np.log(n)/np.log(2)))

class Individual(object):

    def __init__(self,chromosome):
        self.chromosome = chromosome
        self.fitness = self.calculate_fitness()

    @classmethod 
    def mutate(self):
        global GENES
        return random.choice(GENES)

    @classmethod
    def create_gnome(self):
        global TARGET_LENGTH
        return [self.mutate() for _ in range(TARGET_LENGTH)]

    def mate(self , par2):
        child_chromosome = []

        for gp1 , gp2 in zip(self.chromosome , par2.chromosome):
            probability_of_crossover = random.random()

            if (probability_of_crossover > 0.1):
                # do crossover
                probability_of_p1_gene = random.random()
                if probability_of_p1_gene > 0.5:
                    child_chromosome.append(gp1)
                else:
                    child_chromosome.append(gp2)
            else:
                # do mutation
                child_chromosome.append(self.mutate())

        return Individual(child_chromosome)

    def calculate_fitness(self):
        global TARGET_LENGTH
        s = ''.join(map(str, self.chromosome))
        x = int(s , 2)
        return g(x)
        

def main():
    global POPULATION_SIZE
    global TARGET_LENGTH
    global RANGE_OF_X

    TARGET_LENGTH = determine_target_length(RANGE_OF_X)
    
    generation = 1

    count = 1000

    population = []

    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        population.append(Individual(gnome))

    while count!=0:
        count-=1
        population = sorted(population , key = lambda x:x.fitness)

        if population[0].fitness <= 0:
            found = True
            break
        
        new_generation = []

        s = int(0.10*POPULATION_SIZE)
        new_generation.extend(population[:s])

        s = int(0.90*POPULATION_SIZE)

        for _ in range(s):
            parent1 = random.choice(population[:POPULATION_SIZE//2])
            parent2 = random.choice(population[:POPULATION_SIZE//2])
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation

        print("Gen: {} Str: {} Fit: {}".format(generation, "".join(population[0].chromosome), population[0].fitness))
        # print(parent1.chromosome, parent2.chromosome)

        generation += 1
    
    print("Gen: {} Str: {}\tFit: {}".format(generation, "".join(population[0].chromosome), population[0].fitness))

if __name__ == "__main__":
    main()