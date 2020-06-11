from algorithms import evolve_params_DE_algorithm
import pygmo
from Server import Server
import time
from utils import load_population, store_population
import problem
import numpy as np
if __name__ == "__main__":
    pygmo.set_global_rng_seed(4)
    #server = Server()
    #server.start()
    #time.sleep(5)
    fname = 0
    p = problem.My_Problem('{}_times_evolved_parameters'.format(fname))
    pg_prob = pygmo.problem(p)
    while True:
        if fname == 0:
            population = pygmo.population(pg_prob, #100)
            7)
            print(type(population))
        else:
            pop = load_population('{}_times_evolved_population'.format(fname))
            population = pygmo.population()
            for p in pop:
                print(p)
                population.push_back(x=np.array(p))
        last_pop, algo = evolve_params_DE_algorithm(1, 4, 2, population)
        uda = algo.extract(pygmo.sade)
        fname += 10
        store_population('{}_times_evolved_population'.format(fname), last_pop)
        with open('log_file_{}_generations.txt'.format(fname), 'w') as f:
            for line in uda.get_log():
                f.write('{}\n'.format(line[2:-2]))
