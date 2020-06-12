# In this class we define our UDP (User Defined Problem) in order to use pygmo library

import json
from client import Client
import os
import subprocess
from multiprocessing import Queue,Pool
import math
import time
class My_Problem():

    def __init__(self, filename):
        #load original parameters
        d = json.load(open(filename, 'r'))
        self.params_keys = list(d.keys())
        #define bounds as value_of_the_parameter +- 50%
        self.lower_bound = [value - abs(value * 0.5) for value in d.values()]
        self.upper_bound = [value + abs(value * 0.5) for value in d.values()]

    def fitness(self, params_values):
        params = dict(zip(self.params_keys, params_values))
        print('prima di valutare la fitness')
        with Pool(2) as p:
            results=p.starmap(Client,[(params,3001),(params,3002)])
            distRaced_forza,time_forza = results[0].info
            distRaced_alpine,time_alpine = results[1].info
        #return fitness ( we have to minimize, so we want to maximize the mean speed and put a minus sign)
        #distRaced_forza,time_forza=Client(params,3001).info
        print("valutata una fitness")
        #distRaced_alpine, time_alpine = Client(params,3002).info
        if time_forza == 0 or time_alpine==0:
            return [math.inf]
        return [-((distRaced_forza / time_forza) + (distRaced_alpine/time_alpine))]

        #return [-((distRaced_forza / time_forza))]

    def get_bounds(self):
        #return bounds for our parameters
        return (self.lower_bound, self.upper_bound)
