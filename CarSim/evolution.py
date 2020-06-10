#in this file we make the evolution algorithm
import pygmo
import problem

class Evolution():
    def __init__(self,pop_size,gen,seed,params,verbosity):
        self.pop_size = pop_size
        self.gen = gen
        self.seed = seed
        self.verbosity = verbosity
        self.prob = pygmo.problem(problem.My_Problem(params))
        self.pop = pygmo.population(self.prob,size=pop_size,seed=self.seed)

    def evolve_params_DE_algorithm(self,DE_params):
        variant,variant_adpt,seed = DE_params.values()
        algo = pygmo.algorithm(pygmo.sade(gen=self.gen,variant=variant,variant_adpt=variant_adpt,seed=seed))
        algo.set_verbosity(self.verbosity)
        new_pop = algo.evolve(self.pop)
        return new_pop,algo

    def evolve_params_PSO_algorithm(self,PSO_params):
        omega,eta1,eta2,variant,neighb_type,neigh_param,seed = PSO_params.values()
        algo = pygmo.algorithm(pygmo.pso_gen(self.gen,omega=omega,eta1=eta1,eta2=eta2,variant=variant,neighb_type=neighb_type,neigh_param=neigh_param,seed=seed))
        algo.set_verbosity(self.verbosity)
        new_pop = algo.evolve(self.pop)
        return new_pop,algo