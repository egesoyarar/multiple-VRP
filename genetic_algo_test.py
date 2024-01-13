from genetic_algo import *
import unittest


class CheckAlgoFuncs(unittest.TestCase):
    def test_initial_population(self):
        startIndexes = [0, 1, 2]
        locationIndexes = [3, 4, 5]
        populationSize = 5

        population = initial_population(startIndexes, locationIndexes, populationSize)

        self.assertEqual(len(population), populationSize)
        self.assertEqual(len(population[0]), (len(startIndexes) + len(locationIndexes)))

        print('\nInitial Population Test passed.')

    def test_mutation(self):
        population = [[0, 1, 2, 3, 4, 5],
        [0, 5, 4, 3, 2, 1],
        [0, 3, 1, 2, 5, 4]]
        prob = 0.25

        mutated_population = mutation(population, prob)

        self.assertEqual(len(population), len(mutated_population))
        self.assertEqual(len(population[0]), len(mutated_population[0]))
        
        print('\nMutation Test passed.')

    def test_calculate_duration(self):

        # Define test inputs
        startIndexes = [0, 2, 5]
        jobs = {
            "location_index": [0, 1, 2, 3, 4, 5, 6],
            "service": [0, 20, 30, 25, 15, 10, 5]
        }
        gene = [0, 1, 6, 5, 3, 2, 4]
        matrix = [[0, 10, 20, 30, 40, 50, 60],
            [10, 0, 15, 25, 35, 45, 55],
            [20, 15, 0, 10, 20, 30, 40],
            [30, 25, 10, 0, 15, 25, 35],
            [40, 35, 20, 15, 0, 10, 20],
            [50, 45, 30, 25, 10, 0, 15],
            [60, 55, 40, 35, 20, 15, 0]
        ]

        expected_output = [90, 50, 35]

        self.assertEqual(calculate_duration(startIndexes, jobs, gene, matrix), expected_output)

        print('\nCalculate Duration Test passed.')


    def test_crossover(self):
        p1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        p2 = [0, 6, 8, 4, 3, 1, 2, 5, 7]
        
        c1, c2 = p_crossover(p1, p2)
        
        self.assertEqual(c1, [0, 6, 2, 8, 7, 5, 1, 4, 3])
        self.assertEqual(c2, [0, 1, 5, 7, 8, 2, 6, 3, 4])

        print('\nCrossover Test passed.')

if __name__ == '__main__':  
    unittest.main()  