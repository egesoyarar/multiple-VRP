import argparse

from ga_parser import *
from genetic_algo import *

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='inputs/input.json', help='Input path')
    parser.add_argument('--size', type=int, default=100, help='Number of population')
    parser.add_argument('--year', type=int, default=1000, help='Number of years to run the simulation')
    parser.add_argument('--prob', type=float, default=0.05, help='Probability of mutation')

    args = parser.parse_args()

    path = args.path
    size = args.size
    year = args.year
    prob = args.prob

    result = ga_solver(path, size, year, prob)
    print(result)

if __name__ == '__main__':
    main()