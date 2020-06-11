# In this class we define our UDP (User Defined Problem) in order to use pygmo library

import json
from client import Client
import os
import subprocess


class My_Problem():

    def __init__(self, filename):
        #load original parameters
        d = json.load(open(filename, 'r'))
        self.params_keys = list(d.keys())
        #define bounds as value_of_the_parameter +- 50%
        self.lower_bound = [value - abs(value * 0.5) for value in d.values()]
        self.upper_bound = [value + abs(value * 0.5) for value in d.values()]



    def fitness(self, params_values):
        client = Client(dict(zip(self.params_keys, params_values)))
        client_info = client.race()
        #return fitness ( we have to minimize, so we want to maximize the mean speed and put a minus sign)
        return [-(client_info.d['distRaced'] / (client_info.d['lastLapTime'] + client_info.d['curLapTime']))]

    def get_bounds(self):
        #return bounds for our parameters
        return (self.lower_bound, self.upper_bound)
