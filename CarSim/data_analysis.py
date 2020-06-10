import evolution
import pygmo
from Server import Server
import os
import time
import sys
import getopt
import json
from utils import load_population,store_population
ophelp = 'Options:\n'
ophelp += ' --algorithm, -A <algorithm> the algorithm you want to evolve.\n'
ophelp += ' --population, -p <population>    dimension of the population.\n'
ophelp += ' --generation, -g <generation>     how many generation you want to train.\n'
ophelp += ' --algoparams, -AP <name>     parameter file name of the algorithm.\n'
ophelp += ' --file, -f <name>    parameter file name [default_parameters]\n'
ophelp += '--verbosity, -v <number> '
ophelp += ' --help, -h           Show this help.\n'
usage = 'Usage: %s [ophelp [optargs]] \n' % sys.argv[0]
usage = usage + ophelp

if __name__ == "__main__":
    pygmo.set_global_rng_seed(4)
    #server = Server()
    #server.start()
    #time.sleep(5)
    evo = evolution.Evolution(7, "default_parameters")
    last_pop, algo = evo.evolve_params_DE_algorithm(20,10,2)
    uda = algo.extract(pygmo.sade)
    store_population('population_20_generations',last_pop)
    with open('log_file.txt','w') as f:
        f.write(str(uda.get_log()))
