import evolution
import pygmo
from Server import Server
import os
import time
import sys
import getopt
import json
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
    #print(last_pop)
    d = json.load(open('default_parameters', 'r'))
    params_keys = list(d.keys())
    with open('modified_parameters','w') as f:
        for i in range(len(last_pop)):
            values = last_pop.get_x()[i]
            d = dict(zip(params_keys,values))
            json_object = json.dumps(d)
            f.write(json_object)
    with open('log_file.txt','w') as f:
        f.write(str(uda.get_log()))
