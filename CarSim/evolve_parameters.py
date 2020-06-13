from algorithms import evolve_population_DE_algorithm
import pygmo
from Server import Server
import time
import numpy as np
from utils import load_population, store_population
import problem
import numpy as np
from CACS import CACS

if __name__ == "__main__":
    #set pygmo random seed
    pygmo.set_global_rng_seed(4)
    np.random.seed(4)
    #start two servers (one for each track)
    server_alpine = Server('alpine')
    server_alpine.start()
    server_forza = Server('forza')
    server_forza.start()
    time.sleep(10)
    fname = 6
    # #create a UDP (user defined problem) required by pygmo
    # p = problem.My_Problem('{}_times_evolved_parameters'.format(fname))
    # #create a pygmo problem
    # pg_prob = pygmo.problem(p)
    # while True:
    #     if fname == 0: #first run
    #         #create a population of 7 individuals
    #         population = pygmo.population(pg_prob, 100)
    #     else:
    #         pop = load_population('{}_times_evolved_population'.format(fname))
    #         population = pygmo.population(pg_prob)
    #         for p in pop:
    #             population.push_back(x=np.array(p))
    #     last_pop, algo = evolve_population_DE_algorithm(1, 4, 2, population)
    #     uda = algo.extract(pygmo.sade)
    #     fname += 1
    #     store_population('{}_times_evolved_population'.format(fname), last_pop)
    #     with open('log_file_{}_generations.txt'.format(fname), 'w') as f:
    #         for line in uda.get_log():
    #             f.write('{}\n'.format(line))
    c = CACS('{}_times_evolved_parameters'.format(fname), n_ants=104, evaporation=1.1, stop_condition=100)
    c.evolve()

