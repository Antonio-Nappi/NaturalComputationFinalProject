# from algorithms import evolve_population_DE_algorithm
# import pygmo
from Server import Server
import time
# from utils import load_population, store_population
# import problem
import numpy as np
from CACS import CACS

if __name__ == "__main__":
    # set pygmo random seed
    # pygmo.set_global_rng_seed(190196)
    np.random.seed(211294)

    # # initialize
    # fname = 0
    #
    # # create a UDP (user defined problem) required by pygmo
    # p = problem.My_Problem('0_times_evolved_parameters'.format(0))
    # pg_prob = pygmo.problem(p)
    # individuals = 7
    # while True:
    #     if fname == 0:  # first run
    #         population = pygmo.population(pg_prob, individuals)
    #     else:
    #         population = load_population(
    #             '{}_individuals/{}_times_evolved_population'.format(individuals, fname), pg_prob)
    #     last_pop, algo = evolve_population_DE_algorithm(1, 6, 2, population)
    #     uda = algo.extract(pygmo.sade)
    #     fname += 1
    #     store_population('{}_individuals/{}_times_evolved_population'.format(individuals, fname),
    #                      last_pop)
    #     if uda is None:
    #         print("ERRORE")
    #     with open('log_file_{}_generations.txt'.format(fname), 'w') as f:
    #         for line in uda.get_log():
    #             f.write('{}\n'.format(line))

    # start two servers (one for each track)
    server_wheel = Server('forza')
    server_wheel.start()
    server_forza = Server('wheel')
    server_forza.start()
    time.sleep(10)
    dirname = 'ants_speed_extra_raced_with_bounds_evap_1.5\\'
    c = CACS('default_parameters_with_bounds', dir_name='{}'.format(dirname), n_ants=96,
             evaporation=1.5, stop_condition=100)
    c.evolve()
