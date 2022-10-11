import numpy as np
from CarNeuralNetwork import INPUT_SIZE, HIDDEN1_LAYER_SIZE, HIDDEN2_LAYER_SIZE, OUTPUT_SIZE, MIN_WEIGHT_VALUE, MAX_WEIGHT_VALUE

"""
------------------------
//GENETSKI ALGORITAM\\
------------------------
"""

GENES_NUM = INPUT_SIZE*HIDDEN1_LAYER_SIZE + HIDDEN1_LAYER_SIZE*HIDDEN2_LAYER_SIZE + HIDDEN2_LAYER_SIZE*OUTPUT_SIZE
POP_SIZE = 50

class Chromosome:
    def __init__(self):
        self.genes = np.random.randint(MIN_WEIGHT_VALUE, MAX_WEIGHT_VALUE, size=(GENES_NUM))/10
        self.fitness = 0
        self.weights1 = []
        self.weights2 = []
        self.weights3 = []
        
    def update_weights(self):
        k = 0
        
        w1 = np.empty((INPUT_SIZE, HIDDEN1_LAYER_SIZE))
        for i in range(INPUT_SIZE):
            for j in range(HIDDEN1_LAYER_SIZE):
                w1[i][j] = self.genes[k]
                k += 1
        self.weights1 = w1
        
        w2 = np.empty((HIDDEN1_LAYER_SIZE, HIDDEN2_LAYER_SIZE))
        for i in range(HIDDEN1_LAYER_SIZE):
            for j in range(HIDDEN2_LAYER_SIZE):
                w2[i][j] = self.genes[k]
                k += 1
        self.weights2 = w2
        
        w3 = np.empty((HIDDEN2_LAYER_SIZE, OUTPUT_SIZE))
        for i in range(HIDDEN2_LAYER_SIZE):
            for j in range(OUTPUT_SIZE):
                w3[i][j] = self.genes[k]
                k += 1
        self.weights3 = w3
    
    def fitness_calc_dummy(self):
        self.fitness = 0
        for i in range(GENES_NUM):
            self.fitness += np.abs(self.genes[i])
        
class Population:
    def __init__(self, chrom_num):
        self.num_of_chromosomes = chrom_num
        self.chromosomes = []
        for i in range(self.num_of_chromosomes):
            self.chromosomes.append(Chromosome())
            
        self.CROSSOVER_PROBABILITY = 0.6
        self.MUTATION_PROBABILITY = 0.1
        self.ELITE_NUM = 6
        self.KICK_NUM = 10
        
        self.Best_fitness = 0
        
        self.first_selected = np.empty_like(self.chromosomes[0].genes)
        self.second_selected = np.empty_like(self.chromosomes[0].genes)
        
        self.first_offspring = np.empty_like(self.chromosomes[0].genes)
        self.second_offspring = np.empty_like(self.chromosomes[0].genes)

    
    def selection(self):
        fitness_sum = 1
        for i in range(self.ELITE_NUM):
            fitness_sum += self.chromosomes[i].fitness
        
        random_select = np.random.randint(0, int(fitness_sum))
        tmp_sum = 0
        skip_index = 0
        for i in range(self.ELITE_NUM):
            tmp_sum += self.chromosomes[i].fitness
            if tmp_sum > random_select:
                np.copyto(self.first_selected, self.chromosomes[i].genes)
                skip_index = i
                fitness_sum -= self.chromosomes[i].fitness
                break
            
        random_select = np.random.randint(0, int(fitness_sum))
        tmp_sum = 0
        for i in range(self.ELITE_NUM):
            if i != skip_index:
                tmp_sum += self.chromosomes[i].fitness
                if tmp_sum > random_select:
                    np.copyto(self.second_selected, self.chromosomes[i].genes)
                    break
    
    def crossover(self):
        np.copyto(self.first_offspring, self.first_selected)
        np.copyto(self.second_offspring, self.second_selected)
        for i in range(GENES_NUM):
            if (np.random.random() < self.CROSSOVER_PROBABILITY):
                tmp = self.first_offspring[i]
                self.first_offspring[i] = self.second_offspring[i]
                self.second_offspring[i] = tmp
                   
    def reconstruct_population(self, index):
        np.copyto(self.chromosomes[(self.num_of_chromosomes-self.KICK_NUM)+2*index].genes, self.first_offspring)
        np.copyto(self.chromosomes[(self.num_of_chromosomes-self.KICK_NUM)+2*index+1].genes, self.second_offspring)
        self.chromosomes[(self.num_of_chromosomes-self.KICK_NUM)+2*index].fitness = 0
        self.chromosomes[(self.num_of_chromosomes-self.KICK_NUM)+2*index+1].fitness = 0
        
    def mutation(self):
        for i in range(GENES_NUM):
            if(np.random.random() < self.MUTATION_PROBABILITY):
                self.first_offspring[i] = np.random.randint(MIN_WEIGHT_VALUE, MAX_WEIGHT_VALUE)/10
            if(np.random.random() < self.MUTATION_PROBABILITY):
                self.second_offspring[i] = np.random.randint(MIN_WEIGHT_VALUE, MAX_WEIGHT_VALUE)/10
                 
    def make_a_step(self):
        self.chromosomes.sort(key=lambda x: x.fitness, reverse=True)
        for i in range(self.KICK_NUM//2):
            self.selection()
            self.crossover()
            self.mutation()
            self.reconstruct_population(i)

    
if __name__ == "__main__":
    pop = Population(50)    
    
    for i in range(1000):
        for i in range(50):
            pop.chromosomes[i].fitness_calc_dummy()
        pop.make_a_step()
        print(pop.chromosomes[0].fitness)

