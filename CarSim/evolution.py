#in this file we make the evolution algorithm
import pygmo

def evolve_params_DE_algorithm(self,gen,variant,variant_adpt,population = None):
    print(gen,type(gen),variant,type(variant),variant_adpt,type(variant_adpt))
    algo = pygmo.algorithm(pygmo.sade(gen,variant,variant_adpt))
    algo.set_verbosity(1)
    new_pop = algo.evolve(population)
    return new_pop,algo

def evolve_params_PSO_algorithm(self,PSO_params):
    omega,eta1,eta2,variant,neighb_type,neigh_param,seed = PSO_params.values()
    algo = pygmo.algorithm(pygmo.pso_gen(self.gen,omega=omega,eta1=eta1,eta2=eta2,variant=variant,neighb_type=neighb_type,neigh_param=neigh_param,seed=seed))
    algo.set_verbosity(self.verbosity)
    new_pop = algo.evolve(self.pop)
    return new_pop,algo