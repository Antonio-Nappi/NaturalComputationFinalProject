#in this file we make the evolution algorithm
import pygmo
import problem
pop_size = 100
seed = 456
gen = 5
prob = pygmo.problem(problem.My_Problem("default_parameters"))
print("problema creato")
pop = pygmo.population(prob,size=pop_size,seed=seed)
print(pop)
print("popolazione creata")
algo = pygmo.algorithm(pygmo.gaco(gen=gen))
print("algoritmo creato")
new_pop = algo.evolve(pop)
print(new_pop)
print("popolazione evoluta")
