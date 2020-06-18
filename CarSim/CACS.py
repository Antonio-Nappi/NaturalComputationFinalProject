import csv
import json
import numpy as np
import time
from client import Client
from multiprocessing import Pool


class CACS():
    def __init__(self, param_file_name, dir_name='.\\', n_ants=None, evaporation=1,
                 stop_condition=100):
        with open('{}{}'.format(dir_name, param_file_name), "r") as file:
            self._params = json.load(file)
        self._starting_iteration = 0  # int(param_file_name[0])
        # self._param_file_name = param_file_name[0]
        self._dir_name = dir_name
        self._n_params = len(self._params.keys())
        self._n_ants = len(self._params.keys()) if n_ants is None else n_ants
        self._stop_condition = stop_condition
        self._bounds = {}
        self._x_min = {}
        self._sigma = {}
        self._evaporation = evaporation
        self._fitness = None

    def initial_solution(self):
        for key in self._params.keys():
            self._bounds[key] = (self._params[key][0] * self._params[key][1],
                                 self._params[key][0] * self._params[key][2])
            self._x_min[key] = self._params[key][0]
            self._sigma[key] = 3 * (self._bounds[key][1] - self._bounds[key][0])

    def recover_solution(self, best, last):
        self._starting_iteration = int(last.split("_")[0])
        for key in self._params.keys():
            self._bounds[key] = (self._params[key][0] * self._params[key][1],
                                 self._params[key][0] * self._params[key][2])
        with open('{}{}'.format(self._dir_name, best), "r") as best_file:
            reader = csv.reader(best_file, delimiter=",")
            for index, row in enumerate(reader):
                if index == 1:
                    fitness = float(row[0])
                    if self.is_higher_fitness(fitness):
                        self.update(fitness)
                    self._x_min = dict(zip(self._params.keys(), [float(elem) for elem in row[1:]]))
                    break
        with open('{}{}'.format(self._dir_name, last), "r") as last_file:
            reader = csv.reader(last_file, delimiter=",")
            results = []
            for index, row in enumerate(reader):
                if index > 0:
                    results.append(
                        (None, dict(zip(self._params.keys(), [float(elem) for elem in row[1:]]))))
            self.compute_sigma(results)

    def evaluate(self, params):
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
                distRaced_wheel / time_wheel) - extra_dist_penalty

    def evolve(self, recover=None):
        if recover is None:
            self.initial_solution()
            fitness = self.evaluate(self._x_min)
            print("Initial fitness:", fitness)
            if self.is_higher_fitness(fitness):
                self.update(fitness)
        else:
            self.recover_solution(recover[0], recover[1])

        for iter in range(self._starting_iteration, self._stop_condition):
            results = []
            print('iteration {}, fitness {}'.format(iter + 1, self._fitness))
            for k in range(self._n_ants):
                print('ant {}'.format(k + 1))
                x = {}
                for key in self._params.keys():
                    drawn = np.random.normal(self._x_min[key], self._sigma[key])
                    if drawn < self._bounds[key][0]:
                        drawn = self._bounds[key][0]
                    elif drawn > self._bounds[key][1]:
                        drawn = self._bounds[key][1]
                    x[key] = drawn
                fitness = self.evaluate(x)
                results.append((fitness, x))

            t0 = time.time()
            results.sort(key=lambda t: t[0], reverse=True)
            print("Time elapsed:", (time.time() - t0)/1000)
            self.store_data(
                '{}{}_ants_results.csv'.format(self._dir_name, iter + 1),
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
        for key in self._params.keys():
            xi = [elem[key] for elem in xs]
            self._sigma[key] = self._evaporation * np.std(xi)

    def store_data(self, filename, results):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            header_row = ['fitness']
            header_row.extend(self._params.keys())
            writer.writerow(header_row)
            for result in results:
                row = [result[0]]
                row.extend(result[1].values())
                writer.writerow(row)
        with open(filename[:-4], 'w', newline='') as f:
            json.dump(results[0][1], f)
