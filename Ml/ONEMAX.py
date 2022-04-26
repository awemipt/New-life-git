import random
import matplotlib.pyplot as plt


ONEMAXLENGTH = 100

POPULATIONSIZE = 200
P_CROSSOVER = 0.9
P_MUTATION = 0.1
MAX_GENERATIONS = 50

RANDOM_SEED = 123
random.seed(RANDOM_SEED)


class FitnessMax():
    def __init__(self):
        self.values = [0]


class Individual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = FitnessMax()


def oneMaxFitness(individual: Individual):
    return sum(individual)


def createIndividual():
    return Individual([random.randint(0, 1) for i in range(ONEMAXLENGTH)])


def createPopulation(n=POPULATIONSIZE):
    return [createIndividual() for i in range(n)]


population = createPopulation()
generationCounter = 0

fitValues = list(map(oneMaxFitness, population))

for individual, fitnessValue in zip(population, fitValues):
    individual.fitness.values[0] = fitnessValue

maxValue = []
averageValue = []


def selectionTournamentStage(inds, indsfit):
    return inds[indsfit.index(max(inds))]


def clone(value: Individual):
    ind = Individual(value)
    ind.fitness.values[0] = value.fitness.values[0]
    return ind


def selectionTournament(population, p_len):
    offspring = []
    for n in range(p_len):
        i1 = i2 = i3 = 0
        while i1 == i2 or i2 == i3 or i1 == i3:
            i1, i2, i3 = random.randint(0, p_len-1), random.randint(0, p_len-1), random.randint(0, p_len-1)
        offspring.append(max(population[i1], population[i2], population[i3], key=lambda ind: ind.fitness.values[0]))

    return offspring


def cxOnePoint(child1, child2):
    s = random.randint(2,len(child1)-3)
    child1[s:], child2[s:] = child2[s:], child1[s:]


def mutation(ind: Individual, mutarate=1.e-5):
    for i in range(len(ind)):
        if random.random()< mutarate:
            ind[i] = 0 if ind[i] == 1 else 1


while generationCounter < MAX_GENERATIONS:

    generationCounter += 1
    offspring = selectionTournament(population, len(population))
    offspring = list(map(clone, offspring))
    for child1, child2 in zip(offspring[1::2], offspring[::2]):
        if random.random()<P_CROSSOVER:
            cxOnePoint(child1, child2)

    for ind in offspring:
        if random.random()<P_MUTATION:
            mutation(ind, mutarate=1./ONEMAXLENGTH)

    freshFitValues = list(map(oneMaxFitness, offspring))

    for individual, freshFitValue in zip(offspring, freshFitValues):
        individual.fitness.values[0] = freshFitValue

    population[:] = offspring

    fitnessValues = [ind.fitness.values[0] for ind in population]

    maxValue.append(max(fitnessValues))
    averageValue.append(sum(fitnessValues)/len(population))
    print(f"Generation {generationCounter} ")

plt.plot(range(0, 50), maxValue, color='red', )
plt.plot(range(0, 50), averageValue, color='blue')
plt.xlabel("generation")
plt.ylabel("max/average fitness")
plt.show()



