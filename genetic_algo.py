import random
from ga_parser import *

def ga_solver(path, populationSize, evolutionYear, prob):
    #Parse from json
    vehicles, jobs, matrix = get_lists(path)

    #Generate initial populations
    population = initial_population(vehicles['start_index'], jobs['location_index'], populationSize)

    for i in range(evolutionYear):
        #Calculate the route durations
        durations = calculate_total_durations(vehicles['start_index'], jobs, population, matrix)
        durationWeights = list(map(lambda x: 1/(x**5), durations))

        #Select genes according to total durations
        choosenPopulation = []
        for i in range(populationSize):
            choosenGene = random.choices(population=population,weights=durationWeights)
            choosenPopulation.append(choosenGene[0])

        #Apply crossover to the population
        population = crossover_population(choosenPopulation)

        #Mutate lucky genes
        population = mutation(population, prob)

    durations = calculate_total_durations(vehicles['start_index'], jobs, population, matrix)
    lowestDuration = min(durations)
    lowestDurIndex = durations.index(lowestDuration)
    bestRoute = population[lowestDurIndex]
    bestDurations = calculate_duration(vehicles['start_index'], jobs, bestRoute, matrix)

    result = parse_routes(bestRoute, bestDurations, vehicles, jobs)

    return result

def initial_population(startIndexes, locationIndexes, populationSize):
    population = []
    startIndexesCopy = startIndexes.copy()
    firstElem = startIndexesCopy.pop(0)
    mergedArray = startIndexesCopy + locationIndexes
    for i in range(populationSize):
        gene = [firstElem]
        random.shuffle(mergedArray)
        gene += mergedArray
        population.append(gene)

    return population

def mutation(population, prob):
    #In this GA, mutation will be replacing 2 genes' places
    geneSize = len(population[0])
    for i in range(len(population)):
        mutationProb = random.uniform(0, 1)
        if mutationProb < prob:
            gene1 = random.randint(1,geneSize-1)
            gene2 = random.randint(1,geneSize-1)
            population[i][gene1], population[i][gene2] = population[i][gene2], population[i][gene1]

    return population

def calculate_total_durations(startIndexes, jobs, population, matrix):
    pop_durations = []

    for gene in population:
        durations = calculate_duration(startIndexes, jobs, gene, matrix)
        pop_durations.append(sum(durations))

    return pop_durations

def calculate_duration(startIndexes, jobs, gene, matrix):
    durations = []
    duration = 0
    for i in range(1, len(gene)):

        if(gene[i] in startIndexes):
            
            durations.append(duration)
            duration = 0
            continue

        s = gene[i-1] #source
        d = gene[i] #destination

        currentIndex = jobs['location_index'].index(d)
        serviceDuration = jobs['service'][currentIndex]

        duration = matrix[s][d] + serviceDuration + duration

    durations.append(duration)

    return durations

def crossover_population(population):
    newPopulation = []

    if len(population) % 2 == 1:
        residual = population.pop(1)
        newPopulation.append(residual)

    it = iter(population)
    for gene1 in it:
        gene2 = next(it)

        child1, child2 = p_crossover(gene1, gene2)
        newPopulation.extend([child1, child2])

    return newPopulation

def ox_crossover(parent1, parent2):
    point1 = random.randint(0, len(parent1)-1)
    point2 = random.randint(0, len(parent1)-1)
    if point1 > point2:
        point1, point2 = point2, point1

    child1 = parent1[point1:point2+1]

    for gene in parent2:
        if gene not in child1:
            child1.append(gene)

    child2 = parent2[point1:point2+1]
    for gene in parent1:
        if gene not in child2:
            child2.append(gene)

    return child1, child2

def p_crossover(parent1, parent2):
    #This crossover technique is impressed by Proposed Crossover Operator.
    #For details, check references

    #In the 2 line below, the reason of second elements is moving to the selection part.
    child1, child2 = [parent1[0], parent2[1]], [parent1[0], parent1[1]]

    duplicatedItems1 = parent2[2::].copy()
    duplicatedItems2 = parent1[2::].copy()

    for i in range(2, len(parent1)-1):
        lastIndex1 = parent1.index(child1[-1])
        lastIndex2 = parent2.index(child2[-1])

        if (parent2[lastIndex1] in child1):
            child1.append(duplicatedItems1[0])
            duplicatedItems1.remove(child1[-1])
            child2.append(duplicatedItems2[0])
            duplicatedItems2.remove(child2[-1])
            continue   
        
        child1.append(parent2[lastIndex1])
        child2.append(parent1[lastIndex2])

        duplicatedItems1.remove(child1[-1])
        duplicatedItems2.remove(child2[-1])

    child1 += duplicatedItems1
    child2 += duplicatedItems2

    return child1, child2