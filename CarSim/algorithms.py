#in this file we make the evolution algorithm
import pygmo

def evolve_params_DE_algorithm(gen,variant,variant_adpt,population):
    algo = pygmo.algorithm(pygmo.sade(gen,variant,variant_adpt))
    algo.set_verbosity(1)
    #print(type(algo))
    #print(type(population))
    new_pop = algo.evolve(population)
    return new_pop,algo

def evolve_params_PSO_algorithm(gen,omega,eta1,eta2,variant,neighb_type,neigh_param,population):
    algo = pygmo.algorithm(pygmo.pso_gen(gen,omega,eta1,eta2,variant,neighb_type,neigh_param))
    algo.set_verbosity(1)
    new_pop = algo.evolve(population)
    return new_pop,algo