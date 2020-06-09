import json
from client import Client
from Server import Server

class My_Problem:

    def __init__(self,filename):
        d = json.load(open(filename,'r'))
        self.params_keys = list(d.keys())
        self.lower_bound = [value - abs(value*0.5) for value in d.values()]
        self.upper_bound = [value + abs(value * 0.5) for value in d.values()]
        self.servers = list()

    def fitness(self,params_values):
        client_info = Client(dict(zip(self.params_keys,params_values))).race()
        print(client_info.d)
        return [-(client_info.d['distRaced']/(client_info.d['lastLapTime']+client_info.d['curLapTime']))]

    def get_bounds(self):
        return(self.lower_bound,self.upper_bound)

    def get_used_servers(self):
        return self.servers