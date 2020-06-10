from evolution import evolve_params_DE_algorithm
import pygmo
from Server import Server
import os
import time
import sys
import getopt
import json
from utils import load_population, store_population
import problem
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
    server = Server()
    server.start()
    time.sleep(5)
    fname = 0
    p = problem.My_Problem('{}_times_evolved_parameters'.format(fname))
    pg_prob =pygmo.problem(p)
    while True:
        if fname == 0:
            population = pygmo.population(pg_prob, 7)
        else:
            population = load_population('{}_times_evolved_population'.format(fname))
        last_pop, algo = evolve_params_DE_algorithm(1, 4, 2,population)
        uda = algo.extract(pygmo.sade)
        fname += 1
        store_population('{}_times_evolved_population'.format(fname), last_pop)
        with open('log_file_{}_generations.txt'.format(fname), 'a') as f:
            for line in uda.get_log():
                f.write('{}\\n'.format(line[2:-2]))
