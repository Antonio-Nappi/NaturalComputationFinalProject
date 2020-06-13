import csv
import json
import numpy as np
from client import Client
from multiprocessing import Pool


class CACS():
    def __init__(self, param_file_name, dir_name='.\\', n_ants=None, evaporation=1,
                 stop_condition=100):
        with open('{}{}'.format(dir_name, param_file_name), "r") as file:
            self._params = json.load(file)
        self._starting_iteration = int(param_file_name[0])
        self._param_file_name = param_file_name[0]
        self._dir_name = dir_name
        self._n_params = len(self._params.keys())
        self._n_ants = len(self._params.keys()) if n_ants is None else n_ants
        self._stop_condition = stop_condition
        self._bounds = []
        self._x_min = []
        self._sigma = []
        self._evaporation = evaporation
        self._fitness = None

    def initial_solution(self):
        for i, key in enumerate(self._params.keys()):
            self._bounds.append((self._params[key] - abs(self._params[key]) * 0.5,
                                 self._params[key] + abs(self._params[key]) * 0.5))
            self._x_min.append(np.random.uniform(self._bounds[i][0], self._bounds[i][1]))
            self._sigma.append(3 * (self._bounds[i][1] - self._bounds[i][0]))

    def evaluate(self, x):
        params = dict(zip(self._params.keys(), x))
        with Pool(2) as p:
            results = p.starmap(Client, [(params, 3001), (params, 3002)])
            distRaced_forza, time_forza, length_forza = results[0].info
            distRaced_wheel, time_wheel, length_wheel = results[1].info
        extra_dist_forza = (distRaced_forza - length_forza) / 10
        extra_dist_wheel = (distRaced_wheel - length_wheel) / 10
        extra_dist_penalty = extra_dist_forza * extra_dist_wheel
        if time_forza == 0 or time_wheel == 0:
            return - np.inf
        return (distRaced_forza / time_forza) * (
                    distRaced_wheel / time_wheel) + extra_dist_penalty

    def evolve(self):
        self.initial_solution()
        fitness = self.evaluate(self._x_min)
        if self.is_higher_fitness(fitness):
            self.update(fitness)

        for iter in range(self._stop_condition):
            results = []
            for k in range(self._n_ants):
                print('iteration {}, ant {}'.format(self._starting_iteration + iter + 1, k + 1))
                x = []
                for i in range(self._n_params):
                    drawn = np.random.normal(self._x_min[i], self._sigma[i])
                    if drawn < self._bounds[i][0]:
                        drawn = self._bounds[i][0]
                    elif drawn > self._bounds[i][1]:
                        drawn = self._bounds[i][1]
                    x.append(drawn)
                fitness = self.evaluate(x)
                results.append((fitness, x))

            results.sort(reverse=True)
            self.store_data(
                '{}{}_ants_results.csv'.format(self._dir_name, self._starting_iteration + iter + 1),
                results)
            if self.is_higher_fitness(results[0][0]):
                self.update(results[0][0], results[0][1])
            self.compute_sigma(results)

    def is_higher_fitness(self, fitness):
        if self._fitness is None or fitness > self._fitness:
            return True
        else:
            return False

    def update(self, fitness, x_min=None):
        self._fitness = fitness
        if x_min is not None:
            self._x_min = x_min

    def compute_sigma(self, results):
        xs = [elem[1] for elem in results]
        for i in range(len(xs[0])):
            xi = [elem[i] for elem in xs]
            self._sigma[i] = self._evaporation * np.std(xi)

    def store_data(self, filename, results):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            header_row = ['fitness']
            header_row.extend(self._params.keys())
            writer.writerow(header_row)
            for result in results:
                row = [result[0]]
                row.extend(result[1])
                writer.writerow(row)
