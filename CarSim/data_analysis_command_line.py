import evolution
import pygmo
from Server import Server
import os
import time
import sys
import getopt

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
import json

def parse_command_string(argv):
    d ={}
    try:
        opts, args = getopt.getopt(argv, 'A:p:g:AP:f:s:v:h',
                                  ['algorithm=', 'population=', 'generation=', 'algoparams=', 'file=','seed=', 'verbosity=','help'])
    except getopt.error:
        print("There is an error")
        sys.exit(-1)
    try:
        for opt in opts:
            if opt[0] == '-h' or opt[0] == '--help':
                print(usage)
                sys.exit(0)
            if opt[0] =="-A" or opt[0]=='--algorithm':
                d['algorithm'] = opt[1]
            if opt[0] == '-p' or opt[0]=='-population':
                d['population']=opt[1]
            if opt[0] == "-g" or opt[0] == '--generation':
                d['generation'] = opt[1]
            if opt[0] == '-AP' or opt[0] == '-algoparams':
                d['algoparams'] = opt[1]
            if opt[0] == "-f" or opt[0] == '--file':
                d['params'] = opt[1]
            if opt[0] == "-s" or opt[0] == '--seed':
                d['seed'] = opt[1]
            if opt[0] == "-v" or opt[0] == '--verbosity':
                d['verbosity'] = opt[1]
    except ValueError as why:
        print('Bad parameter \'%s\' for option %s: %s\n%s' % (
            opt[1], opt[0], why, usage))
        sys.exit(-1)
    return d



if __name__ == "__main__":
    parameters = parse_command_string(sys.argv[1:])
    pygmo.set_global_rng_seed(parameters['seed'])
    server = Server()
    server.start()
    time.sleep(5)
    evo = evolution.Evolution(parameters['population'], parameters['generation'], parameters['params'], parameters['verbosity'])
    last_pop, algo = evo.evolve_params_DE_algorithm(parameters['algoparams'])
    uda = algo.extract(pygmo.sade)

